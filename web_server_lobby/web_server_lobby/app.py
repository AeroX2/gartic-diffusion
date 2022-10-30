import random

from flask import Flask, jsonify
from flask_socketio import join_room, leave_room, SocketIO
from lobby import Lobby, User

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

lobbies = set()
lobby_code = {}
@socketio.on('lobby_create')
def lobby_create(data):
    username = data['username']
    lobby_uuid = data['lobby_uuid']
    lobbies.add(lobby)
    
    join_room(lobby)
    send(username + ' has entered the room.', to=lobby)

@socketio.on('lobby_remove')
def lobby_remove(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=lobby)
    
@socketio.on('lobby_join')
def lobby_join(data):
    code = data['code']
    if (code in lobby_code):
        lobby = lobbies[lobby_code[code]]
        join_room(lobby)
        send(username + ' has entered the room.', to=lobby)
    emit('lobby_join', {'error': 'Invalid lobby code'})
    
valid_codes = [i for i in range(10000,99999)]
random.shuffle(valid_codes)

@socketio.on('generate_code')
def lobby_on_generate_code(data):
    lobby = data['room']
    if (lobby in lobbies):
        if (len(valid_codes) > 0):
            code = valid_codes.pop()
            lobby_code[code] = lobby
            emit('generate_code_response', {'code': code})
        else:
            emit('generate_code_response', {'error': 'Ran out of valid codes'})
    else:
        emit('generate_code_response', {'error': 'Invalid lobby uuid'})
    
if __name__ == '__main__':
    socketio.run(app)