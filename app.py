from flask import Flask, render_template, flash, request,  redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import datetime
# 创建Flask对象app
app = Flask(__name__)
# 人为入栈,解决上下文冲突
ctx = app.app_context()
ctx.push()
# 引入数据库配置文件settings.py
app.config.from_pyfile('settings.py')
# 创建数据库对象db
db = SQLAlchemy(app)

'''
定义Expense类继承自db.Model类
此类用于在数据库charity中创建expense表,用于存储慈善机构的开支详情
表头包括:id,program,admin,fundraising,
其中id为主键,用于唯一标识开支关系的元组，其会随着开支关系的添加而自增
'''


class Expense(db.Model):
    # 定义表名
    __tablename__ = 'expense'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 定义主键,自增
    program = db.Column(db.Integer, unique=False)
    admin = db.Column(db.Integer, unique=False)
    fundraising = db.Column(db.Integer, unique=False)


class Category(db.Model):
    # 定义表名
    __tablename__ = 'category'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, unique=True)
    category_name = db.Column(db.String(255), unique=True)


class Charity(db.Model):
    # 定义表名
    __tablename__ = 'charity'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    charity_id = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32), unique=False)
    category_id = db.Column(db.Integer, unique=False)
    name = db.Column(db.String(255), unique=True)
    address = db.Column(db.String(255), unique=True)  # 此属性不允许重复
    city = db.Column(db.String(32), unique=False)
    state = db.Column(db.String(32), unique=False, nullable=True)  # 此属性允许为空
    telephone = db.Column(db.String(32), unique=True)
    revenue = db.Column(db.Integer, unique=False)
    zip = db.Column(db.String(32), unique=False)
    expense_id = db.Column(db.Integer, db.ForeignKey(
        'expense.id'), unique=False)  # 定义外键,expense_id为expense表的主键
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.category_id'), unique=False)  # 定义外键,category_id为category表的主键
    # 通过expenses获取到以expense_id为主键的expense表的元组
    expenses = db.relationship('Expense', backref='charity')
    category = db.relationship('Category', backref='charity')


class Donor(db.Model):
    # 定义表名
    __tablename__ = 'donor'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.String(32),  unique=True)
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
    category = db.Column(db.String(32), unique=False)
    gift_donors = db.relationship('Donor', backref='gift')
    gift_charities = db.relationship('Charity', backref='gift')


class Log(db.Model):
    # 定义表名
    __tablename__ = 'log'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    log_id = db.Column(db.String(255), unique=False)
    operation_table = db.Column(db.String(255), unique=False, nullable=True)
    operation_name = db.Column(db.String(255), unique=False)
    operation_tuple = db.Column(db.String(255), unique=False, nullable=True)
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
            log = Log(log_id=account, operation_name="登录",
                      log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
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
        elif len(account) != 3:
            flash('账号长度必须为3位!!!')
        elif len(zipCode) != 5:
            flash('邮编长度必须为5位!!!')
        elif len(telphone) != 10:
            flash('电话号码必须是10位!!!')
        elif phone:
            flash('电话号码已被注册使用!!!')
        else:
            donor = Donor(donor_id=account, password=password2, last_name=last_name, first_name=first_name,
                          address=street, city=city, state=state, zip=zipCode, telephone=telphone)
            db.session.add(donor)
            db.session.commit()

            curr_time = datetime.datetime.now()
            log = Log(log_id=account, operation_table='donor', operation_name="添加", operation_tuple=account,
                      log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
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
        telphone1 = request.form.get('telphone1')
        telphone2 = request.form.get('telphone2')
        telphone3 = request.form.get('telphone3')
        telphone = telphone1+'-'+telphone2+'-'+telphone3
        state = request.form.get('state')
        city = request.form.get('city')
        street = request.form.get('street')
        revenue = request.form.get('revenue')
        program = request.form.get('program')
        admin = request.form.get('admin')
        fundraising = request.form.get('fundraising')
        zip = request.form.get('zip')
        _name = Charity.query.filter_by(name=name).first()
        id = Charity.query.filter_by(charity_id=account).first()
        _telphone = Charity.query.filter_by(telephone=telphone).first()
        _category = Category.query.filter_by(category_name=category).first()
        if not all([account, password, password2, name, category, [telphone1, telphone2, telphone3], state,
                    city, street, revenue, program, admin, fundraising]):
            flash('填入信息不完整!!!')
        elif password != password2:
            flash('两次输入密码不一致！！！')
        elif id:
            flash('账号已存在!!!')
        elif _name:
            flash('机构名称已被注册!!!')
        elif len(account) != 4:
            flash('账号长度必须为4位!!!')
        elif len(telphone) != 12:
            flash('电话号码必须是10位数字!!!')
        elif _telphone:
            flash('电话号码已被注册使用!!!')
        else:
            try:
                expense = Expense(program=program, admin=admin,
                                  fundraising=fundraising)
                db.session.add(expense)
                db.session.commit()
            except Exception as e:
                print(e)
                flash("开销项填入数据错误！！！")
                db.session.rollback()

            try:
                if not _category:
                    _category = Category(category_id=1+Category.query.order_by(desc(Category.id)).first().category_id,
                                         category_name=category)
                    db.session.add(_category)
                    db.session.commit()
            except Exception as e:
                print(e)
                flash("填入数据错误！！！")
                db.session.rollback()

            charity = Charity(charity_id=account, password=password2, category_id=_category.category_id,
                              name=name, address=street, city=city, state=state, telephone=telphone,
                              revenue=revenue, expense_id=expense.id, zip=zip)
            db.session.add(charity)
            db.session.commit()

            curr_time = datetime.datetime.now()
            log = Log(log_id=account, operation_table='charity', operation_name="添加", operation_tuple=account,
                      log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('signUpCharity.html')


'''
通过app对象的route函数解析到/homePage路由, 提供get和post两种请求方式。
此页面用于呈现用户登录后显示的内容, 包括查询和捐赠功能
本页面根据homePage页面不同的input表单控件获取到的值作出不同的事件响应
'''


@app.route('/homePage.html', methods=['GET', 'POST'])
def homePage():
    # 通过SQLAlchemy提供的查询函数进行数据库数据查询
    # 查询donor表全部数据
    donors = Donor.query.all()
    # 查询charity表全部数据并按照revenue降序返回
    charities = Charity.query.order_by(
        desc(Charity.revenue))
    # 查询gift表全部数据并按amount降序返回
    gifts = Gift.query.order_by(desc(Gift.amount))
    # 获取log表的按时间降序排列后的第一个元组
    logID = Log.query.order_by(
        desc(Log.log_time)).first()
    # 获取donor表中donor_id为当前登录id的元组
    donor = Donor.query.filter_by(donor_id=logID.log_id).first()
    # 获取charity表中charity_id为当前登录id的元组
    charity = Charity.query.filter_by(charity_id=logID.log_id).first()

    # 此处定义homePage页面显示与否判断的bool变量
    displayCharity = False
    displayDonor = False
    displayGift = False
    displayCategory = False
    displayCheckDonor = False
    displayGiver = False
    # 此处用于定义homePage页面查询需要用到变量
    gift = ''
    logName = ""
    giftDonate = ''
    donorName = ''
    realname = ''
    anonymous = ''
    categoryName = ''
    charityName = ''
    checkCharity = ''
    Giver = []
    checkDonor = []
    categoryName_Charity = []
    # 判断登录用户类别,并查询登录的用户名
    if donor:
        logName = donor.last_name+donor.first_name
    elif charity:
        logName = charity.name
    # 如果homePage页面进行了查询,则执行下面的代码
    if request.method == 'POST':
        # 根据homePage页面定义的input表单name名获取到对应的值
        changeInfo = request.form.get('changeInfo')
        deleteItem = request.form.get('deleteItem')
        logout = request.form.get('logout')
        CPE = request.form.get('charity')
        DRC = request.form.get('donor')
        MG = request.form.get('gift')
        categoryName = request.form.get('categoryName')
        category = Category.query.filter_by(
            category_name=categoryName).first()
        charityName = request.form.get('charityName')
        checkCharity = Charity.query.filter_by(name=charityName).first()
        last_name = request.form.get('donorName1')
        first_name = request.form.get('donorName2')
        charityID = request.form.get('charityID')
        donorID = request.form.get('donorID')
        donateType = request.form.get('donateType')
        donateAmount = request.form.get('donateAmount')
        realname = request.form.get('realname')
        anonymous = request.form.get('anonymous')
        donateDonor = Donor.query.filter_by(donor_id=donorID).first()
        donateCharity = Charity.query.filter_by(charity_id=charityID).first()
        # 如果last_name，first_name都不为空，则将其拼接成donorName
        if all([last_name, first_name]):
            donorName = last_name+first_name

        # 如果用户点击了退出登录按钮，则直接返回主页面
        if logout:
            # 重定向到index路由
            return redirect(url_for('index'))
        # 如果用户点击了修改信息按钮，则返回注册界面
        elif changeInfo:
            # 获取系统当前时间
            curr_time = datetime.datetime.now()
            log = ''
            # 在log表中记录相应操作
            if donor:
                db.session.delete(donor)
                log = Log(log_id=logID.log_id,  operation_table='donor',
                          operation_name="修改", operation_tuple=logID.log_id,
                          log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            elif charity:
                db.session.delete(charity)
                log = Log(log_id=logID.log_id,  operation_table='charity',
                          operation_name="修改", operation_tuple=logID.log_id,
                          log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()
            if donor:
                return redirect(url_for('signUpDonor'))
            elif charity:
                return redirect(url_for('signUpCharity'))
        # 如果用户点击了注销账号按钮，则从数据库中删除该元组并返回注册页面
        elif deleteItem:
            curr_time = datetime.datetime.now()
            log = ''
            # 在log表中记录相应操作
            if donor:
                db.session.delete(donor)
                log = Log(log_id=logID.log_id,  operation_table='donor',
                          operation_name="删除", operation_tuple=logID.log_id,
                          log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            elif charity:
                db.session.delete(charity)
                log = Log(log_id=logID.log_id,  operation_table='charity',
                          operation_name="删除", operation_tuple=logID.log_id,
                          log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
            db.session.add(log)
            db.session.commit()
            return redirect(url_for('index'))
        # 如果用户点击了自定义查询的按钮
        elif CPE:
            displayCharity = not displayCharity
        elif DRC:
            displayDonor = not displayDonor
        elif MG:
            displayGift = not displayGift
        # 如果用户点击了自定义查询中的查询类别名按钮
        elif categoryName:
            if category:
                categoryName_Charity = Charity.query.filter_by(
                    category_id=category.category_id)
                gift = Gift.query.filter_by(
                    category=categoryName).all()
                displayCategory = True
            else:
                flash("当前尚无"+categoryName+"类别慈善机构!!!")
        # 如果用户点击了自定义查询中的查询慈善机构按钮
        elif charityName:
            if checkCharity:
                Giver = Gift.query.filter(
                    Gift.gift_charities.has(name=charityName)).all()
                displayGiver = True
            else:
                flash("当前尚无名为"+charityName+"的慈善机构!!!")
        # 如果用户点击了自定义查询中的查询捐赠者按钮
        elif donorName:
            if not all([last_name, first_name]):
                flash("请填入完整姓氏和姓名!!!")
            else:
                aimedDonor = Donor.query.filter_by(
                    last_name=last_name, first_name=first_name).first()
                if aimedDonor:
                    checkDonor = Gift.query.filter_by(
                        gift_donor=aimedDonor.donor_id).all()
                if checkDonor:
                    displayCheckDonor = True
                else:
                    flash("当前尚无名为"+donorName+"的捐赠者!!!")
        # 如果用户点击了捐赠按钮
        elif donorID:
            if not donateDonor:
                flash("只有注册为捐赠者才可以进行捐赠哦！")
            elif not donateCharity:
                flash("该慈善机构ID并不存在!")
            else:
                curr_time = datetime.datetime.now()
                if realname:
                    giftDonate = Gift(gift_name=donateType, gift_donor=donorID, gift_charity=charityID,
                                      category=donateCharity.category.category_name,
                                      date=datetime.datetime.strftime(
                                          curr_time, '%Y-%m-%d %H:%M:%S'),
                                      amount=donateAmount)
                elif anonymous:
                    anonymousID = Donor.query.filter_by(
                        donor_id="anonymous").first()
                    donateAmount = int(1.5*int(donateAmount))
                    giftDonate = Gift(gift_name=donateType, gift_donor=anonymousID.donor_id, gift_charity=charityID,
                                      category=donateCharity.category.category_name,
                                      date=datetime.datetime.strftime(
                                          curr_time, '%Y-%m-%d %H:%M:%S'),
                                      amount=donateAmount)
                log = Log(log_id=donorID, operation_table='gift', operation_name="添加", operation_tuple=Gift.query.count()+1,
                          log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
                db.session.add_all([log, giftDonate])
                db.session.commit()
        elif not (categoryName or charityName or donorName):
            flash("请在自定义查询框中输入数据先哦！")
    # 当用户访问到该路由(/homePage)则返回homePage.index文件,并返回下面的参数
    return render_template('homePage.html',  logID=logID, logName=logName,
                           donors=donors, charities=charities, gifts=gifts,
                           displayCharity=displayCharity, displayDonor=displayDonor, displayGift=displayGift,
                           categoryName=categoryName, categoryName_Charity=categoryName_Charity, displayCategory=displayCategory,
                           gifted_donors=gift, displayGiver=displayGiver, Giver=Giver, checkCharity=checkCharity,
                           displayCheckDonor=displayCheckDonor, donorName=donorName, checkDonor=checkDonor,
                           giftDonate=giftDonate, realname=realname, anonymous=anonymous)


if __name__ == '__main__':
    # 先清楚数据库中全部表
    db.drop_all()
    # 创建所有上面的定义的表
    db.create_all()
    # 创建expense元组e1,e2,e3
    e1 = Expense(program=50000, admin=10000, fundraising=500000)
    e2 = Expense(program=300000, admin=10000, fundraising=540000)
    e3 = Expense(program=50000, admin=200000, fundraising=500000)
    db.session.add_all([e1, e2, e3])
    db.session.commit()
    # 创建category表元组category1,category2,category3
    category1 = Category(category_id=11, category_name="动物保护")
    category2 = Category(category_id=12, category_name="环境保护")
    category3 = Category(category_id=13, category_name="儿童保护")
    db.session.add_all([category1, category2, category3])
    db.session.commit()
    # 创建charity表元组c1,c2,c3
    c1 = Charity(charity_id="c001", password="c000001", category_id=category1.category_id, name="关爱动物中心", address="深圳南山区xxxx",
                 city="深圳", state="广东", telephone="400-0987-1234", revenue=1000000, expense_id=e1.id, zip=10000)
    c2 = Charity(charity_id="c002", password="c000002", category_id=category2.category_id, name="保护环境协会", address="广州增城区xxxx",
                 city="广州", state="广东", telephone="400-5678-1234", revenue=500000, expense_id=e2.id, zip=10001)
    c3 = Charity(charity_id="c003", password="c000003", category_id=category3.category_id, name="关爱儿童协会", address="东莞中唐镇xxxx",
                 city="东莞", state="广东", telephone="400-3678-1234", revenue=20000000, expense_id=e3.id, zip=10002)
    db.session.add_all([c1, c2, c3])
    db.session.commit()
    # 创建donor表元组d1,d2,d3
    d1 = Donor(donor_id="d01", password="d000001", last_name="欧阳", first_name="致远",
               address="中山市xxxx", city="中山", state="广东", zip="xxxxxx", telephone="12345678900")
    d2 = Donor(donor_id="d02", password="d000002", last_name="公孙", first_name="向阳",
               address="惠州市xxxx", city="惠州", state="广东", zip="xxxxxx", telephone="00987654321")
    d3 = Donor(donor_id="anonymous", password="anonymous", last_name="匿名者", first_name="anonymous",
               address="暂无数据", city="暂无数据", state="暂无数据", zip="暂无数据", telephone="暂无数据")
    db.session.add_all([d1, d2, d3])
    db.session.commit()
    # 创建gift元组g1,g2,g3
    curr_time = datetime.datetime.now()
    g1 = Gift(gift_name="现金", gift_donor=d1.donor_id, gift_charity=c3.charity_id,
              category=c3.category.category_name, date=datetime.datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'),
              amount=150)
    g2 = Gift(gift_name="现金", gift_donor=d2.donor_id, gift_charity=c1.charity_id,
              category=c1.category.category_name, date=datetime.datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'), amount=1000)
    g3 = Gift(gift_name="现金", gift_donor=d2.donor_id, gift_charity=c2.charity_id,
              category=c2.category.category_name, date=datetime.datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'), amount=500)
    db.session.add_all([g1, g2, g3])
    db.session.commit()
    # 创建log表元组log1,log2,log3
    curr_time = datetime.datetime.now()
    log1 = Log(log_id=c1.charity_id, operation_table='charity', operation_name="添加",
               operation_tuple=c1.charity_id, log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log2 = Log(log_id=c2.charity_id,  operation_table='charity', operation_name="添加",
               operation_tuple=c2.charity_id, log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log3 = Log(log_id=c3.charity_id,  operation_table='charity', operation_name="添加",
               operation_tuple=c3.charity_id, log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log4 = Log(log_id=d1.donor_id,  operation_table='donor', operation_name="添加",
               operation_tuple=d1.donor_id, log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log5 = Log(log_id=d2.donor_id,  operation_table='donor', operation_name="添加",
               operation_tuple=d2.donor_id, log_time=datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    db.session.add_all([log1, log2, log3, log4, log5])
    db.session.commit()
    # db.drop_all()  # 用于演示时清空数据库表内容
    # 开启调试
    app.run(debug=True)
