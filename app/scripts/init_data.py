# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : init_data.py.py
# @Time    : 2025/3/15 12:03
from app.remindApp import create_app
from app.remindApp.models import Category
from app.remindApp import db

app = create_app()

with app.app_context():
    # 初始化分类数据
    main_categories = [
        {'name': '食品', 'children': ['主食', '零食']},
        {'name': '个护', 'children': ['水乳', '洗面奶']}
    ]

    for main in main_categories:
        parent = Category(name=main['name'], level=1)
        db.session.add(parent)
        db.session.flush()

        for sub_name in main['children']:
            child = Category(
                name=sub_name,
                parent_id=parent.id,
                level=2
            )
            db.session.add(child)

    db.session.commit()
    print("分类数据初始化完成！")