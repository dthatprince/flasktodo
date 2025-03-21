from flask import Flask, jsonify
import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
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

class Todo(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(db.String(250), nullable=False)
    desc: Mapped[str] = mapped_column(db.Text, nullable=False)





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