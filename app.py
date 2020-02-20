import redis
from flask import Flask, render_template, request

app = Flask(__name__)
redisClient = redis.Redis(host='redis', port=6379)            

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/confirmation', methods=['POST'])
def submit():
	if request.method == 'POST':
		voter = request.form['voter'].upper()
		MVP = request.form['MVP']
		OPOY = request.form['OPOY']
		DPOY = request.form['DPOY']
		OROY = request.form['OROY']
		DROY = request.form['DROY']
		if voter == '' or MVP == '' or OPOY == '' or DPOY == '' or OROY == '' or DROY == '':
			return render_template('error.html')
	redisClient.hmset(voter, {"MVP":MVP, "OPOY":OPOY, "DPOY":DPOY, "OROY":OROY, "DROY":DROY})
	return render_template('confirmation.html')

@app.route('/submissions')
def viewsubmissions():
    return render_template('submissions.html')

@app.route('/results', methods=['POST'])
def search():
	if request.method == 'POST':
		search = request.form['searchname'].upper()
		if search == '' or redisClient.hget(search, "MVP") is None:
			return render_template('searcherror.html')
	return render_template('searchresults.html', voter=search, MVP=redisClient.hget(search, "MVP").decode('utf-8'), OPOY=redisClient.hget(search, "OPOY").decode('utf-8'), DPOY=redisClient.hget(search, "DPOY").decode('utf-8'), OROY=redisClient.hget(search, "OROY").decode('utf-8'), DROY=redisClient.hget(search, "DROY").decode('utf-8'))
