# coding: utf8
"""
Define the Tasks Model
"""


from app.extensions import db
from app.models.abc import BaseModel, MetaBaseModel


class Tasks(db.BaseModel, BaseModel, metaclass=MetaBaseModel):
    """Customer Model"""

    __tablename__ = "tasks"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), index=False, unique=False, nullable=True)

    def __init__(self, **kwargs):
        """ Create a new task """
        self.task = kwargs.get("task") or None

