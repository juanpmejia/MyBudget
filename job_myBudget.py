import schedule
import time
import os
import urllib.request

def job():
    print("VOY A PEDIR LA PAGINA!")
    urllib.request.urlopen("https://ide.c9.io/juanpam/mybudget-test").read()
    print("ACABO DE PEDIR LA PAGINA!")

schedule.every(10).seconds.do(job)
# schedule.every().hour.do(job)

while 1:
    schedule.run_pending()
