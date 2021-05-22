import requests
from flask import Flask, render_template, request
from twilio.rest import Client
import requests_cache

account_sid = 'ACb66b656d1659d80ddae9f97437655c49';
auth_token = 'c88e4196e92a57787c82cc7fece74f8b';

client = Client(account_sid, auth_token)
app = Flask(__name__)


@app.route('/')
def registration_form():
    return render_template('login_page.html')


@app.route('/login_page', methods=['POST', 'GET'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['trip']
    full_name = first_name+"."+last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if travel_pass < 5 and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="whatsapp:+918143114804",
                               from_="whatsapp:+14155238886",
                               body="Hello "+" "+full_name+", "+"your travel from"+" "+source_dt+" "+"to"+" "+destination_dt+" "
                                    + "has"+" "+status+" "+"on "+date)
        return render_template('user_registration_dtls.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)
    else:
        status='Not Confirmed'
        client.messages.create(to="whatsapp:+918143114804",
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + " " + "your travel from" + " " + source_dt + " " + "to" + " " + destination_dt + " "
                                    + "has" + " " + status + " " + "on " + date + ", Apply later")
        return render_template('user_registration_dtls.html', var=full_name, var1=email_id, var2=id_proof,
                               var3=source_st, var4=source_dt, var5=destination_st, var6=destination_dt,
                               var7=phoneNumber, var8=date, var9=status)


if __name__ == "__main__":
    app.run(port=9001, debug=True)