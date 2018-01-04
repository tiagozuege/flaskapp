class Contato(object):
    """docstring for Contato."""

    def __init__(self, nome, email, msg):    
        super(Contato, self).__init__()
        self.nome = nome
        self.email = email
        self.msg = msg

    def setNome(self, nome):
        self.nome = nome


    def getNome(self):
        return self.nome


    def setEmail(self, email):
        self.email = email


    def getEmail(self):
        return self.email


    def setMsg(self, msg):
        self.msg = msg


    def getMsg(self):
        return self.msg