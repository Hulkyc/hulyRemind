# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : run.py.py
# @Time    : 2025/3/15 10:11
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    # print(app.config['SQLALCHEMY_DATABASE_URI'])