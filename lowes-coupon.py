# -*- coding: UTF-8 -*-
"""
lowes coupon generator
"""
from flask import Flask, render_template, request, jsonify
import generator
import sendgrid
import os
from sendgrid.helpers.mail import *
from cloudant import Cloudant
import json
import atexit
import datetime



app = Flask(__name__)    # Construct an instance of Flask class for our webapp
db_name = 'email'
client = None
db = None

if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.getenv('VCAP_SERVICES'))
    print('Found VCAP_SERVICES')
    if 'cloudantNoSQLDB' in vcap:
        creds = vcap['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)
elif os.path.isfile('vcap-local.json'):
    with open('vcap-local.json') as f:
        vcap = json.load(f)
        print('Found local VCAP_SERVICES')
        creds = vcap['services']['cloudantNoSQLDB'][0]['credentials']
        user = creds['username']
        password = creds['password']
        url = 'https://' + creds['host']
        client = Cloudant(user, password, url=url, connect=True)
        db = client.create_database(db_name, throw_on_exists=False)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000

port = int(os.getenv('PORT', 8000))

@app.route('/')   # URL '/' to be handled by main() route handler
def main():
    """Say hello"""
    return render_template('index.html', code_set=generator.code_gen())

# /**
#  * Endpoint to sendemail and record email to db
# * Send a POST request to localhost:8000/api/sendemail with body
# * {
# *     "email": "name@example.com"
# * }
# */
#  */
@app.route('/api/sendemail', methods=['POST'])
def sendemail():
    email = request.json['email']
    if client:
        data = {'email': email, 'timestamp': datetime.datetime.now().isoformat()}
        db.create_document(data)
        #send email
        sg = sendgrid.SendGridAPIClient(apikey='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')
        from_email = Email("noreply@acouponpool.com")
        to_email = Email(email)
        subject = "Your Lowe's Coupons"
        content = Content("text/plain", "Coupon code is ...")
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return 'Hello %s! I added the email to the database.' % email
    else:
        print('No database')
        return 'Hello %s!' % email


@atexit.register
def shutdown():
    if client:
        client.disconnect()


if __name__ == '__main__':  # Script executed directly?
    app.run(host='0.0.0.0', port=port)  # Launch built-in web server and run this Flask webapp