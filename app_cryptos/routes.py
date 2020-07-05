from app_cryptos import app
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from app_cryptos.forms import Formulario_Purchase
from app_cryptos.error_rlimits import CmcErrors
import datetime
import sqlite3
import json
import requests
from requests import Request
from requests import Session
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import TooManyRedirects

dataRoute = './data/Data_myCrypto.db'
API_KEY=app.config['API_KEY']

def dataQuery(consulta):

    conn = sqlite3.connect(dataRoute)
    cursor = conn.cursor()

    consulta = cursor.execute(consulta).fetchall()

    if len(consulta) == 0:
        consulta = None
    conn.commit()
    conn.close()

    return consulta

@app.route("/")
def index():
        try:
            transaccion = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")
            return render_template("index.html", route='index', transaccion=transaccion)

        except sqlite3.Error:
            errorDB = "Error establishing a database connection."
            return render_template("index.html", route='index', errorDB=errorDB)

@app.route("/purchase", methods=['GET', 'POST'])
def purchase():

    form = Formulario_Purchase(request.form)
    
    list_divisa=request.values.get("list_divisa")
    list_equivalente=request.values.get("list_equivalente")
    cantidad_Divisa=request.values.get("cantidad_Divisa")
    quant = 0
    pu = 0

    if request.method == 'GET':

        return render_template("purchase.html", route='purchase', form=form, data=[quant,pu])

    if request.values.get("calcular_equivalente"):
        if not form.validate():
            validError = "Saldo insuficiente para realizar transferencia."
            return render_template("purchase.html", route='purchase',form=form , validError=validError, data=[quant,pu])

        #Validar seleccion de la misma divisa

        if list_divisa == list_equivalente:
            EqualCurrency = "invalid operation"
            return render_template("purchase.html", route='purchase',form=form , EqualCurrency=EqualCurrency, data=[quant,pu])

        # Validacion de compatibilidad de calculo entre criptomendas

        if list_divisa == 'EUR' and list_equivalente != 'BTC':

            InvalidExchange = "invalid operation - no se puede {} con EUR".format(list_equivalente)
            return render_template("purchase.html", route='purchase',form=form , InvalidExchange=InvalidExchange, data=[quant,pu])

        if list_equivalente == 'EUR'and list_divisa != "BTC":

            InvalidExchange = "invalid operation- no se puede comprar EUR con {}".format(list_divisa)
            return render_template("purchase.html", route='purchase', form=form , InvalidExchange=InvalidExchange, data=[quant,pu])

        apiQuery = Api_Purchase(list_divisa, list_equivalente)
        if apiQuery[0] =='error':
            messageError = CmcErrors(apiQuery[1])
            errorAPI = "{}".format(messageError)
            return render_template("purchase.html", route='purchase', form=form , errorAPI=errorAPI, data=[quant,pu])
        else:
            dataQuant = apiQuery[1]

        quant = float(dataQuant)*float(cantidad_Divisa)
        pu = dataQuant

        return render_template("purchase.html", route='purchase', form=form, data=[quant, pu, list_divisa])

    if request.values.get("Op_Comprar"):

        if not form.validate():
            validError = "Saldo insuficiente para realizar transferencia."
            return render_template("purchase.html", route='purchase', form=form , validError=validError, data=[quant,pu])


        #Validacion restriccion de rangos max / min aceptadas por cantidad de divisa
        
        if list_divisa == 'EUR':
            saldo = 99999999
        else:
            try:
                saldoDisponible = dataQuery(''' WITH BALANCE AS ( SELECT SUM(to_quantity) AS saldo FROM MOVEMENTS WHERE to_currency LIKE "%{}%" UNION ALL SELECT -SUM(from_quantity) AS saldo FROM MOVEMENTS WHERE from_currency LIKE "%{}%" ) SELECT SUM(saldo) FROM BALANCE; '''.format(list_divisa, list_divisa))
            except sqlite3.Error:

                errorDB = "Error establishing a database connection."
                return render_template("purchase.html", route='purchase', form=form , errorDB=errorDB, data=[quant,pu])

            if saldoDisponible[0] == (None,):
                saldo = 0
            else:
                saldo = saldoDisponible[0][0]

        if list_divisa == 'EUR' or saldo != 0:

            dt = datetime.datetime.now()
            fecha=dt.strftime("%d/%m/%Y")
            hora=dt.strftime("%H:%M:%S")
            apiQuery = Api_Purchase(list_divisa, list_equivalente)

            if apiQuery[0] =='error':
                messageError = CmcErrors(apiQuery[1])
                errorAPI = "{}".format(messageError)
                return render_template("purchase.html", route='purchase', form=form , errorAPI=errorAPI, data=[quant,pu])
            else:
                dataQuant = apiQuery[1]
                quant = float(dataQuant)*float(cantidad_Divisa)

            # Comprobación de saldo suficiente con la crypto que se quiere comprar

            if saldo >= quant or list_divisa == 'EUR':

                conn = sqlite3.connect(dataRoute)
                cursor = conn.cursor()
                transaccion  = "INSERT INTO MOVEMENTS(date, time, from_currency, from_quantity, to_currency, to_quantity) VALUES(?, ?, ?, ?, ?, ?);"

                try:
                    cursor.execute(transaccion, (fecha, hora, list_divisa, float(quant), list_equivalente, float(cantidad_Divisa)))
                except sqlite3.Error:
                    quant = 0
                    pu = 0
                    errorDB = "Error establishing a database connection."
                    return render_template("purchase.html", route='purchase', form=form , errorDB=errorDB, data=[quant,pu])

                conn.commit()
                try:
                    transaccion = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")
                    conn.close()
                    return render_template("index.html", route='index', form=form, transaccion=transaccion)
                except sqlite3.Error:
                  
                    errorDB = "Error establishing a database connection."
                    return render_template("purchase.html", route='purchase', form=form , errorDB=errorDB, data=[quant,pu])
            else:
                pu = dataQuant
                insufficientCurrency = "No cuenta con saldo suficiente en {} para realizar la operación.".format(list_divisa)
                return render_template("purchase.html", route='purchase', form=form , insufficientCurrency=insufficientCurrency, data=[quant,pu])
        else:
  
            alert = "No cuenta con saldo en {} para realizar la operación.".format(list_divisa)
            return render_template("purchase.html", route='purchase', form=form, data=[quant, pu, list_divisa], alert=alert)

def Api_Purchase(list_equivalente, list_divisa):

    url= "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY=<API_KEY>".format(list_divisa, list_equivalente)

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY
    }
    session = Session()
    session.headers.update(headers)

    response = session.get(url)
    data = json.loads(response.text)
    try:
        return ('', data['data']['quote'][list_equivalente]['price'])
    except:
        errorCodeAPI = data['status']['error_code']
        return ('error', errorCodeAPI)


@app.route("/status")
def status():

    # Calculo Euros inversion y Saldo de euros invertidos
    try:

        empty_dataMyCrypto = dataQuery("SELECT date, time, from_currency, from_quantity, to_currency, to_quantity FROM MOVEMENTS;")

    except sqlite3.Error:

        Inversion = 0
        valor_Actual = 0
        errorDB = "Error establishing a database connection."
        return render_template("status.html", route='status', errorDB=errorDB, empty_dataMyCrypto=True)

    if empty_dataMyCrypto == None:

        return render_template("status.html", route='status', empty_dataMyCrypto=True)

    try:

        InverFrom= dataQuery('SELECT SUM(from_quantity) FROM MOVEMENTS WHERE from_currency LIKE "%EUR%";')
        InverTo= dataQuery('SELECT SUM(to_quantity) FROM MOVEMENTS WHERE to_currency LIKE "%EUR%";') 

    except sqlite3.Error:

        Inversion = 0
        valor_Actual = 0
        errorDB = "Error establishing a database connection."
        return render_template("status.html", route='status', errorDB=errorDB, empty_dataMyCrypto=True)
    
    totalInverFrom = 0
    totalInverTo = 0

    for cont1 in range(len(InverFrom)):

        if InverFrom[cont1] == (None,):

            totalInverFrom += 0

        else:

            InverFromInt = InverFrom[cont1][0]
            totalInverFrom += InverFromInt

    for cont2 in range(len(InverTo)):

        if InverTo[cont2] == (None,):

            totalInverTo += 0

        else:

            InverToInt = InverTo[cont2][0]
            totalInverTo += InverToInt

    Inversion = totalInverFrom
    totalSaldoInver = totalInverTo - totalInverFrom

    # Calculo saldo de Cryptomonedas
    try:
        cryptoSaldo()
    except sqlite3.Error:
        Inversion = 0
        valor_Actual = 0
        errorDB = "Error establishing a database connection."
        return render_template("status.html", route='status', errorDB=errorDB, empty_dataMyCrypto=True)

    # Calculo valor actual en euros de cryptos y valor actual
    cryptos_posibles = ("BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")
    cont3 = 0
    cryptoValorActual = {}
    valorActCrypto = 0
    for currency in cryptos_posibles:
        apiQuery = Api_Status('EUR', currency)
        if apiQuery[0] =='error':
            Inversion = 0
            valor_Actual = 0
            messageError = CmcErrors(apiQuery[1])
            errorAPI = "{}".format(messageError)
            return render_template("status.html", route='status', errorAPI=errorAPI, Inversion=Inversion, cryptoSaldos=cryptoSaldo(), valor_Actual=valor_Actual)
        else:
            cotizacion = apiQuery[1]
            saldoCurrency= cryptoSaldo()[cont3]
            cryptoValorActual[currency] = cotizacion * saldoCurrency
            valorActCrypto += cryptoValorActual[currency]
            cont3 += 1
    
    valor_Actual = Inversion + totalSaldoInver + valorActCrypto  
    
    return render_template("status.html", route='status', Inversion=Inversion, cryptoSaldos=cryptoSaldo(), valor_Actual=valor_Actual)

def cryptoSaldo():
    cryptos_posibles = ("BTC", "ETH", "XRP", "LTC", "BCH", "BNB", "USDT", "EOS", "BSV", "XLM", "ADA", "TRX")
    cryptoSaldos = []
    for currency in cryptos_posibles:
        exchangeCryptos = dataQuery(''' WITH BALANCE AS (SELECT SUM(to_quantity) AS saldo FROM MOVEMENTS WHERE to_currency LIKE "%{}%" UNION ALL SELECT -SUM(from_quantity) AS saldo FROM MOVEMENTS WHERE from_currency LIKE "%{}%") SELECT SUM(saldo) FROM BALANCE'''.format(currency, currency))
        if exchangeCryptos[0] == (None,):
            exchangeCryptos=0
            cryptoSaldos.append(exchangeCryptos)
        else:
            cryptoSaldos.append(exchangeCryptos[0][0])
    return cryptoSaldos

def Api_Status(list_equivalente, list_divisa):

    url= "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount=1&symbol={}&convert={}&CMC_PRO_API_KEY=<API_KEY>".format(list_divisa, list_equivalente)

    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY
    }
    session = Session()
    session.headers.update(headers)

    response = session.get(url)
    data = json.loads(response.text)
    try:
        return ('', data['data']['quote'][list_equivalente]['price'])
    except:
        errorCodeAPI = data['status']['error_code']
        return ('error', errorCodeAPI)