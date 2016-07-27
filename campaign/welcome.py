HOST='box.halqaran.org'
PORT=587
USERNAME='welcome@halqaran.org'
PASSWORD='we/sharaf.143'
TLS=True
SSL=False
DEBUG=None

from sender import Mail, Message
import time

class Welcome():
    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.username = USERNAME
        self.password = PASSWORD
        self.tls = TLS
        self.ssl = SSL
        self.debug = DEBUG

    def send(self, to=[], subject='Subject', content='Welcome to Hal Qaran!', isHtml=False, cc='', bcc=[]):
        self.msg = Message(subject)
        self.msg.fromaddr = ("Hal Qaran", self.username)
        self.msg.to = to
        if isHtml==True:
            self.msg.body = ''
            self.msg.html = content
        else:
            self.msg.body = content
            self.msg.html = ''
        self.msg.cc = cc
        self.msg.bcc = bcc
        self.msg.reply_to = self.username
        self.msg.date = time.time()
        self.msg.charset = "utf-8"
        self.msg.extra_headers = {}
        self.msg.mail_options = []
        self.msg.rcpt_options = []
        if self.mail != None:
            self.mail.send(self.msg)
            return True
        else:
            return False

    def login(self):
        self.mail = Mail(self.host, port=self.port, username=self.username, password=self.password, use_tls=self.tls, use_ssl=self.ssl, debug_level=self.debug)
        return self.mail




