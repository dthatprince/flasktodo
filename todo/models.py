from db import db
from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

class Todo(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(250), nullable=False)
    desc: Mapped[str] = mapped_column(db.Text, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "desc": self.desc, "status": self.status}