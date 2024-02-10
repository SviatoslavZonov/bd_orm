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

with open('test_data1.json', 'r') as db:
    data = json.load(db)

#  Для 3 задания
# with open('tests_data.json', 'r') as db:
#     data = json.load(db)

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
session.close()

#вывод по id

# request = Publisher.id == input("Введите идентификатор издателя: ")
# q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
#     join(Publisher).join(Stock).join(Sale).join(Shop).\
#         filter(request).order_by(Sale.date_sale)
# for book, shop, price, date in q:
#         print(f'{book:<40} | {shop:<25} | {price:<10} | {date}')
#
# session.close()

# вывод по имени и id
request = input("Введите идентификатор или имя издателя: ")
if request.isnumeric():
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).\
        join(Publisher).join(Stock).join(Sale).join(Shop).\
            filter(Publisher.id == int(request)).order_by(Sale.date_sale)
    for book, shop, price, date in q:
        print(f'{book:<40} | {shop:<25} | {price:<10} | {date}')
else:
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale). \
        join(Publisher).join(Stock).join(Sale).join(Shop). \
        filter(Publisher.name.like(f'%{request}%')).order_by(Sale.date_sale)
    for book, shop, price, date in q:
        print(f'{book:<40} | {shop:<25} | {price:<10} | {date}')
session.close()