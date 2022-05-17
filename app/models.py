from dataclasses import dataclass
from app import db


class User(db.Model):
    
    __tablename__ = 'user'
    
    id = db.Column(db.String(256),
                   primary_key = True)
    
    username = db.Column(db.String(64),
                         unique = True,
                         nullable = False)
    
    email = db.Column(db.String(120),
                      unique = True,
                      nullable = False)
    
    password = db.Column(db.String(256),
                         nullable = False)
    
                         
    def __init__(self, id: str, username: str, email: str, password: str) -> None:
        
        
        self.id = id
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self) -> str:
        
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def __str__(self) -> str:
        return super().__str__()
    
@dataclass
class Data(db.Model):
    
    __tablename__ = 'datas'
    
    id: str
    
    temp: float
    
    hum: float
    
    datetime: str
    
    id = db.Column(db.String(256),
                   primary_key = True)
    
    temp = db.Column(db.Float,
                     nullable = False)
    
    hum = db.Column(db.Float,
                    nullable = False)
    
    datetime = db.Column(db.DateTime,
                         nullable = False)
    
    def __init__(self, id: str, temp: float,
                 hum: float, datetime) -> None:
        
        self.id = id
                
        self.temp = temp 
        
        self.hum = hum
        
        self.datetime = datetime
    
    def __repr__(self):

        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))