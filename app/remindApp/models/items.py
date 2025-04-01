# @Version : 1.0
# @Author  : hu_ling_yi
# @File    : items.py
# @Time    : 2025/3/15 11:01
from datetime import datetime
from app.remindApp.extensions import db


class Item(db.Model):
    """物品模型"""
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)

    # 关系定义
    #images = db.relationship('ItemImage', backref='item', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at

        }


class ItemImage(db.Model):
    """物品图片"""
    __tablename__ = 'item_images'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    def to_dict(self):
        return {
            "id": self.id,
            "item_id": self.item_id,
            "image_url": self.image_url,
            "is_main": self.is_main

        }