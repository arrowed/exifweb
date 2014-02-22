from flask import Flask, Response, abort, flash, redirect, render_template, request, url_for

import redis_helper as redis_conn

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True
app.config['red'] = redis_conn
app.secret_key = 'asdfasdfasdir0945ph;oososhkj'



@app.route('/')
def index():
    return render_template('main.html', next=url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
def add_folder():
    if request.form['directory']:

        directory = request.form['directory']
        jobs = redis_conn._add_job_to_queue('jobs', directory )
        flash('Added directory %s to the processing queue, you are %s in line' % (directory, find_nth(jobs)),
              'alert-success')

    if request.form['next']:
        return redirect(request.form['next'])

    return render_template('main.html', next=url_for('index'))


def find_nth(number):
    '''Borrowed from http://codegolf.stackexchange.com/a/4712'''

    k = number % 10
    return "%d%s"% (number,"tsnrhtdd"[(number/10%10!=1)*(k<4)*k::4])

if __name__ == '__main__':
    app.run()

