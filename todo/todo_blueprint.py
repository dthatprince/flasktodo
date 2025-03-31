from flask import Blueprint, jsonify
from flask_restful import Api, Resource

from error_handler import InvalidAPIUsage
from todo.models import Todo



todo_blueprint = Blueprint('todo', __name__, url_prefix='/todo')

api = Api(todo_blueprint)


@todo_blueprint.errorhandler(InvalidAPIUsage)
def bad_request_error(e):
    return jsonify(e.to_dict()), e.status_code

@todo_blueprint.errorhandler(InvalidAPIUsage)
def unauthorized_error(e):
    return jsonify(e.to_dict()), e.status_code


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

todo_blueprint.register_error_handler(400, bad_request_error)
todo_blueprint.register_error_handler(401, unauthorized_error)

