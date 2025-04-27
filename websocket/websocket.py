from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS  # Allow all origins for CORS

# Create the Flask app
app = Flask(__name__)

# Initialize SocketIO with the app
socketio = SocketIO(app, cors_allowed_origins=["http://localhost:5173", "http://localhost:5000", "http://localhost:5001"])  # Allow only the React frontend

# Allow CORS for all origins
CORS(app, resources={r"/*": {"origins": "*"}})  # You can restrict origins for production

# Route for index (optional, for testing the server)
@app.route('/')
def index():
    return "WebSocket server is running!"

# Handle incoming WebSocket messages
@socketio.on('message')
def handle_message(data):
    print(f"Received message: {data}")
    send(f"Server says: {data}")  # Send message back to the client
    emit("message",data, broadcast=True)

@socketio.on('alarm')
def handle_alarm(data):
    print(f"Alarm received: {data}")
    emit("alarm", data, broadcast=True)
# Handle a custom event (optional)
@socketio.on('my event')
def handle_my_event(json):
    print(f"Received custom event data: {json}")
    emit('my response', {'data': 'Response from server'})  # Emit custom event back

# Run the Flask app with SocketIO
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
