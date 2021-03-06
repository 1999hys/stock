from flask import Flask, request, render_template ,redirect ,url_for
from flask_mail import Mail,Message
import pandas as pd
import csv
import numpy as np
import getData, catStock, getID
import click
import datetime

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
stockID = '2427'
itStock = ['2427', '2453', '2468', '2471', '2480', '3029', '3130', '4994', '5203', '6112', '6183', '6214']
a = 0
accountInfo = ['','','','']

#信箱設置
app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_DEFAULT_SENDER=('hahaha', 'jjfj3750@gmail.com'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='jjfj3750@gmail.com',
    MAIL_PASSWORD='<a1s2d3f4>'
)
mail = Mail(app)

@app.route("/message/<ema>/<acc>/<pw1>/<pw2>")
def message(acc,ema,pw1,pw2):
    print(acc,pw1,pw2)
    msg_title = 'Hahahaha'
    msg_recipients = [ema]
    msg_body = '沒想到成功了欸\r\n系統時間：' + str(datetime.datetime.now())
    msg = Message(msg_title,recipients=msg_recipients)
    msg.body = msg_body
    mail.send(msg)
    global accountInfo
    accountInfo = getID.checkAccInfo(acc,ema,pw1,pw2)
    print(accountInfo)
    return redirect(url_for('account'))

#記錄登入狀況
@app.route("/")
def home():
    return render_template('login.html') 

@app.route("/login")
def login():
    return render_template('login.html') 

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/account")
def account():
    return render_template('account.html', info = accountInfo)

@app.cli.command("refresh")
def refresh():
    catStock.catStock()

#查詢功能 + 重新導向
@app.route("/chart/<cType>",methods=['POST'])
def searchCha(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkCha(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('chart', stId = stockID, cType = chart[0]))

@app.route("/technical/<cType>",methods=['POST'])
def searchTec(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkTec(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('technical', stId = stockID, cType = chart[0]))

@app.route("/financial/<cType>",methods=['POST'])
def searchFin(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkFin(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('financial', stId = stockID, cType = chart[0]))

@app.route("/predict/<cType>",methods=['POST'])
def searchPre(cType):
    global stockID
    ID = str(request.values['stock_id'])
    err = getID.check(ID)
    chart = getID.checkPre(cType)
    if err == 0:
        stockID = ID
    return redirect(url_for('predict', stId = stockID, cType = chart[0]))    
    

#進入30日圖表 /chart/30days/2427
#進入當日圖表 /chart/today/2427
@app.route("/chart/<cType>/<stId>")
def chart(cType,stId):
    global stockID
    print(stId)
    print(cType)
    err = getID.check(stId)
    chart = getID.checkCha(cType)
    if err == 0:
        stockID = stId
    name = getID.getName(stockID)
    data = getData.getData(stockID)
    datatoday = getData.getTodayCsv(stockID)
    return render_template('index.html', re = data, name = name, today = datatoday, cType = chart, err = err, stock = stockID) 

#進入技術指標 /technical/rsi/2427 
@app.route("/technical/<cType>/<stId>")
def technical(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkTec(cType)
    if err == 0:
        stockID = stId
    dataTec = getData.getAll(stockID)
    data = getData.getData(stockID)
    name = getID.getName(stockID)
    return render_template('technical.html', re = data, name = name, tec = dataTec, cType = chart, err = err, stock = stockID) 

#進入技術指標 /financial/SymScore/2427 
@app.route("/financial/<cType>/<stId>")
def financial(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkFin(cType)
    if err == 0:
        stockID = stId
    dataFin = getData.getFin(stockID, chart[1])
    name = getID.getName(stockID)
    return render_template('financial.html', name = name, fin = dataFin, cType = chart, err = err, stock = stockID) 

#進入技術指標 /predict/pre/2427 
@app.route("/predict/<cType>/<stId>")
def predict(cType,stId):
    global stockID
    print(stId)
    err = getID.check(stId)
    chart = getID.checkPre(cType)
    if err == 0:
        stockID = stId
    dataPre = getData.getPre(stockID)
    print(dataPre)
    name = getID.getName(stockID)
    return render_template('predict.html', name = name, pre = dataPre, cType = chart, err = err, stock = stockID)     


if __name__ == "__main__":

    app.run(debug=True)