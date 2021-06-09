#import Flask 
from flask import Flask, jsonify
import numpy as np
from tensorflow import keras
import json
from urllib.request import urlopen

#create an instance of Flask
app = Flask(__name__)

def preprocessDataAndPredict(temp, humid, rain, wind):
    #put all inputs in array
    test_data = np.array([[temp, humid, rain, wind]], dtype=np.float32)
    model = keras.models.load_model("banjir_model.h5")
    #predict
    prediction = model.predict(test_data)
    return prediction
    pass

url = 'https://api.openweathermap.org/data/2.5/onecall?lat=-6.2146&lon=106.8451&exclude=current,minutely,hourly&units=metric&appid=fc6243945d988df193f40812f9d2408e'
    
response = urlopen(url)
    
data_json = json.loads(response.read())
    
today = data_json['daily'][0]
temp = today['temp']
    
average_temp = (temp['day'] + temp['eve'] + temp['morn'] + temp['night']) / 4
humidity = today['humidity']
rain = today['rain']
wind = today['wind_speed']
dt = today['dt']

prediction = preprocessDataAndPredict(average_temp, humidity, rain, wind)[0][0] * 100
hasil = "{:.1f}".format(prediction)
    
data_libas = [
    {'id': 0,
     'datetime' : dt,
     'temp': average_temp,
     'humidity': humidity,
     'rain': rain,
     'wind': wind,
     'predict' : hasil}
]

@app.route('/predict/', methods=['GET'])
def predict():
    return jsonify(data_libas)
    

if __name__ == '__main__':
    app.run(debug=True)