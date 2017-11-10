from flask import Flask, render_template, request
from dataset import getData

data = getData()


app = Flask(__name__)

def check_paramaters(parameters):
    if parameters == 'ok':
        print('yes, the parameter its correct!')
    else:
        print('oh no, invalid parameter!')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/teste', methods=['POST', 'GET'])
def teste():
    if request.method == 'POST':
        print('Here was a post')
        print(request.form['teste'])                    #Imprime os dados que vieram pelo POST
        check_paramaters(request.form['teste'])
    return render_template('teste.html', data = data)
