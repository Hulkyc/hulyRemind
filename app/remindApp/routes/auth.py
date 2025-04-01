# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : auth.py
# @Time    : 2025/3/15 11:17
from flask import Blueprint, request, jsonify
import requests
from ..models import User, Item
from ..extensions import db
from ..utils.auth import generate_token, optimized_generator, hash_password, decode_token

auth_bp = Blueprint('auth', __name__)


# 登录接口
@auth_bp.route('user/login', methods=['POST'])
def user_login():
    code = request.json.get('code')
    if not code:
        return jsonify({'code': 400, 'msg': '缺少code参数'}), 400
    # return jsonify({'code': 400, 'msg': '缺少code参数'}),400

    # # 调用微信接口
    # wx_url = f"https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}"
    # response = requests.get(wx_url)
    # wx_data = response.json()
    #
    # 获取或创建用户
    user = User.query.filter_by(nickname=request.json.get('nickname')).first()
    if not user:
        return jsonify({'code': 400, 'data': "用户未注册"})
    elif not user.verify_password(request.json.get('password')):
        return jsonify({'code': 400, 'data': "校验失败"})
    # 生成JWT

    token = generate_token(user.id)
    userid = decode_token(token)["user_id"]
    return jsonify({'code': 200,
                    'data': {'token': token},
                    'user_id': userid})


# 用户注册接口
@auth_bp.route('/user/create', methods=['POST'])
def user_create():
    user = User.query.filter_by(nickname=request.json.get('nickname')).first()
    if not user:
        id = optimized_generator()
        nickname = request.json.get('nickname')
        password_hash = hash_password(request.json.get('password'))
        user = User(id=id, openid=id, nickname=nickname,
                    password_hash=password_hash)
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': 200, 'data': "注册成功", 'message': "注册成功"})
        except Exception as e:
            e = str(e)
            return jsonify({'code': 400, 'data': {}, 'message': "出现错误:" + e})
    else:
        return jsonify({'code': 400, 'data': {}, 'message': "用户已存在"})


@auth_bp.route('/', methods=['GET'])
def test01():
    return jsonify({'code': 400, 'msg': '缺少code参数'})
