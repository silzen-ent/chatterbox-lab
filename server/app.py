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



# GET /messages: returns an array of all messages as JSON, ordered by created_at in ascending order.
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = Message.query.order_by('created_at').all()
        return make_response([message.to_dict() for message in messages], 200)

    # POST /messages: creates a new message with a body and username from params, and returns the newly created post as JSON.
    elif request.method == 'POST':
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )

        db.session.add(message)
        db.session.commit()

        return  make_response(message.to_dict(),  201,)


    
# PATCH /messages/<int:id>: updates the body of the message using params, and returns the updated message as JSON.
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()

    if request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])
        
        db.session.add(message)
        db.session.commit()

        return make_response(message.to_dict(), 200)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return make_response( {'deleted': True} , 200)

        

if __name__ == '__main__':
    app.run(port=5555)
