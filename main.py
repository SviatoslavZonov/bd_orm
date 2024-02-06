import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json

from DBModels import create_tables, Publisher, Sale, Book, Stock, Shop

SQLsystem = 'postgresql'
login = 'postgres'
password = 'bdlike45'
host = 'localhost'
port = 5432
db_name = "DBORM"
DSN = f'{SQLsystem}://{login}:{password}@{host}:{port}/{db_name}'
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open('tests_data.json', 'r') as db:
    data = json.load(db)

for line in data:
    method = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line['model']]
    session.add(method(id=line['pk'], **line.get('fields')))

session.commit()

#доработать вывод

request = input('Введи имя писателя или id для вывода: ')
result = (session.query(Book, Shop, Sale).
          filter(Publisher.name == request).
          filter(Publisher.id == Book.id).
          filter(Book.id_publisher == Stock.id_book).
          filter(Stock.id_shop == Shop.id).
          filter(Stock.id == Sale.id_stock).all())
for r in result:
    print(f'{r[0]} | {r[1]} | {r[2]}')

session.close()