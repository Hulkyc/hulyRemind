# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : items.py
# @Time    : 2025/3/15 10:59
import os
import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from app.config.dev import Config
from app.remindApp.models import Item, Category, ItemImage
from ..utils.auth import get_current_user, optimized_generator, decode_token
from ..extensions import db

items_bp = Blueprint('items', __name__)


# 通过token获取用户id
def get_userid_by_token(token):
    token = token.split(" ")[1] if len(token.split(" ")) > 1 else None
    if token:
        user_id = decode_token(token)
        if user_id is None:
            return {'code': 400, 'data': "操作失败", 'message': "token失效"}
        else:
            user_id = user_id['user_id']
            return user_id
    else:
        return {'code': 400, 'data': "操作失败", 'message': "token用户缺失"}


# 查询物品接口
@items_bp.route('/items/search', methods=['post'])
def items_search():
    category_id = request.json.get('category_id')
    token = request.headers['Authorization']
    user_id = get_userid_by_token(token)
    if not isinstance(user_id, int):
        return user_id
    items = Item.query.filter_by(category_id=category_id, user_id=user_id).all()
    for i in items:
        print(i.to_dict())
    return jsonify({"code": 200,
                    "message": "success",
                    "data": [item.to_dict() for item in items]})


# 新建物品接口
@items_bp.route('/items/create', methods=['POST'])
def items_create():
    token = request.headers['Authorization']
    id = optimized_generator()
    user_id = get_userid_by_token(token)
    if not isinstance(user_id, int):
        return user_id
    category_id = request.json.get('category_id')
    name = request.json.get('name')
    description = request.json.get('description')
    item = Item(id=id,
                user_id=user_id,
                category_id=category_id,
                name=name,
                description=description)
    image = ItemImage(id=optimized_generator(),
                      item_id=id,
                      image_url="static/uploads/default-item.png")
    try:
        db.session.add(item)
        db.session.add(image)
        db.session.commit()
        return jsonify({'code': 200, 'data': "创建成功", 'message': "注册成功"})
    except Exception as e:
        e = str(e)
        return jsonify({'code': 400, 'data': {}, 'message': "出现错误:" + e})


# 修改物品接口
@items_bp.route('/items/update', methods=['POST'])
def items_update():
    token = request.headers['Authorization']
    user_id = get_userid_by_token(token)
    if not isinstance(user_id, int):
        return user_id
    id = request.json.get('id')
    item = Item.query.filter_by(id=id, user_id=user_id).first()
    if item is None:
        return jsonify({"code": 404, "message": "物品不存在"})
    data = request.get_json()
    if 'name' in data and len(data['name']) > 0:
        item.name = data['name']

    if 'description' in data:
        item.description = data['description']

    if 'category_id' in data:
        if not Category.query.get(data['category_id']):
            return jsonify({"code": 400, "message": "无效分类ID"}), 400
        item.category_id = data['category_id']
    try:
        db.session.commit()
        return jsonify({
            "code": 200,
            "message": "修改成功",
            "data": item.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": f"保存失败: {str(e)}"}), 500


# 删除物品接口
@items_bp.route('/item/delete', methods=['post'])
def items_delete():
    id = request.headers.get('id')
    token = request.headers['Authorization']
    user_id = get_userid_by_token(token)
    if not isinstance(user_id, int):
        return user_id
    name = request.json.get('name')
    item = Item.query.filter_by(id=id, user_id=user_id, name=name).all()

    if not item:
        return jsonify({'code': 404, 'data': "删除失败", 'message': "物品不存在"})
    for i in item:
        try:
            db.session.delete(i)
            db.session.commit()
            return jsonify({'code': 200, 'data': "删除成功", 'message': "删除成功"})
        except Exception as e:
            db.session.rollback()
            e = str(e)
            print(e)
            return jsonify({'code': 500, 'data': {}, 'message': "出现错误:" + e})


@items_bp.route('/items/create', methods=['POST'])
def create_item():
    # 1. 获取当前用户
    user = get_current_user(request.json.get['token'])  # 需要实现用户验证

    # 2. 接收参数
    data = request.form
    category_id = data.get('category_id')

    # 3. 验证分类是否存在
    if not Category.query.get(category_id):
        return {'error': '无效分类'}, 400

    # 4. 创建物品记录
    new_item = Item(
        user_id=user.id,
        category_id=category_id,
        name=data['name']
    )
    db.session.add(new_item)
    db.session.commit()

    return {'id': new_item.id}, 201


# 获取物品分类信息
@items_bp.route('/items/categories', methods=['GET'])
def get_items_categories():
    category_id = request.args.get('category_id')
    main_id = request.args.get('main_id')
    if not (category_id and main_id):
        categories_main = Category.query.filter_by(parent_id=0).all()
        i = 0
        parent_list = []
        while i < len(categories_main):
            parent_list.append(categories_main[i].to_dict())
            categories_sub = Category.query.filter_by(parent_id=categories_main[i].id).all()
            for j in categories_sub:
                parent_list[i]['children'].append(j.to_dict())
            i += 1

        return jsonify({"code": 200,
                        "message": "success",
                        "data": parent_list
                        })

    categories_main = Category.query.filter_by(id=main_id).all()
    i = 0
    parent_list = []
    while i < len(categories_main):
        parent_list.append(categories_main[i].to_dict())
        categories_sub = Category.query.filter_by(parent_id=categories_main[i].id, id=category_id).all()
        for j in categories_sub:
            parent_list[i]['children'].append(j.to_dict())
        i += 1

    return jsonify({"code": 200,
                    "message": "success",
                    "data": parent_list})


# 上传物品图片


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def generate_safe_filename(filename):
    """生成安全的存储路径"""
    # 按日期分目录：uploads/2023/08/23
    date_str = datetime.now().strftime("%Y/%m/%d")
    save_dir = os.path.join(Config.UPLOAD_FOLDER, date_str)
    # 创建目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)
    # 生成唯一文件名：3e7b4a5c6d7e8f9a0b1c2d3e4f5a6b7c8.jpg
    ext = filename.rsplit('.', 1)[1].lower()
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    # 返回相对路径和绝对路径
    relative_path = os.path.join(date_str, unique_name)
    absolute_path = os.path.join(save_dir, unique_name)
    return relative_path, absolute_path


@items_bp.route('/items/image', methods=['post'])
def upload_item_image():
    # 验证文件存在
    if 'file' not in request.files:
        return jsonify({'code': 400, 'message': '未选择文件'})
    file = request.files['file']
    item_id = request.form.get('item_id')

    # 验证文件名
    if file.filename == '':
        return jsonify({'code': 400, 'message': '无效文件名'})
    # 验证文件类型
    if not allowed_file(file.filename):
        return jsonify({'code': 400, 'message': '不支持的文件类型'})
    try:
        # 生成安全文件名
        original_filename = secure_filename(file.filename)  # 消毒原始文件名
        relative_path, absolute_path = generate_safe_filename(original_filename)

        # 更新数据库
        item = Item.query.get(item_id)
        if item:
            image = ItemImage.query.filter_by(item_id=item_id, is_main=1).first()
            print(image.to_dict())
            image.image_url = relative_path  # 存储相对路径
            print(relative_path)
            db.session.commit()
            # 保存文件
            file.save(absolute_path)

        # 返回访问URL
        # image_url = f"{current_app.config['BASE_URL']}/{Config.UPLOAD_FOLDER}/{relative_path}"
        return jsonify({
            'code': 200,
            'data': {
                # 'url': image_url,
                'path': relative_path
            },
            'message': '上传成功'
        })

    except Exception as e:
        print(str(e))
        return jsonify({'code': 500, 'message': '文件上传失败'})
