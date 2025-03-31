from flask import Flask
from db import db
from flask_migrate import Migrate
from todo.todo_blueprint import todo_blueprint

app = Flask(__name__)

app.register_blueprint(todo_blueprint)

# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///to-do-app.db" #TODO: create a configuration file to add all configurations
# initialize the app with the extension
db.init_app(app)

# Initialize Flask-Migrate 
migrate = Migrate(app, db)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)