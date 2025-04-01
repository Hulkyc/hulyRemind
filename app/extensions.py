# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : extensions.py
# @Time    : 2025/3/15 10:46
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化扩展对象（尚未绑定应用）
db = SQLAlchemy()        # 数据库ORM
migrate = Migrate()      # 数据库迁移
