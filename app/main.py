# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : main.py.py
# @Time    : 2025/3/15 10:11
import os

from app.remindApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    # print(remindApp.config['SQLALCHEMY_DATABASE_URI'])
    # (debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 80))