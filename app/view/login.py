from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from app import db, app
from app.model import Log, Charity, Donor, LogIn


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        p1 = " "
        p2 = " "
        flag1 = Charity.query.filter_by(charity_id=account).first()
        if flag1:
            p1 = flag1.password
        flag2 = Donor.query.filter_by(donor_id=account).first()
        if flag2:
            p2 = flag2.password
        if not all([account, password]):
            flash('账号或密码输入不全！！！')
        elif not (flag1 or flag2):
            flash("不存在此账号!!!")
        elif not (p1 == password or p2 == password):
            flash("密码错误!!!")
        else:
            curr_time = datetime.datetime.now()
            log = Log(log_id=account, operation_name="登录",
                      log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            logIn = LogIn(log_id=account, log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add_all([log, logIn])
            db.session.commit()
            return redirect(url_for('homePage'))

    return render_template('index.html')
