# Exemplo de um web app que utiliza Flask

Este é um pequeno exemplo de um web app que utiliza o microframework Flask
com suporte a persistência de dados utilizando MySQL.


## Para executar o web app, faça o seguinte:


**Instalação das dependências (Debian-based OS):**

- `pip install flask` (ignore se já estiver instalado)
- `pip install flask_mysqldb`
- `sudo apt-get install mysql-server`       (opcional)
- `sudo apt-get install mysql-client`       (opcional)
- `sudo apt-get install libmysqlclient-dev` (opcional)

**Configuração da aplicação:**

- `git clone https://github.com/tiagozuege/flaskapp.git`
- `cd flaskapp`
- `export FLASK_APP=app.py`
- `export FLASK_DEBUG=1`
- `flask run`

A aplicação estará disponível através da URL *http://localhost:5000*
