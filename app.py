from flask import Flask, jsonify
import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from datetime import datetime
from sqlalchemy import Boolean, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_migrate import Migrate

from flask_restful import Resource, Api
import json

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
api = Api(app)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to-do-app.db"
# initialize the app with the extension
db.init_app(app)

# Initialize Flask-Migrate 
migrate = Migrate(app, db)

# Data Model for Users
class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}
    
    def __repr__(self):
        return f"<User {self.username}>"
    
# Data Model for Tasks
class Todo(db.Model):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(db.String(250), nullable=False)
    description: Mapped[str] = mapped_column(db.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    status: Mapped[bool] = mapped_column(Boolean, default=False)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", back_populates="tasks")
    
    def to_dict(self):
        return {"id": self.id, "title": self.title, "desc": self.description, 
                "description": self.description, "created_at": self.created_at,
                 "due_date": self.due_date, "user.id": self.user_id, "status": self.status}

    def __repr__(self):
        return f"<Task {self.title}>"




class TodosApi(Resource):
    def get(self):
        todos = Todo.query.all()
        
        temp =[]
        for todo in todos:
            temp.append({"id": todo.id, "title": todo.title, "desc": todo.desc})
        print(temp)
        jsonify_todos = jsonify(temp)
    
        return jsonify_todos
    
    
class TodoApi(Resource):
    def get(self, todo_id):
        todo = Todo.query.get_or_404(todo_id)
        return {"id": todo.id, "title": todo.title, "desc": todo.desc}
    
    
api.add_resource(TodosApi, '/')
api.add_resource(TodoApi, '/<int:todo_id>')




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)