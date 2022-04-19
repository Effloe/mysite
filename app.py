from flask import Flask, redirect, url_for, render_template, request, session, flash
from dbutils import DBUtils
from datetime import datetime
from utils import require_login, get_page
from werkzeug.utils import secure_filename
from compute import Calculate_percentage
import math
import os
import time

app=Flask(__name__)
db = DBUtils()

BASEDIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_PATH = os.path.join(BASEDIR, 'static/upload')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'bmp'])
app.config["SECRET_KEY"] = 'adfklajsda9d87fqorow7r1902387132j'

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        sql = "select * from user where username='" + username + "' and password='" + password + "'"
        try:
            results = db.query(sql)
            if len(results) == 1:
                session['username'] = username
                return redirect(url_for('index', flag=True))
            else:
                flash('username and password not matched！', 'danger')
                return redirect(url_for('login'))
        except Exception as e:
            print('exception - {}'.format(str(e)))
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['repeat-password']

        if password != password2:
            flash('Two password not matched!', 'danger')
            return redirect(url_for('register'))
        querysql = "select * from user where username='" + username + "'"
        sql = "INSERT INTO user (username, password) VALUES ('" + username + "', '" + password + "')"
        try:
            results = db.query(querysql)
            if len(results) == 1:
                flash('Username exists alreay, please input another one！', 'danger')
                return redirect(url_for('register'))
            else:
                db.execute(sql)
                session['username'] = username
                return redirect(url_for('index'))
        except Exception as e:
            print('exception - {}'.format(str(e)))
            return redirect(url_for('register'))
    else:
        return render_template('register.html')


@app.route('/logout')
@require_login
def logout():
    session.clear()
    flash('Logout, welcome login again！', 'success')
    return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@require_login
def index():
    imgname = ''
    if request.method == 'POST':
        filepath = ''
        f = request.files['image']
        if f and allowed_file(f.filename):
            imgname = secure_filename(f.filename)
            filepath = os.path.join(UPLOAD_PATH, imgname)
            print('filepath:{}'.format(filepath))
            f.save(filepath)
    return render_template('index.html', imgname=imgname)

@app.route('/analysis', methods=['GET', 'POST'])
@require_login
def analysis():
    start_dt = time.time()
    imgname = request.form.get('imgname')
    imgpath = os.path.join(UPLOAD_PATH, imgname)
    result = Calculate_percentage(imgpath)
    end_dt = time.time()
    calctime =  round(end_dt - start_dt, 4)
    create_dt = datetime.now()
    sql = "INSERT INTO history (imgname, calctime, result, create_dt) VALUES ('{}',{},'{}','{}')".format(imgname, calctime, result, create_dt)
    db.execute(sql)
    return render_template('index.html', imgname=imgname, calctime=calctime, result = result)

@app.route('/history', defaults={'page':1})
@app.route('/history/<page>')
@require_login
def history(page):
    datas={}
    perpage = 10
    page = int(page)
    startat = (page-1) * perpage
    show_shouye_status = 0
    if page > 1:
        show_shouye_status = 1

    allsql = 'SELECT count(*) FROM history'
    sql = "select * from history limit {}, {}".format(startat, perpage)
    historys = db.query(allsql)
    total_items = historys[0][0]
    total_pages = int(math.ceil(total_items / perpage))
    print('total_items {} -  total_pages {} '.format(total_items,total_pages))
    dic = get_page(total_pages, page)
    datas = {
                'page': page,
                'total': total_pages,
                'perpage': perpage,
                'show_shouye_status': show_shouye_status,
                'dic_list': dic
                }
    results = db.query(sql)
    return render_template('history.html', results = results, datas = datas)

@app.route('/delete/<id>')
@require_login
def delete(id):
    sql = "DELETE FROM history WHERE id = {}".format(id)
    db.execute(sql)
    flash('The record is deleted successfully!', 'success')
    return redirect(url_for('history'))
if __name__ == '__main__':
    app.run(port=5000)