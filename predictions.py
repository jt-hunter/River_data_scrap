import tensorflow as tf
import numpy as np

# get inputs from other script
from retriveve_conditions import prediction_inputs

# func to get predict output to string
def predict_to_string(predict):
    predict = str(predict[0][0])[:4]
    return predict

# load model and get prediction from inputs
def get_predictions():
    predict_17hr = predict_to_string(tf.keras.models.load_model('Models/model_17hrs.h5')\
                                     .predict(prediction_inputs[0].astype(float).reshape(1,4)))
    predict_15hr = predict_to_string(tf.keras.models.load_model('Models/model_15hrs.h5')\
                                     .predict(prediction_inputs[1].astype(float).reshape(1,2)))
    predict_8hr = predict_to_string(tf.keras.models.load_model('Models/model_8hrs.h5')\
                                    .predict(prediction_inputs[2].astype(float).reshape(1,3)))
    predict_4hr = predict_to_string(tf.keras.models.load_model('Models/model_4hrs.h5')\
                                    .predict(prediction_inputs[3].astype(float).reshape(1,4)))
    return predict_17hr, predict_15hr, predict_8hr, predict_4hr
