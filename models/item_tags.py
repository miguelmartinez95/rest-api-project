from db import db


class ItemTags(db.Model):
    __tablename__ = "item_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.item_id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id"))

