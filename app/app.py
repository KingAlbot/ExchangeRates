import os
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

service_startdate = "start date"

db = SQLAlchemy(app)
migrate = Migrate(app, db)



class exchange_rates(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    base = db.Column(db.String(3))
    currency = db.Column(db.String(3))
    currency_value = db.Column(db.Float)

    def __repr__(self):
        return self.date


@app.route("/api/v1/<string:date>/<string:currency>")
def get_exchange_rates(date, currency):

    try:
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return {'error':'wrong date format must be yyyy-mm-dd'}, 404

    currencies = ["USD", "EUR", "RUB", "CNY"]
    if currency not in currencies:
        return {'error':f'no exchange rates for this currency, available exchange rates: {",".join(currencies)}'}, 404


    exchange_rates_query = exchange_rates.query.filter_by(date=date).filter_by(base=currency)

    if exchange_rates_query.first() is None:
        return {'error':'no entry found. Service started: ' + service_startdate}

    response = dict()
    response["base"] = currency
    response["date"] = date
    for i in exchange_rates_query:
        response[i.currency] = i.currency_value

     

    return response

@app.errorhandler(404)
def page_not_found(error):
     return "<h1>Error 404. Page not found.</h1>", 404


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=80)

