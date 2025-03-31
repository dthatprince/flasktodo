from flask import Blueprint, jsonify
from flask_restful import Api, Resource
from todo.models import Todo



todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')

api = Api(todo_blueprint)


class TodosApi(Resource):
    def get(self):
        todos = Todo.query.all()

        temp = []
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

