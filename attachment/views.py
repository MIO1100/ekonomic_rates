from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponse
from django.db import connection
import requests
import json
from .models import Rates
def index(request):
    # check and add string to db
    cursor = connection.cursor()
    now = datetime.datetime.now().date()
    cursor.execute("SELECT max(DATE) FROM db.`table`;")
    result = cursor.fetchall()[0][0]
    result = datetime.date(2020,4,28)+datetime.timedelta(days=1)
    if (now<result):
        print("1")
        date_list = [result + datetime.timedelta(i) for i in range((now - result).days + 1)]
        response = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        todos = json.loads(response.text)
        data= todos['Date'].split('T')[0]
        date = datetime.date(int(data.split('-')[0]), int(data.split('-')[1]), int(data.split('-')[2]))
        rate = Rates("",date, todos['Valute']['EUR']['Value'], todos['Valute']['USD']['Value'], todos['Valute']['JPY']['Value'], todos['Valute']['CNY']['Value'], todos['Valute']['EUR']['Nominal'], todos['Valute']['USD']['Nominal'], todos['Valute']['JPY']['Nominal'], todos['Valute']['CNY']['Nominal'])
        cursor.execute(rate.insert())


    s = cursor.execute("SELECT * FROM db.`table`")
    print(s)
    # for row in cursor:
    #     print(row)
    #


    return render(
        request,
        'attachment/rates.html',
        context={'data': cursor.description},
    )
