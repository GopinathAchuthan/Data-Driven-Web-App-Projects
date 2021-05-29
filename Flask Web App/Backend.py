# run this file using the command "python path_to_Backend.py"

import pickle
import pandas as pd 

from flask import Flask
from flask import redirect, url_for, abort, request, escape, make_response
app = Flask(__name__)


filename = 'finalized_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

df_description = pd.read_csv('symptom_Description.csv')
df_precaution = pd.read_csv('symptom_precaution.csv')

@app.route('/search', methods=['GET'])
def search():
    if request.method == 'GET':
        data = request.json['data']
        desc = df_description[df_description.Disease == data].values[0][1]
        prec = df_precaution[df_precaution.Disease == data].values[0][1:]
        list_prec = '<ul>'
        for value in prec:
            list_prec += '<li>{value}</li>'.format(value=value)
        list_prec += '</ul>'
        return {'msg': data, 'description':desc, 'precaution':list_prec}
    else: abort(405)
        

# root path
@app.route('/model', methods=['POST'])
def data():
    if request.method == 'POST':
        pred = loaded_model.predict(request.json['data'])
        return {'msg': list(pred)}
    else: abort(405)
    

# error path
@app.errorhandler(405)
def malformed_query(error):
    """
    Redirects 405 errors
    """
    resp = make_response("Malformed Query")
    return resp


if __name__ == '__main__':
   app.run(host='127.0.0.1', port=8001, debug=False)