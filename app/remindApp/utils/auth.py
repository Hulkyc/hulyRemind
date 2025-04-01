# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : auth.py
# @Time    : 2025/3/15 11:52
from datetime import datetime, timedelta
import random

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from app.remindApp.models import User
from itertools import permutations

# 预生成所有可能的4位不重复数字
all_valid_numbers = [int(''.join(p)) for p in permutations('0123456789', 4) if p[0] != '0']
random.shuffle(all_valid_numbers)


def optimized_generator():
    """生成userid"""
    return all_valid_numbers.pop()


def generate_token(user_id, expires_in=6):
    """生成JWT令牌"""
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(hours=6)
    }
    return jwt.encode(
        payload,
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )


def decode_token(token):
    """解析验证JWT令牌"""
    try:
        payload = jwt.decode(
            token,
            current_app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None  # 令牌过期
    except jwt.InvalidTokenError:
        return None  # 无效令牌


def hash_password(password):
    """生成密码哈希"""
    return generate_password_hash(password)


def verify_password(password_hash, password):
    """验证密码"""
    return check_password_hash(password_hash, password)


def get_current_user(token):
    """通过令牌获取用户对象"""
    if not token:
        return None
    payload = decode_token(token)
    if not payload:
        return None
    return User.query.get(payload['user_id'])
