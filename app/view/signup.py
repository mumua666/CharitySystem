from datetime import datetime
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import desc
from app import db, app
from app.model import Category, Expense, Charity, Donor, Log


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
