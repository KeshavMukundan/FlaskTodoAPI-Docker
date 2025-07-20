from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@db/todo"
# If running normally
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost/todo"

# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@localhost:3307/todo_db"


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'supersecretkey'
SUPER_SECRET_KEY = app.config["SECRET_KEY"]

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable= True)
    email = db.Column(db.String(100), unique= True, nullable= False)
    password = db.Column(db.String(200), nullable= False)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable= False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)

    user = db.relationship('User', backref= db.backref('todos'), lazy= True)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing"})
        
        try:
            data = jwt.decode(token, SUPER_SECRET_KEY, algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "The token has expired"}), 400
        except jwt.InvalidTokenError:
            return jsonify({"message": "The token is invalid"}), 400

        return f(current_user, *args, **kwargs)        
    return decorator



@app.route("/")
def index():
    return jsonify({"message": "API running... "})

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"Name" : name, "Email": email, "Password": hashed_password}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid Credentials"}), 401
    

    payload = {"user_id": user.id, "exp": datetime.now(timezone.utc) + timedelta(hours = 1)}

 

    token = jwt.encode(payload, SUPER_SECRET_KEY, algorithm= 'HS256')    
    return jsonify({"token": token}), 200
    


@app.route("/todos", methods=["POST"])
@token_required
def create_todos(current_user):
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")



    new_todo = Todo(title= title, description= description, user_id= current_user.id)

    db.session.add(new_todo)
    db.session.commit()

    return jsonify({"id": new_todo.id, "title": new_todo.title,
                    "description": new_todo.description, "user_id": current_user.id}), 200


@app.route("/todos")
@token_required
def get_todos(current_user):
    page = request.args.get("page", default= 1, type= int)
    limit = request.args.get("limit", default= 1, type= int)

    offset = (page - 1) * limit

    todos = Todo.query.filter_by(user_id= current_user.id).offset(offset).limit(limit).all()
    total = Todo.query.filter_by(user_id= current_user.id).count()
    result = [{"id": todo.id, "title": todo.title, "description": todo.description} for todo in todos]

    return jsonify({"data": result, "page": page, "limit": limit, "total": total}), 200


@app.route("/todos/<int:id>", methods=["PUT"])
@token_required
def update_todos(current_user, id):
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")

    todo = db.session.get(Todo, id)
    if not todo:
        return jsonify({"error": "Todo not Found"}), 404
    if todo.user_id != current_user.id:
        return jsonify({"error": "Authentication Failed"}), 403

    todo.title = title
    todo.description = description
    db.session.commit()


    return jsonify({"id": todo.id, "title": todo.title, "description": todo.description}), 200

@app.route("/todos/<int:id>", methods= ["DELETE"])
@token_required
def delete_todo(current_user, id):
    todo = db.session.get(Todo, id)

    if not todo:
        return jsonify({"error": "Todo NOT FOUND"}), 404
    if todo.user_id != current_user.id:
        return jsonify({"error": "Authentication Failed"})
    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "The Todo has been successfully deleted"}), 200



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=3700, host= '0.0.0.0')