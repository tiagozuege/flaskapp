from models.contato import Contato
from flask_mysqldb import MySQL

mysql = MySQL(app=None)

class ContatoDAO(object):


    """Data Access Object for Contato."""

    def __init__(self):
        super(ContatoDAO, self).__init__()

    def insert(self, contato):
        c = contato
        ret = 0

        try:
            # Start sql transaction
            cur = mysql.connection.cursor()
            sql_str = "INSERT INTO contatos VALUES ( %i, '%s', '%s', '%s')"
            params = (0, c.getNome(), c.getEmail(), c.getMsg())
            print(sql_str % params)
            cur.execute(sql_str % params)
            mysql.connection.commit()
            cur.close()
            # End sql transaction
        except:
            ret = -1

        return ret