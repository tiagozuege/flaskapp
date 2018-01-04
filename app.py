from flask import Flask, redirect, render_template, request
from flask_mysqldb import MySQL
from datetime import date
from models.contato import Contato
from daos.contatodao import ContatoDAO
import time


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
    if request.args.get('update') != '0':
        update_id = request.args.get('update')
        update_article = fetchArticles(update_id)
    if request.method == 'POST':
        id = request.form['id']
        title = request.form['titulo']
        text = request.form['texto']
        if id == '':
            insertArticles(request.form['titulo'], request.form['texto'])
        else:
            updateArticles(id, title, text)
    articles = fetchArticles('0')
    return render_template('artigos.html', data=articles, update=update_article)


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

@app.route('/contato', methods=['POST', 'GET'])
def contato():
    msg = None
    if request.method == 'POST':
        print("***DEBUG: POST method coming to /contato")
        nome = request.form['nome']
        email = request.form['email']
        msgm = request.form['mensagem']
        msg = "Você acabou de enviar a sua mensagem. Em breve iremos lhe responder."
        contato = Contato(nome,email,msgm)
        contatoDao = ContatoDAO()
        ret = contatoDao.insert(contato)
        if ret == -1:
            msg = "Ops! Aconteceu um problema. Por favor tente novamente. Se o erro persistir, entre em conato com o suporte técnico."
    return render_template('contato.html', msg=msg)
    

def fetchArticles(id):
    cur = mysql.connection.cursor()
    if id == '0':
        cur.execute('''SELECT * FROM artigos''')
    else:
        cur.execute("SELECT * FROM artigos WHERE id = '%s'" % id)
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

def updateArticles(id, title, text):
    cur = mysql.connection.cursor()
    sql_str = "UPDATE artigos SET titulo = '%s', texto = '%s' WHERE id = %s"
    params = (title, text, id)
    print(sql_str % params)
    cur.execute(sql_str % params)
    mysql.connection.commit()
    cur.close()