from .extensions import db, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f'<User: {self.username}>'

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    
#class Utenti(db.Model, UserMixin):
#   __tablename__ = 'Utenti'
#   
#   nomeUtente = db.Column(db.String(80), unique=True, nullable=False)
#   email = db.Column(db.String(120), primary_key=True)
#   password = db.Column(db.String(120), nullable=False)    
#
#   def __init__(self, nomeUtente, email, password):
#       self.nomeUtente = nomeUtente
#       self.email = email
#       self.password = generate_password_hash(password)
#
#   def __repr__(self):
#       return f'<Utente: {self.nomeUtente}>'
#
#   def verify_password(self, password):
#       return check_password_hash(self.password, password)
     
#class Questionari(db.Model, UserMixin):
#   __tablename__ = 'Questionari'
#   
#   idQuestionario = db.Column(db.Integer, primary_key=True)
#   nomeQuestionario = db.Column(db.String(120), nullable=False)
#   descrizione = db.Column(db.String(500), nullable=False)
#   creatore = db.Column(db.String(120), ForeignKey('Utenti.email'), nullable=False  )     
#   numeroSubmit = db.Column(db.Integer, default=0)
#
#   def __init__(self, nomeQuestionario, descrizione, creatore):
#       self.nomeQuestionario = nomeQuestionario
#       self.descrizione = descrizione
#       self.creatore = creatore


#class Domande(db.Model, UserMixin):
#   __tablename__ = 'Domande'
#   
#   idDomanda = db.Column(db.Integer, primary_key=True)
#   testoDomanda = db.Column(db.String(250), nullable=False)
#   categoria = db.Column(db.String(120), nullable=False)
#   idQuestionario = db.Column(db.Integer, ForeignKey('Questionario.idQuestionario'), nullable=False  )     
#   multipla = db.Column(db.bool)
#
#   def __init__(self, testoDomanda, categoria, idQuestionario, multipla):
#       self.testoDomanda = testoDomanda
#       self.categoria = categoria
#       self.idQuestionario = idQuestionario
#       self.multipla = multipla


#class Risposte(db.Model, UserMixin):
#   __tablename__ = 'Risposte'
#   
#   idRisposta = db.Column(db.Integer, primary_key=True)
#   testo = db.Column(db.String(250), nullable=False)
#   idDomanda = db.Column(db.Integer, ForeignKey('Domande.idDomanda'), nullable=False  )     
#   domandaSucc = db.Column(db.Integer, ForeignKey('Domande.idDomanda')  )     
#   nRisposte = dbColumn(db.Integer, default=0 )
#
#   def __init__(self, testo, idDomanda, domandaSucc):
#       self.testo = testo
#       self.idDomanda = idDomanda
#       self.domandaSucc = domandaSucc
        
