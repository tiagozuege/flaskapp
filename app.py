from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
#from dataset import getData, getArtigos
from datetime import date
import time 

# data = getData()
#articles = getArtigos()

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
        print('POST comming from /artigos')
        insertArticles(request.form['titulo'], request.form['texto'])
    articles = fetchArticles('0')
    return render_template('artigos.html', data=articles)


@app.route('/artigo/<string:id>')
def artigo(id):
    article = fetchArticles(id)
    return render_template('artigo.html', data=article)


@app.route('/artigo/<string:id>/remove')
def artigoRemove(id):
    error = None
    removeArticles(id)
    print('The article id %s was removed' % id)
    return redirect('/artigos')

    #article = fetchArticles(id)
    #return render_template('artigo.html', data=article)



# Teste para verificar parametros enviados por POST
@app.route('/teste', methods=['POST', 'GET'])
def teste():
    if request.method == 'POST':
        print('Here was a post')
        print(request.form['teste'])                    #Imprime os dados que vieram pelo POST
        check_paramaters(request.form['teste'])
    return render_template('teste.html', data=data)

# Teste Mysql

@app.route('/teste-mysql')
def teste2():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM usuarios''')
    data = cur.fetchall()
    cur.close()
    #return data
    return render_template('teste-mysql.html', data=data)

def fetchArticles(id):
    cur = mysql.connection.cursor()
    if id == '0':
        cur.execute('''SELECT * FROM artigos''')
    else:
        cur.execute('''SELECT * FROM artigos WHERE id = %s''', id)
    data = cur.fetchall()
    cur.close()
    return data

def insertArticles(title, text):

    # Get current time before insert
    d = time.strftime('%d')
    m = time.strftime('%m')
    y = time.strftime('%Y')
    dt = y+'-'+m+'-'+d
    
    # Start sql transaction
    cur = mysql.connection.cursor()
    sql_str = "INSERT INTO artigos VALUES ( %i, '%s', '%s', %i, '%s')"
    params = (0, title, text, 1, dt)
    print(sql_str % params)
    cur.execute(sql_str % params)
    mysql.connection.commit()
    cur.close()

    # End sql transaction

def removeArticles(id):
    cur = mysql.connection.cursor()
    sql_str = "DELETE FROM artigos WHERE id = %s"
    print(sql_str % id)
    cur.execute(sql_str % id)
    mysql.connection.commit()
    cur.close()