from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
from dataset import getData, getArtigos

data = getData()
articles = getArtigos()

app = Flask(__name__)

# Config MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Init MySQL

mysql = MySQL(app)


def checkLogin(param, param2):
    ok = False
    if param == 'admin' and param2 == 'senha':
        print('Login aceito!')
        ok = True
    else:
        print('Login recusado! Cheque os seus dados.')
        ok = False
    return ok



# Teste para verificar parametros de request

def check_paramaters(parameters):
    if parameters == 'ok':
        print('yes, the parameter its correct!')
    else:
        print('oh no, invalid parameter!')


# Rotas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        login_ok = checkLogin(request.form['usr'], request.form['pwd'])
        if login_ok:
            return redirect('/')
        else:
            error = "Login recusado. Tente novamente, ou entre em contato com o administrador."
    return render_template('login.html', error=error)


@app.route('/artigos', methods=['POST', 'GET'])
def artigos():
    if request.method == 'POST':
        print('Here was a post')
    return render_template('artigos.html', artigos = articles)



@app.route('/artigo/<string:id>')
def artigo(id):
    return render_template('artigo.html', id=id)


# Teste para verificar parametros enviados por POST
@app.route('/teste', methods=['POST', 'GET'])
def teste():
    if request.method == 'POST':
        print('Here was a post')
        print(request.form['teste'])                    #Imprime os dados que vieram pelo POST
        check_paramaters(request.form['teste'])
    return render_template('teste.html', data = data)

# Teste Mysql

@app.route('/teste-mysql')
def teste2():
    l = []
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM usuarios''')
    data = cur.fetchall()
    #return data
    return render_template('teste-mysql.html', data=data)


# Exemplo de insert
'''
cur = mysql.connection.cursor()
cur.execute('INSERT INTO... VALUES (%s, %s, %s)', (data1, d2, d3))

mysql.connection.commit()

cur.close()
'''

