import os
import yfinance as yf
import pandas as pd

import matplotlib.pyplot as plt

from symbol_management import path_symbols, load_symbols


def initial_acquisition(symbols, interval, period):
    symbols_success = set()
    symbols_issue = set()
    symbols_dublicate = set()
    c = 0
    
    
    for idx, components in symbols.items():
        for symbol, values in components.items():
            c+= 1
            if(symbol == "CON.DE"):
                save_path = os.path.join(data_path, interval, "CON_.DE") + ".pkl"
            else:
                save_path = os.path.join(data_path, interval, symbol) + ".pkl"

            
            if(os.path.isfile(save_path)):
                symbols_dublicate.add(symbol)
                continue
            
            t = yf.Ticker(symbol)
            df_history = t.history(interval=interval, period=period)
            
            print(symbol, df_history.shape)
            
            if(df_history.shape[0] == 0):
                symbols_issue.add(symbol)
                continue
            
            df_history.to_pickle(save_path)            
            
            symbols_success.add(symbol)
    print(c)
    
    return symbols_success, symbols_dublicate, symbols_issue


def filename2symbol(filename):   
    if(filename == "CON_.DE"):
        return "CON.DE"
    else:
        return filename


def check_for_duplicates(interval):
    contain_duplicates = []
    
    save_path = os.path.join(data_path, interval)
    for filename in os.listdir(save_path):
        if filename.endswith(".pkl"):
            path = os.path.join(save_path, filename)
            df = pd.read_pickle(path)
            if(df.index.duplicated().any()):
                contain_duplicates.append(filename)
    return contain_duplicates


def check_for_NaNs(interval):
    contain_NaNs = []
    
    save_path = os.path.join(data_path, interval)
    for filename in os.listdir(save_path):
        if filename.endswith(".pkl"):
            path = os.path.join(save_path, filename)
            df = pd.read_pickle(path)
            if(df.isnull().values.any()):
                contain_NaNs.append(filename)
    return contain_NaNs
    

def update_all_existing_symbols(interval):  
    symbols_success = set()
    symbols_issue = set()
    symbols_unchanged = set()
    
    save_path = os.path.join(data_path, interval)
    
    for filename in os.listdir(save_path):
        if filename.endswith(".pkl"):
            symbol = filename2symbol(filename[:-4])           
            path = os.path.join(save_path, filename)
            df_old = pd.read_pickle(path)
            
            
            df_new = update_symbol_data(symbol, df_old.copy(), interval)
            n_rows_diff = df_new.shape[0] - df_old.shape[0]
            
            print(symbol + ": ", n_rows_diff)

            if(n_rows_diff > 0):
                df_new.to_pickle(path)
                symbols_success.add(symbol)
            elif(n_rows_diff == 0):
                symbols_unchanged.add(symbol)
            else:
                symbols_issue.add(symbol)

    return symbols_success, symbols_unchanged, symbols_issue

failed = []
def update_symbol_data(symbol, df, interval):    
    
    if(df.shape != (0,7)):
        most_recent_date = df.iloc[-1].name.date().strftime('%Y-%m-%d')
        
        #most_recent_date = "2021-02-14"
        
        most_recent_date_old = most_recent_date
        #print(most_recent_date_old)
        t = yf.Ticker(symbol)
        rows_update = t.history(interval=interval, start=most_recent_date)
                
        print(rows_update.shape[0])
        if(rows_update.shape[0] == 0):
            return df
        
        #print("rows_update", rows_update.shape)
        #most_recent_date = rows_update.iloc[0].name.date().strftime('%Y-%m-%d')
        if(most_recent_date != most_recent_date_old):
            failed.append([symbol, most_recent_date_old, most_recent_date])
        #print(most_recent_date)
        #print("----")
        #print(most_recent_date)
        rows_to_drop = df.loc[most_recent_date:]
        #print(rows_to_drop.shape)
                
        if(rows_to_drop.shape != (0,7)):
            rows_remaining = df.drop(rows_to_drop.index)
        else:
            rows_remaining = df
                
        result = pd.concat([rows_remaining, rows_update[most_recent_date:]])

        #raise SystemExit()
    else:
        t = yf.Ticker(symbol)
        result = t.history(interval=interval, start="2010-01-01")
    
    return result


data_path = os.path.join("P://", "fin", "fin_pred","data")

symbols = load_symbols()

# =============================================================================
# DEPRECATED:
#   CXO   
# =============================================================================


# ALWAYS RUN AFTER SYMBOL CHANGES
# =============================================================================
# result = initial_acquisition(symbols, "1m", "7d")
# result = initial_acquisition(symbols, "15m", "60d")
# result = initial_acquisition(symbols, "60m", "730d")
# result = initial_acquisition(symbols, "1d", "10y")
# =============================================================================

result = update_all_existing_symbols("1m")
result = update_all_existing_symbols("15m")
result = update_all_existing_symbols("60m")
result = update_all_existing_symbols("1d")

res = check_for_duplicates("1m")
res = check_for_NaNs("1m")

symbol = "GC=F"
interval = "1m"
period = "7d"

t = yf.Ticker(symbol)
df  = t.history(interval=interval, start="2021-02-26")

#res = t.recommendations


path = os.path.join(data_path, interval, symbol) + ".pkl"
df = pd.read_pickle(path)




# get dublicate row indizes
# df.index[df.index.duplicated() == True]

# access rows by datetime
#w = df.loc['2021-01-21'].between_time('09:26', '09:32')





# plot
path = os.path.join(data_path, "1d", "^GDAXI") + ".pkl"
df = pd.read_pickle(path)
test = df["Close"].to_numpy()
plt.plot(test)

df.plot(y="Close")



# manually update symbol data
symbol = "GC=F"
filename = "GC=F"
interval = "1m"
t = yf.Ticker(symbol)
path = os.path.join(data_path, interval, filename) + ".pkl"
df = pd.read_pickle(path)
df_new = update_symbol_data(symbol, df, interval)
#df_new.to_pickle(path)



t = df.index.isin(df_new.index)
missing = df.index[~t]

# manually drop n last columns of dataframe
# =============================================================================
# save_path = os.path.join(data_path, "1d")
# for filename in os.listdir(save_path):
#     if filename.endswith(".pkl"):          
#         path = os.path.join(save_path, filename)
#         df = pd.read_pickle(path)
#         df.drop(df.tail(50).index,inplace=True)
#         print(df.shape)
#         
#         df.to_pickle(path)
# =============================================================================


most_recent_date = "2021-03-02"
t = yf.Ticker("symbol")
rows_update = t.history(interval=interval, start=most_recent_date)


rows_update[most_recent_date:]

