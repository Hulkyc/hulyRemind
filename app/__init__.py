# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : __init__.py.py
# @Time    : 2025/3/15 10:35
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.models import Category

# 初始化扩展  //使用全局初始化的对象
# db = SQLAlchemy()
# migrate = Migrate()
from app.extensions import db, migrate


def create_app(config_name='dev'):
    app = Flask(__name__)

    # 加载配置
    from config.dev import DevelopmentConfig
    app.config.from_object(DevelopmentConfig)

    # 初始化的扩展绑定应用
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图前导入模型，确保迁移检测到所有模型
    from .models.user import User
    from .models.items import Item
    from .models.category import Category

    # 注册蓝图
    from .routes.auth import auth_bp
    from .routes.items import items_bp
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(items_bp, url_prefix='/api')

    # 创建上传目录
    upload_dir = app.config['UPLOAD_FOLDER']
    upload_dir.mkdir(parents=True, exist_ok=True)

    return app
