from flask import Flask, request
import db
import datetime
from random import randint

app = Flask(__name__)

HUMIDITY_MIN = 53
HUMIDITY_MAX = 58

humidity = 10


@app.route('/', methods=['GET'])
def main_page():
    return 'This is the main page' #+ str(STORE['humidity'])


@app.route('/delete_db', methods=['GET'])
def delete_db():
    db.deleteAll()
    return 'OK'


@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    data = db.getStoredData()
    temperature = [x[1] for x in data]

    return ' '.join(str(x) for x in temperature)

@app.route('/get_humidity', methods=['GET'])
def get_humidity():
    data = db.getStoredData()
    humidity = [x[2] for x in data]

    return ' '.join(str(x) for x in humidity)


@app.route('/get_light', methods=['GET'])
def get_light():
    data = db.getStoredData()
    light = [x[0] for x in data]

    return ' '.join(str(x) for x in light)


@app.route('/get_flow_rate', methods=['GET', 'POST'])
def get_flow_rate():
    data = request.get_data()
    temperature, hum, light, time  = data.split()

    now = datetime.datetime.now()
    time = now.hour

    humidity = hum

    db.storeData(temperature, humidity, light, time)
    data = db.getStoredData()

    return calculate_waterflow(data, humidity)


def calculate_waterflow(data, humidity):
    global HUMIDITY_MIN
    global HUMIDITY_MAX

    # light = [x[2] for x in data]
    # temperature = [x[0] for x in data]
    # hum = humidity
    # time = [x[3] for x in data]
    print(humidity)
    if int(humidity) < 10:
        result = 100
        return str(result)
    elif int(humidity) < 20:
        result = 80
        return str(result)

    elif int(humidity) < 25:
        result = 60
        return str(result)
    elif int(humidity) < 35:
        result = 40
        return str(result)
    elif int(humidity) < 40:
        result = 20
        return str(result)
    else:
        return '0'


if __name__ == '__main__':
    app.run()
