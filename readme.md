# MyCrypto Simulation 🏗️

Proyecto Final BootCamp Zero - V Edición | KeepCoding

Aplicación web: Simulador de cryptos 

# Introduction 📃 

Simulador de inversiones en cryptos que retorna el valor real en euros de las
diez cryptomonedas con mayor volumen de negocio actualmente. 

La aplicación está conformada por tres views, a saber:

* **/:** Muestra la tabla con los movimientos (compras y conversiones de cryptomonedas) realizadas por el usuario.

* **/purchase:** Se trata de un formulario en el que es posible realizar una compra, venta o intercambio de monedas. Se podrá comprar **BTC** en **Euros** y vender **BTC** a **Euros**, el resto de cryptomonedas se intercambiarán por **BTC** y entre ellas.

* **/status:** mostrará en pantalla el estado de la inversión, los euros gastados en comprar **BTC** y el valor actual del total de cryptomonedas que existan en el stock del usuario según sus movimientos.


## Stack 📚

* [Python](https://www.python.org/) - Programming language
* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web develoment
* [Skeleton CSS](http://getskeleton.com/) - Framework CSS
* [Jinja2](https://jinja.palletsprojects.com/en/2.11.x/) - Web template engine
* [SQLite](https://www.sqlite.org/index.html) - Database engine
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - Form library
* [AWS](https://aws.amazon.com/es/) - Web deploy

## Getting started 🏁

* **Crear y Activar entorno virtual**
```
python -m venv venv 
venv\Scripts\activate
```
* **Instalar versiones actualizadas del archivo "requirements" y actualizarlo para posteriores usos:**
```
pip install  -r requirements.txt
pip install --upgrade --force-reinstall -r requirements.txt
pip freeze > requirements.txt
```
Renombrar el archivo **.env_template** por **.env**
```
FLASK_APP=pon aquí tu punto de entrada
FLASK_ENV=entorno
```
debe sustituir los datos por:
```
FLASK_APP=run.py
FLASK_ENV=development
```
* **Crear Base de datos Data_myCrypto.db**

Debe ejecutar **migrations.sql** con **Sqlite3** en el fichero elegido como base de datos.

* **Crear variable de entorno en el terminal**
```
set FLASK_APP=run.py
set FLASK_ENV=development
```
*  **Vincular API**

Visitar la web de CoinMarketCap para conseguir una APIKEY:
```
https://pro.coinmarketcap.com/
```
Introducir su API_KEY y genere su SECRET_KEY en el archivo **config_key.py** y renombrelo como **config.py** 



* **Lanzar aplicación**
```
flask run
```
## Database 🛠️

El siguiente apartado corresponde a los esquemas de las tablas usadas en la base de datos **Data_myCrypto.db**

**MOVEMENTS**

| Columna | Tipo |
|     :---      |   :---   |
| id | integer, clave primaria |
| date | Text (formato YYYY-MM-DD) |
| time | Text (formato HH:MM:SS.nnn) |
| from_currency | integer Foreign key a CRYPTOS |
| form_quantity| Real |
| to_currency|Real |
| to_quantity|Real |

**CRYPTOS**

| Columna | Tipo |
|     :---      |   :---   |
| id | integer, clave primaria |
| symbol | Text |
| name | Text |

las monedas o cryptomonedas utilizadas para el desarrollo de este simulador fueron: 

**EUR, BTC, ETH, XRP, LTC, BCH, BNB, USDT, EOS,BSV, XLM, ADA, TRX.**
