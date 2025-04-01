# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : image.py.py
# @Time    : 2025/3/15 11:48
import os
from werkzeug.utils import secure_filename
from flask import current_app


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def save_image(file):
    if not allowed_file(file.filename):
        raise ValueError('不支持的文件类型')

    filename = secure_filename(file.filename)
    save_dir = current_app.config['UPLOAD_FOLDER']

    # 生成唯一文件名
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(save_dir, filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1

    # 保存文件
    file.save(os.path.join(save_dir, filename))
    return f"/static/uploads/{filename}"