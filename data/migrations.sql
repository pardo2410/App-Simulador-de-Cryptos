CREATE TABLE "cryptos" (
	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"symbol"	TEXT NOT NULL,
	"name"	TEXT NOT NULL
)

CREATE TABLE "movements" (
	"Id"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"date"	TEXT NOT NULL,
	"time"	TEXT NOT NULL,
	"from_currency"	TEXT NOT NULL,
	"from_quantity"	REAL NOT NULL,
	"to_currency"	TEXT NOT NULL,
	"to_quantity"	REAL NOT NULL,
	FOREIGN KEY("to_currency") REFERENCES "cryptos"("Id"),
	FOREIGN KEY("from_currency") REFERENCES "cryptos"("Id")
)
