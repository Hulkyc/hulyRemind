# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : response.py.py
# @Time    : 2025/3/15 11:47
from flask import jsonify

def success(data=None):
    return jsonify({
        'code': 200,
        'data': data
    })

def error(msg, code=400):
    return jsonify({
        'code': code,
        'msg': msg
    }), code