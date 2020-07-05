
#CoinMarketCap Errors and Rate Limits

def CmcErrors(codigo):
    if codigo == 1001:
        error_message  = "This API Key is invalid."
    elif codigo == 1002:
        error_message = "API key missing."
    elif codigo == 1003:
        error_message = "Your API Key must be activated. Please go to pro.coinmarketcap.com/account/plan."
    elif codigo == 1004:
        error_message = "Your API Key's subscription plan has expired."
    elif codigo == 1005:
        error_message = "An API Key is required for this call."
    elif codigo == 1006:
        error_message = "Your API Key subscription plan doesn't support this endpoint."
    elif codigo == 1007:
        error_message = "This API Key has been disabled. Please contact support."
    elif codigo == 1008:
        error_message = "You've exceeded your API Key's HTTP request rate limit. Rate limits reset every minute."
    elif codigo == 1009:
        error_message = "You've exceeded your API Key's daily rate limit."
    elif codigo == 1010:
        error_message = "You've exceeded your API Key's monthly rate limit."
    elif codigo == 1011:
        error_message = "You've hit an IP rate limit."
    return error_message 