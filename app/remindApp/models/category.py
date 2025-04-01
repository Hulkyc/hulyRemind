# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : category.py.py
# @Time    : 2025/3/15 11:19
from app.remindApp.extensions import db


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    parent_id = db.Column(db.Integer, default=0)
    level = db.Column(db.SmallInteger, default=1)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id,
            'level': self.level,
            'children': []
        }
