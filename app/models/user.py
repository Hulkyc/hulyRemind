# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : user.py
# @Time    : 2025/3/15 11:12
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(50), unique=True, nullable=False)
    nickname = db.Column(db.String(50))
    password_hash = db.Column(db.String(256), default="123344")
    created_at = db.Column(db.DateTime, default=datetime.now())

    items = db.relationship('Item', backref='user', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        """自动生成密码哈希"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
