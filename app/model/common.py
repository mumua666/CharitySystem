from app import db


# 慈善机构开销表
class Expense(db.Model):
    # 定义表名
    __tablename__ = 'expense'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 定义主键,自增
    program = db.Column(db.Integer, unique=False)
    admin = db.Column(db.Integer, unique=False)
    fundraising = db.Column(db.Integer, unique=False)


# 捐赠物品类别表
class Category(db.Model):
    # 定义表名
    __tablename__ = 'category'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, unique=True)
    category_name = db.Column(db.String(255), unique=True)


# 捐赠物品表
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
