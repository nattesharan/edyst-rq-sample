from flask import Flask,request,render_template,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from redis import Redis
from rq import Queue
app = Flask(__name__)
engine = create_engine('sqlite:///test.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
app.secret_key = 'TESTAPP'
q = Queue(connection=Redis())

def init_db():
    from models import *
    Base.metadata.create_all(bind=engine)

@app.route('/index',methods=['GET','POST'])
def submit_url():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method ==  'POST':
        from tasks import save_summary
        if request.form['url']:
            task = q.enqueue(save_summary, args=(request.form['url'],), result_ttl=5000)
            print task.get_id()
            flash('Success')
        else:
            flash('Please enter url')
        return render_template('form.html')
@app.route('/',methods=['GET'])
def get_summary():
    from models import summary
    summary_list = summary.query.all()
    return render_template('home.html',summary_list=summary_list)
if __name__  == '__main__':
    app.run(port=8080,debug=True)