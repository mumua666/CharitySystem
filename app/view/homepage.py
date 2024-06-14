from datetime import datetime, time
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import desc
from app import db, app
from app.model import Donor, Charity, Gift, Log, LogIn, Category


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
    LogInID = LogIn.query.order_by(desc(LogIn.log_time)).first()

    logTime = ""
    if LogInID:
        logTime = time.strptime(LogInID.log_time, '%Y-%m-%d %H:%M:%S')
    if not LogInID or time.mktime(datetime.datetime.now().timetuple())-time.mktime(logTime) > 500:
        return redirect(url_for("index"))

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
            LogInID = False
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
