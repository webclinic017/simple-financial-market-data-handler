import requests
import os
import json
import yfinance as yf


indizes_de = ["dax", "mdax", "sdax", "tecdax"]
indizes_us = ["dj", "nasdaq", "sp"]
indizes_asia = ["csi300", "hsi", "n225"]
others = ["indizes", "misc"]

most_recent_comps = "30_01_21.txt"
path_components_raw = os.path.join("P://", "fin", "fin_pred", "data", "raw")
path_symbols = os.path.join("P://", "fin", "fin_pred", "data","symbols")


def isin2symbol(isin):
    r = requests.get('https://query2.finance.yahoo.com/v1/finance/search?q=' + isin + 
                     '&quotesCount=6&newsCount=0&enableFuzzyQuery=false&quotesQueryId=tss_match_phrase_query' + 
                     '&multiQuoteQueryId=multi_quote_single_token_query&newsQueryId=news_ss_symbols&enableCb=false&enableNavLinks=false&vespaNewsTimeoutMs=600')
    
    symbol = r.json()["quotes"][0]["symbol"]
    
    return symbol


def manual_modification_de(isin):
    symbol = None
    
    if(isin == "DE0006095003"):
        symbol = "ECV.DE"
    elif(isin == "IE00BZ12WP82"):
        symbol = "LIN.DE"
    elif(isin == "DE000A288904"):
        symbol = "COP.DE"
    elif(isin == "NL0012169213"):
        symbol = "QIA.DE"
    elif(isin == "DE000HAG0005"):
        symbol = "HAG.DE"
    elif(isin == "DE000SAFH001"):
        symbol = "SFQ.DE"
    elif(isin == "NL0000235190"):
        symbol = "AIR.DE"
    elif(isin == "DE000ENER6Y0"):
        symbol = "ENR.DE"
    elif(isin == "LU1673108939"):
        symbol = "AT1.DE"
        
    return symbol


def manual_modification_hsi(isin):
    symbol = None
    
    if(isin == "GB0005405286"):
        symbol = "0005.HK"
        
    return symbol


def manual_modification_us(symbol):
    if(symbol == "BF.B"):
        symbol = "BF-B"
    elif(symbol == "BRK.B"):
        symbol = "BRK-B"
        
    return symbol


def read_raw_components_de(path_components_raw):  
    result = {}
    
    with open(path_components_raw) as f:
        while True:
            name = f.readline().rstrip()
            isin = f.readline().rstrip()
            
            if not isin: break  # EOF
            
            symbol = manual_modification_de(isin)
            
            if(symbol is None):
                symbol = manual_modification_hsi(isin)
            
            if (symbol is None):            
                symbol = isin2symbol(isin)
                print(isin, name, symbol)
            if(symbol in result):
                raise Exception("Symbol already exists" + isin)
            else:
                result[symbol] = {"isin": isin, "name": name}

    return result


def read_raw_components_n225(path_components_raw):  
    result = {}
    
    with open(path_components_raw) as f:
        while True:
            symbol = f.readline().rstrip()
            name = f.readline().rstrip()      
            if not name: break  # EOF
            
            symbol += ".T"
            
            if(symbol in result):
                raise Exception("Symbol already exists: " + symbol)
            else:
                result[symbol] = {}

    return result


def read_raw_components_us(path_components_raw):    
    result = {}
    
    with open(path_components_raw) as f:
        while True:
            symbol = f.readline().rstrip()
            if not symbol: break  # EOF
            
            symbol = manual_modification_us(symbol)
                       
            if(symbol in result):
                raise Exception("Symbol already exists: " + symbol)
            else:
                result[symbol] = {}

    return result


def read_raw_components_csi300(path_components_raw):    
    result = {}
    
    with open(path_components_raw) as f:
        while True:
            symbol = f.readline().rstrip()
            if not symbol: break  # EOF
            
            symbol += ".SS" 
            t = yf.Ticker(symbol)
            df_history = t.history(interval="1h", period="3d")
            
            if(df_history.shape[0] == 0):
                symbol = symbol[:-3] + ".SZ"
                t = yf.Ticker(symbol)
                df_history = t.history(interval="1h", period="3d")
                
                if(df_history.shape[0] == 0):
                    raise Exception("Symbol doesn't exist: " + symbol)
                       
            if(symbol in result):
                raise Exception("Symbol already exists: " + symbol)
            else:
                result[symbol] = {}

    return result


def write_symbols_to_disc(symbols):
    for index, components in symbols.items():
        with open(os.path.join(path_symbols, index + ".json"), 'w') as fp:
            json.dump(components, fp, indent=4)


def validate_symbols(symbols):
    assert len(symbols["dax"]) == 30
    assert len(symbols["mdax"]) == 60
    assert len(symbols["sdax"]) == 70
    assert len(symbols["tecdax"]) == 30
    assert len(symbols["dj"]) == 30
    assert len(symbols["sp"]) == 505
    assert len(symbols["nasdaq"]) == 102
    assert len(symbols["csi300"]) == 300
    assert len(symbols["hsi"]) == 50
    assert len(symbols["n225"]) == 225
    
    if "misc" in symbols:   assert len(symbols["misc"]) == 7
    else:                   print("Attention: 'misc' is missing.")
    
    if "indizes" in symbols:   assert len(symbols["indizes"]) == 15
    else:                   print("Attention: 'indizes' is missing.")
    
    for symbol in list(symbols["dax"].keys()) + list(symbols["mdax"].keys()) + \
        list(symbols["sdax"].keys()) + list(symbols["tecdax"].keys()):     
            assert symbol[-3:] == ".DE"


def load_symbols():
    symbols = {}
    
    for idx in indizes_us + indizes_de + indizes_asia + others:
        p = os.path.join(path_symbols, idx + ".json")
        
        print(p)
        with open(p, 'r') as f:
            symbols[idx] = json.load(f)
            
    validate_symbols(symbols)
    return symbols


def load_symbols_from_raw():
    symbols = {}
    
    for idx in indizes_de:
        p = os.path.join(path_components_raw, idx, most_recent_comps)
        symbols[idx] = read_raw_components_de(p)
        
    for idx in indizes_us:
        print(idx)
        p = os.path.join(path_components_raw, idx, most_recent_comps)
        symbols[idx] = read_raw_components_us(p)   
    
    p = os.path.join(path_components_raw, "csi300", most_recent_comps)
    symbols["csi300"] = read_raw_components_csi300(p)
    
    p = os.path.join(path_components_raw, "hsi", most_recent_comps)
    symbols["hsi"] = read_raw_components_de(p)

    p = os.path.join(path_components_raw, "n225", most_recent_comps)
    symbols["n225"] = read_raw_components_n225(p)
    
      
    validate_symbols(symbols)
    return symbols


# =============================================================================
# symbols = load_symbols_from_raw()
# write_symbols_to_disc(symbols)
# =============================================================================
