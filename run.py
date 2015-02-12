from flask import flash, Flask, Markup, redirect, render_template, url_for
from flask.ext.wtf import Form
from wtforms import fields
import requests, json, flask

SECRET_KEY = 'Insecure-secret-key'
WTF_CSRF_SECRET_KEY = 'this-should-be-more-random'

app = Flask(__name__)
app.config.from_object(__name__)

class SubmitForm(Form):
    title = fields.StringField()
    address = fields.StringField()
    application_Type = fields.StringField()

class ReceiveForm(Form):
    item_id = fields.StringField()

@app.route("/")
def index():
    receive_form = ReceiveForm()
    submit_form = SubmitForm()
    return render_template("index.html",
                           receive_form=receive_form,
                           submit_form=submit_form)

@app.route("/submit", methods=("POST", ))
def Submit_request():
    form = SubmitForm()
    if form.validate_on_submit():
        title = form.title.data
        address = form.address.data
        appType = form.application_Type.data
        
        url = "http://192.168.50.4:5000/BGREST/api/data"
        payload = json.dumps({'title': title, 'address': address, 'type': appType})
        headers = {'content-type': 'application/json'}
        r = requests.post(url, data=payload, headers=headers)
        flash(r.text)
        flash(r.status_code)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

@app.route("/retrieve", methods=("POST", "GET"))
def Retrieve_request():
    form = ReceiveForm()
    if form.validate_on_submit():
        itemid = form.item_id.data
        url = "http://192.168.50.4:5000/BGREST/api/data/"+itemid
        r = requests.get(url)        
        flash(r.text)
        flash(r.status_code)
        return redirect(url_for("index"))
    return render_template("validation_error.html", form=form)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
