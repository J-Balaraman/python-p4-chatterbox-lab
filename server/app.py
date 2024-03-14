from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Chatterbox Lab</h1>'

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.all()
        messages_json = [message.to_dict() for message in messages]
        return make_response(messages_json, 200)
    elif request.method == 'POST':
        json=request.get_json()
        new_message = Message(
            body=json['body'],
            username=json['username'],
        )

        db.session.add(new_message)
        db.session.commit()
        message_dict = new_message.to_dict()
        return make_response(message_dict, 201)
    
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()

    if message == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        return make_response(response_body, 404)
    
    elif request.method == 'PATCH':
        json=request.get_json()
        for attr in json:
            setattr(message, attr, json[attr])

        db.session.add(message)
        db.session.commit()
        message_dict = message.to_dict()

        return make_response(message_dict, 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }

        return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555)
