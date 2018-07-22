from app import db

class summary(db.Model):
    id = db.Column('id', db.Integer, primary_key = True)
    url = db.Column(db.String(100))
    word_count = db.Column(db.Integer())
    def __init__(self,url,word_count):
        self.url = url
        self.word_count = word_count