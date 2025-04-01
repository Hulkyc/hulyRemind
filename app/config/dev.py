# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : dev.py.py
# @Time    : 2025/3/15 10:11
import os
from pathlib import Path


class Config:
    # 基础配置
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = ('mysql+pymysql://root:h112233@192.168.2.106:3306/test_sql')

    # # 微信配置
    # WX_APPID = 'your-wechat-appid'
    # WX_SECRET = 'your-wechat-secret'

    # 文件上传
    UPLOAD_FOLDER = Path(__file__).parent.parent / 'static/uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB


class DevelopmentConfig(Config):
    DEBUG = True


if __name__ == "__main__":
    DevelopmentConfig()
