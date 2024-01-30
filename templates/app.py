from flask import Flask, render_template
from predictions import get_predictions
from retriveve_conditions import run_above_functions_and_return_prediction_inputs, rand_num
import datetime

app = Flask(__name__)


@app.route('/')
def home():

    time = str((datetime.datetime.now() - datetime.timedelta(hours=5)))[:-7]
    predict_17hr, predict_15hr, predict_8hr, predict_4hr = get_predictions()
    return render_template('app.html',rand = rand_num, inputs = run_above_functions_and_return_prediction_inputs(), time = time, value1 = predict_17hr, value2 = predict_15hr, value3 = predict_8hr, \
                           value4 = predict_4hr)


if __name__ == '__main__':
    app.run()
