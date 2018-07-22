from flask import Flask,request,render_template,flash
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
from rq.job import Job
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'TESTAPP'
db = SQLAlchemy(app)
conn = Redis()
q = Queue(connection=conn)
@app.route('/index',methods=['GET','POST'])
def submit_url():
    if request.method == 'GET':
        return render_template('form.html')
    if request.method ==  'POST':
        from tasks import save_summary
        if request.form['url']:
            task = q.enqueue(save_summary, args=(request.form['url'],), result_ttl=86400)
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

@app.route('/job/<job_key>', methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)
    print job.is_finished
    if job.is_finished:
        return str(job.result), 200
    else:
        return "Failed", 202

if __name__  == '__main__':
    app.run(port=8080,debug=True)