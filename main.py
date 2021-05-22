import requests
from flask import Flask, render_template, request
from twilio.rest import Client
#import requests_cache
account_sid="AC1418154aa86c33cd709246c3359f216f"
auth_token="8b3515614f8c09d97704477fc313d5f7"
client=Client(account_sid,auth_token)
app = Flask(__name__, static_url_path='/static')
@app.route('/')
def form():
    return render_template('input.html')

@app.route('/epass', methods=['POST',"GET"])
def epass():
    firstName =request.form['fname']
    lastName = request.form['lname']
    emailID  = request.form['email']
    sourceST = request.form['sourceST']
    sourceDT = request.form['sourceDT']
    destinationST = request.form['destST']
    destinationDT = request.form['destDT']
    phoneNumber = request.form['phoneNumber']
    idProof = request.form['idProof']
    date = request.form['trip']
    fullName =firstName + "." + lastName
    r =requests.get('https://api.covid19india.org/v4/data.json')
    jsonData = r.json()
    cnt = jsonData[destinationST]['districts'][destinationDT]['total']['confirmed']
    pop = jsonData[destinationST]['districts'][destinationDT]['meta']['population']
    travelPass = (cnt/pop)*100
    status=""
    if(travelPass < 30 and request.method=='POST'):
        status='CONFIRMED'
    else:
        status = 'CANCELED'
    client.messages.create(to="whatsapp:+916301380280",from_="whatsapp:+14155238886",body="Hi"+" "+fullName+" "+"Your travel from"+sourceST+" "+sourceDT+" to"+destinationST+" "+destinationDT+" on"+date+"has"+status)
    return render_template('output.html', var=fullName, var1=emailID, var2=idProof, var3=sourceST, var4=sourceDT, var5=destinationST, var6=destinationDT, var7=phoneNumber, var8=date, var9=status)

if __name__ == '__main__':
    app.run()