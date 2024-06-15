# 初始化数据库
def init(db):

    from app.model import Category, Expense, Gift, Charity, Donor, Log
    from datetime import datetime

    # 先清除数据库中全部表
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
    curr_time = datetime.now()
    g1 = Gift(gift_name="现金", gift_donor=d1.donor_id, gift_charity=c3.charity_id,
              category=c3.category.category_name, date=datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'),
              amount=150)
    g2 = Gift(gift_name="现金", gift_donor=d2.donor_id, gift_charity=c1.charity_id,
              category=c1.category.category_name, date=datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'), amount=1000)
    g3 = Gift(gift_name="现金", gift_donor=d2.donor_id, gift_charity=c2.charity_id,
              category=c2.category.category_name, date=datetime.strftime(
                  curr_time, '%Y-%m-%d %H:%M:%S'), amount=500)
    db.session.add_all([g1, g2, g3])
    db.session.commit()
    # 创建log表元组log1,log2,log3
    curr_time = datetime.now()
    log1 = Log(log_id=c1.charity_id, operation_table='charity', operation_name="添加",
               operation_tuple=c1.charity_id, log_time=datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log2 = Log(log_id=c2.charity_id,  operation_table='charity', operation_name="添加",
               operation_tuple=c2.charity_id, log_time=datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log3 = Log(log_id=c3.charity_id,  operation_table='charity', operation_name="添加",
               operation_tuple=c3.charity_id, log_time=datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log4 = Log(log_id=d1.donor_id,  operation_table='donor', operation_name="添加",
               operation_tuple=d1.donor_id, log_time=datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    log5 = Log(log_id=d2.donor_id,  operation_table='donor', operation_name="添加",
               operation_tuple=d2.donor_id, log_time=datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S'))
    db.session.add_all([log1, log2, log3, log4, log5])
    db.session.commit()
    # db.drop_all()  # 用于演示时清空数据库表内容
