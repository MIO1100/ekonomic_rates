from django.shortcuts import render
import threading
# Create your views here.
import datetime
from django.http import HttpResponse
from django.db import connection
import requests
import json
from .models import Rates

date = []
# to RUB
EUR = []
USD = []
CNY = []
JPY = []

# Nominal
EUR_n = []
USD_n = []
CNY_n = []
JPY_n = []

# to EUR
USD_e = []
CNY_e = []
JPY_e = []

# to USD
EUR_u = []
CNY_u = []
JPY_u = []

# to CNY
EUR_c = []
USD_c = []
JPY_c = []

# to JPY
EUR_j = []
USD_j = []
CNY_j = []
parts = [[0] for i in range(9)]


def index(request):

    date.clear()
    EUR.clear()
    USD.clear()
    CNY.clear()
    JPY.clear()
    EUR_n.clear()
    USD_n.clear()
    CNY_n.clear()
    JPY_n.clear()
    # to EUR
    USD_e.clear()
    CNY_e.clear()
    JPY_e.clear()
    # to USD
    EUR_u.clear()
    CNY_u.clear()
    JPY_u.clear()
    # to CNY
    EUR_c.clear()
    USD_c.clear()
    JPY_c.clear()
    # to JPY
    EUR_j.clear()
    USD_j.clear()
    CNY_j.clear()
    # check and add string to db
    cursor = connection.cursor()
    now = datetime.datetime.now().date()
    # cursor.execute("SELECT max(DATE) FROM db.`table`;")
    # result = cursor.fetchall()[0][0]
    result = datetime.date(2020,4,28)+datetime.timedelta(days=1)
    if (now<result):
        print("1")
        date_list = [result + datetime.timedelta(i) for i in range((now - result).days + 1)]
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        todos = json.loads(response.text)
        data= todos['Date'].split('T')[0]
        dat = datetime.date(int(data.split('-')[0]), int(data.split('-')[1]), int(data.split('-')[2]))
        rate = Rates("",dat, todos['Valute']['EUR']['Value'], todos['Valute']['USD']['Value'], todos['Valute']['JPY']['Value'], todos['Valute']['CNY']['Value'], todos['Valute']['EUR']['Nominal'], todos['Valute']['USD']['Nominal'], todos['Valute']['JPY']['Nominal'], todos['Valute']['CNY']['Nominal'])
        # cursor.execute(rate.insert())



    structure(cursor)
    for i in range(len(EUR)):
        USD_e.append( (USD[i]*USD_n[i])/(EUR[i]*EUR_n[i]))
        JPY_e.append((JPY[i]*JPY_n[i])/(EUR[i]*EUR_n[i]))
        CNY_e.append( (CNY[i]*CNY_n[i])/(EUR[i]*EUR_n[i]))

    for i in range(len(USD)):
        EUR_u.append( (EUR[i]*EUR_n[i])/(USD[i]*USD_n[i]))
        JPY_u.append( (JPY[i]*JPY_n[i])/(USD[i]*USD_n[i]))
        CNY_u.append( (CNY[i]*CNY_n[i])/(USD[i]*USD_n[i]))

    for i in range(len(CNY)):
        USD_c.append( (USD[i]*USD_n[i])/(CNY[i]*CNY_n[i]))
        JPY_c.append((JPY[i]*JPY_n[i])/(CNY[i]*CNY_n[i]))
        EUR_c.append( (EUR[i]*EUR_n[i])/(CNY[i]*CNY_n[i]))

    for i in range(len(JPY)):
        USD_j.append((USD[i]*USD_n[i])/(JPY[i]*JPY_n[i]))
        CNY_j.append( (CNY[i]*CNY_n[i])/(JPY[i]*JPY_n[i]))
        EUR_j.append( (EUR[i]*EUR_n[i])/(JPY[i]*JPY_n[i]))
    return render(
        request,
        'attachment/rates.html',
        context={'date': date, 'EUR': EUR, 'USD': USD, 'JPY': JPY, 'CNY': CNY,'EUR_u': EUR_u, 'JPY_u': JPY_u, 'CNY_u': CNY_u, 'USD_e': USD_e, 'JPY_e': JPY_e, 'CNY_e': CNY_e, 'USD_j': USD_j, 'EUR_j': EUR_j, 'CNY_j': CNY_j, 'USD_c': USD_c, 'EUR_c': EUR_c, 'JPY_c': JPY_c },
    )
def structure(curs):
    threads = []
    columns = ["DATE", "EUR", "USD", "JPY", "CNY", "EUR_n", "USD_n", "JPY_n", "CNY_n"]
    for i in range(9):
        threads.append(threading.Thread(target=get_data(columns[i], curs, i)))
        threads[i].start()

    for i in range(9):
        threads[i].join()

def get_data(column, curs, i):
    curs.execute("SELECT "+column+" FROM db.`table`;")

    if(column=="DATE"):
        for j in curs:
            s=j[0].strftime("%d.%m.%Y")
            date.append(s)

    elif(column =='EUR'):
        for j in curs:
            EUR.append(j[0])
    elif (column == 'USD'):
        for j in curs:
            USD.append(j[0])
    elif (column == 'CNY'):
        for j in curs:
            CNY.append(j[0])
    elif (column == 'JPY'):
        for j in curs:
            JPY.append(j[0])
    elif (column == 'EUR_n'):
        for j in curs:
            EUR_n.append(j[0])
    elif (column == 'USD_n'):
        for j in curs:
            USD_n.append(j[0])
    elif (column == 'CNY_n'):
        for j in curs:
            CNY_n.append(j[0])
    elif (column == 'JPY_n'):
        for j in curs:
            JPY_n.append(j[0])