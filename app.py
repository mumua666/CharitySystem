from flask import Flask, render_template, flash, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import datetime

app = Flask(__name__)
# 选择人为入栈。
ctx = app.app_context()
ctx.push()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Linux_Mumu@localhost/charity'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = 'Linux_Mumu'
# app.secret_key = 'Linux_Mumu'
app.config.from_pyfile('settings.py')

db = SQLAlchemy(app)


class Expense(db.Model):
    # 定义表名
    __tablename__ = 'expense'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    program = db.Column(db.Integer, unique=False)
    admin = db.Column(db.Integer, unique=False)
    fundraising = db.Column(db.Integer, unique=False)


class Charity(db.Model):
    # 定义表名
    __tablename__ = 'charity'
    # 定义列对象
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    charity_id = db.Column(db.String(32), primary_key=True, unique=True)
    password = db.Column(db.String(32), unique=False)
    category = db.Column(db.String(32), unique=False)
    name = db.Column(db.String(32), unique=True)
    address = db.Column(db.String(32), unique=True)
    city = db.Column(db.String(32), unique=False)
    state = db.Column(db.String(32), unique=False, nullable=True)
    telephone = db.Column(db.String(32), unique=True)
    revenue = db.Column(db.Integer, unique=False)
    expense = db.Column(db.Integer, db.ForeignKey(
        'expense.id'), unique=False)
    expenses = db.relationship('Expense', backref='charity')


class Donor(db.Model):
    # 定义表名
    __tablename__ = 'donor'
    # 定义列对象
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.String(32), primary_key=True, unique=True)
    password = db.Column(db.String(32), unique=False)
    last_name = db.Column(db.String(32), unique=False)
    first_name = db.Column(db.String(32), unique=False)
    address = db.Column(db.String(32), unique=False)
    city = db.Column(db.String(32), unique=False)
    state = db.Column(db.String(32), unique=False)
    zip = db.Column(db.String(32), unique=False)
    telephone = db.Column(db.String(32), unique=True)


class Gift(db.Model):
    # 定义表名
    __tablename__ = 'gift'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gift_name = db.Column(db.String(32), unique=False)
    gift_donor = db.Column(db.String(32), db.ForeignKey(
        'donor.donor_id'), unique=False)
    gift_charity = db.Column(db.String(32), db.ForeignKey(
        'charity.charity_id'), unique=False)
    date = db.Column(db.String(32), unique=False)
    amount = db.Column(db.Integer, unique=False)
    gift_donors = db.relationship('Donor', backref='gift')
    gift_charities = db.relationship('Charity', backref='gift')


class Log(db.Model):
    # 定义表名
    __tablename__ = 'log'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(32), unique=False)
    operation = db.Column(db.String(255), unique=False)
    log_time = db.Column(db.String(255), unique=False)


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
            log = Log(log_id=account, operation="登录", log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('homePage'))

    return render_template('index.html')


@app.route('/signUp.html', methods=['GET', 'POST'])
def signUp():
    return render_template('signUp.html')


@app.route('/signUpDonor.html', methods=['GET', 'POST'])
def signUpDonor():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        last_name = request.form.get('last_name')
        first_name = request.form.get('first_name')
        telphone = request.form.get('telphone')
        state = request.form.get('state')
        city = request.form.get('city')
        street = request.form.get('street')
        zipCode = request.form.get('zipCode')
        id = Donor.query.filter_by(donor_id=account).first()
        phone = Donor.query.filter_by(telephone=telphone).first()
        if not all([account, password, password2, last_name, first_name, telphone, state, city, street, zipCode]):
            flash('填入信息不完整!!!')
        elif password != password2:
            flash('两次输入密码不一致！！！')
        elif id:
            flash('账号已存在!!!')
        elif len(account) != 7:
            flash('账号长度必须为7位!!!')
        elif len(zipCode) != 6:
            flash('邮编长度必须为6位!!!')
        elif len(telphone) != 11:
            flash('电话号码必须是11位!!!')
        elif phone:
            flash('电话号码已被注册使用!!!')
        else:
            donor = Donor(donor_id=account, password=password2, last_name=last_name, first_name=first_name,
                          address=street, city=city, state=state, zip=zipCode, telephone=telphone)
            db.session.add(donor)
            db.session.commit()

            curr_time = datetime.datetime.now()
            log = Log(log_id=account, operation="注册", log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('signUpDonor.html')


@app.route('/signUpCharity.html', methods=['GET', 'POST'])
def signUpCharity():
    if request.method == 'POST':
        account = request.form.get('account')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        name = request.form.get('name')
        category = request.form.get('category')
        telphone = request.form.get('telphone')
        state = request.form.get('state')
        city = request.form.get('city')
        street = request.form.get('street')
        revenue = request.form.get('revenue')
        program = request.form.get('program')
        admin = request.form.get('admin')
        fundraising = request.form.get('fundraising')
        _name = Charity.query.filter_by(name=name).first()
        id = Charity.query.filter_by(charity_id=account).first()
        _telphone = Charity.query.filter_by(telephone=telphone).first()
        if not all([account, password, password2, name, category, telphone, state, city, street, revenue, program, admin, fundraising]):
            flash('填入信息不完整!!!')
        elif password != password2:
            flash('两次输入密码不一致！！！')
        elif id:
            flash('账号已存在!!!')
        elif _name:
            flash('机构名称已被注册!!!')
        elif len(account) != 7:
            flash('账号长度必须为7位!!!')
        elif len(telphone) != 11:
            flash('电话号码必须是11位数字!!!')
        elif _telphone:
            flash('电话号码已被注册使用!!!')
        else:
            try:
                expense = Expense(program=program, admin=admin,
                                  fundraising=fundraising)
                db.session.add(expense)
                db.session.commit()
            except:
                flash("开销项填入数据错误！！！")

            try:
                charity = Charity(charity_id=account, password=password2, category=category, name=name, address=street, city=city,
                                  state=state, telephone=telphone, revenue=revenue, expense=expense.id)
                db.session.add(charity)
                db.session.commit()
            except:
                flash("填入数据错误！！！")

            curr_time = datetime.datetime.now()
            log = Log(log_id=account, operation="注册", log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('signUpCharity.html')


@app.route('/homePage.html', methods=['GET', 'POST'])
def homePage():
    donors = Donor.query.all()
    charities = Charity.query.order_by(desc(Charity.revenue))
    gifts = Gift.query.all()
    logID = Log.query.order_by(desc(Log.log_time)).first()
    donor = Donor.query.filter_by(donor_id=logID.log_id).first()
    charity = Charity.query.filter_by(charity_id=logID.log_id).first()
    logName = ""
    displayCharity = False
    displayDonor = False
    displayGift = False
    if donor:
        logName = donor.last_name+donor.first_name
    elif charity:
        logName = charity.name
    if request.method == 'POST':

        changeInfo = request.form.get('changeInfo')
        deleteItem = request.form.get('deleteItem')
        CPE = request.form.get('CPE')
        DRC = request.form.get('DRC')
        MG = request.form.get('MG')
        if CPE:
            displayCharity = not displayCharity
        if DRC:
            displayDonor = not displayDonor
        if MG:
            displayGift = not displayGift
        if changeInfo:
            if donor:
                db.session.delete(donor)
                db.session.commit()
            elif charity:
                db.session.delete(charity)
                db.session.commit()
            curr_time = datetime.datetime.now()
            log = Log(log_id=logID.log_id, operation="修改", log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()
            if donor:
                return redirect(url_for('signUpDonor'))
            elif charity:
                return redirect(url_for('signUpCharity'))
        elif deleteItem:
            if donor:
                db.session.delete(donor)
                db.session.commit()
            elif charity:
                db.session.delete(charity)
                db.session.commit()
            curr_time = datetime.datetime.now()
            log = Log(log_id=logID.log_id, operation="删除", log_time=datetime.datetime.strftime(
                curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('homePage.html', donors=donors, charities=charities, gifts=gifts, logID=logID.log_id, logName=logName,
                           displayCharity=displayCharity, displayDonor=displayDonor, displayGift=displayGift)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    e1 = Expense(program=50000, admin=10000, fundraising=500000)
    e2 = Expense(program=300000, admin=10000, fundraising=540000)
    e3 = Expense(program=50000, admin=200000, fundraising=500000)
    db.session.add_all([e1, e2, e3])
    db.session.commit()

    c1 = Charity(charity_id="c000001", password="c000001", category="动物保护", name="关爱动物中心", address="深圳南山区xxxx", city="深圳",
                 state="广东", telephone="400-0987-1234", revenue=1000000, expense=e1.id)
    c2 = Charity(charity_id="c000002", password="c000002", category="环境保护", name="保护环境协会", address="广州增城区xxxx", city="广州",
                 state="广东", telephone="400-5678-1234", revenue=500000, expense=e2.id)
    c3 = Charity(charity_id="c000003", password="c000003", category="儿童保护", name="关爱儿童协会", address="东莞中唐镇xxxx", city="东莞",
                 state="广东", telephone="400-3678-1234", revenue=20000000, expense=e3.id)
    db.session.add_all([c1, c2, c3])
    db.session.commit()

    d1 = Donor(donor_id="d000001", password="d000001", last_name="欧阳", first_name="致远",
               address="中山市xxxx", city="中山", state="广东", zip="xxxxxx", telephone="12345678900")
    d2 = Donor(donor_id="d000002", password="d000002", last_name="公孙", first_name="向阳",
               address="惠州市xxxx", city="惠州", state="广东", zip="xxxxxx", telephone="00987654321")
    db.session.add_all([d1, d2])
    db.session.commit()

    curr_time = datetime.datetime.now()
    g1 = Gift(gift_name="衣物", gift_donor=d1.donor_id, gift_charity=c3.charity_id, date=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'), amount=5)
    g2 = Gift(gift_name="狗狗小屋", gift_donor=d2.donor_id, gift_charity=c1.charity_id, date=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'), amount=1)
    g3 = Gift(gift_name="现金", gift_donor=d2.donor_id, gift_charity=c2.charity_id, date=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'), amount=500)
    db.session.add_all([g1, g2, g3])
    db.session.commit()

    curr_time = datetime.datetime.now()
    log1 = Log(log_id=c1.charity_id, operation="注册", log_time=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'))
    log2 = Log(log_id=c2.charity_id, operation="注册", log_time=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'))
    log3 = Log(log_id=c3.charity_id, operation="注册", log_time=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'))
    log4 = Log(log_id=d1.donor_id, operation="注册", log_time=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'))
    log5 = Log(log_id=d2.donor_id, operation="注册", log_time=datetime.datetime.strftime(
        curr_time, '%Y-%m-%d %H:%M:%S'))
    db.session.add_all([log1, log2, log3, log4, log5])
    db.session.commit()

    # db.drop_all()
    app.run(debug=True)
