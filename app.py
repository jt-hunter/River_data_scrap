from flask import Flask, render_template
import datetime
from predictions import get_predictions

app = Flask(__name__)


@app.route('/')
def home():
    predict_17hr, predict_15hr, predict_8hr, predict_4hr = get_predictions()
    time = str(datetime.datetime.now()
    return render_template('app.html', time = time, value1 = predict_17hr, value2 = predict_15hr, value3 = predict_8hr, \
                           value4 = predict_4hr)


if __name__ == '__main__':
    app.run()
