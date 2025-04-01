# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : sql_test.py
# @Time    : 2025/3/15 16:34
# 创建新用户
from flask import Flask, current_app
from app.models.user import User
from app.extensions import db



with app.app_context():
    new_user = User(id="001", openid="openid", nickname='123456')
    db.session.add(new_user)
    db.session.commit()
