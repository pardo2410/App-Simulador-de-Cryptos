from flask_wtf import FlaskForm
from wtforms import StringField 
from wtforms import IntegerField 
from wtforms import SubmitField 
from wtforms import SelectField 
from wtforms import Label 
from wtforms import FloatField
from wtforms.validators import DataRequired 
from wtforms.validators import InputRequired 
from wtforms.validators import NumberRange 
from wtforms.validators import Length
from wtforms.widgets import Select

class Formulario_Purchase(FlaskForm):
    list_divisa = SelectField('From', choices=[(-1, 'Seleccione Moneda'), ('EUR', 'EURO (EUR)'), ('BTC', 'Bitcoin (BTC)'), ('ETH', 'Ether (ETH)'), ('XRP', 'Ripple (XRP)'), ('LTC', 'Litecoin (LTC)'), ('BCH', 'Bitcoin Cash (BCH)'), ('BNB', 'Binance Coin (BNB)'), ('USDT', 'Tether (USDT)'), ('EOS', 'EOS (ESO)'), ('BSV', 'Bitcoin SV (BSV)'), ('XLM', 'Stellar (XLM)'), ('ADA', 'Cardano (ADA)'), ('TRX', 'TRON (TRX)')])
    list_equivalente = SelectField('To', choices=[(-1, 'Seleccione Moneda'), ('EUR', 'EURO (EUR)'), ('BTC', 'Bitcoin (BTC)'), ('ETH', 'Ether (ETH)'), ('XRP', 'Ripple (XRP)'), ('LTC', 'Litecoin (LTC)'), ('BCH', 'Bitcoin Cash (BCH)'), ('BNB', 'Binance Coin (BNB)'), ('USDT', 'Tether (USDT)'), ('EOS', 'EOS (ESO)'), ('BSV', 'Bitcoin SV (BSV)'), ('XLM', 'Stellar (XLM)'), ('ADA', 'Cardano (ADA)'), ('TRX', 'TRON (TRX)')])
    cantidad_Divisa = FloatField('Cantidad', validators=[InputRequired(), NumberRange(min=0.00001, max=99999999, message='no valido')])

    calcular_equivalente = SubmitField('Calcular')
    Op_Comprar = SubmitField('Aceptar')

