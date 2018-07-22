from app import db_session
import requests
from models import summary 

def save_summary(url):
    resp = requests.get(url)
    word_count = len(resp.text.split())
    data = summary(url,word_count)
    db_session.add(data)
    db_session.commit()
