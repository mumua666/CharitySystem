from app import db


# 慈善机构表
class Charity(db.Model):
    # 定义表名
    __tablename__ = 'charity'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    charity_id = db.Column(db.String(32), unique=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(32), unique=False)

    address = db.Column(db.String(255), unique=True)  # 此属性不允许重复
    city = db.Column(db.String(32), unique=False)
    state = db.Column(db.String(32), unique=False, nullable=True)  # 此属性允许为空
    telephone = db.Column(db.String(32), unique=True)
    revenue = db.Column(db.Integer, unique=False)
    zip = db.Column(db.String(32), unique=False)

    # 定义外键,expense_id为expense表的主键
    expense_id = db.Column(db.Integer, db.ForeignKey(
        'expense.id'), unique=False)
    # 定义外键,category_id为category表的主键
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.category_id'), unique=False)
    # 通过expenses获取到以expense_id为主键的expense表的元组
    expenses = db.relationship('Expense', backref='charity')
    category = db.relationship('Category', backref='charity')


# 捐赠者表
class Donor(db.Model):
    # 定义表名
    __tablename__ = 'donor'
    # 定义列对象
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.String(32),  unique=True)
    last_name = db.Column(db.String(32), unique=False)
    first_name = db.Column(db.String(32), unique=False)
    password = db.Column(db.String(32), unique=False)

    address = db.Column(db.String(32), unique=False)
    city = db.Column(db.String(32), unique=False)
    state = db.Column(db.String(32), unique=False)
    zip = db.Column(db.String(32), unique=False)
    telephone = db.Column(db.String(32), unique=True)
