# from flask import Flask, request, jsonify, render_template
# from flask_cors import CORS
# import datetime

# app = Flask(__name__)
# CORS(app)  # Allow frontend JS to POST

# # Simulated storage (in-memory or you can write to file/db)
# feedback_list = []

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/submit_feedback', methods=['POST'])
# def submit_feedback():
#     data = request.json
#     message = data.get('message')
#     sender = data.get('sender', 'Anonymous')
#     timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     # Simulate storing the message
#     feedback_entry = {
#         'sender': sender,
#         'message': message,
#         'timestamp': timestamp
#     }
#     feedback_list.append(feedback_entry)

#     print(f"📨 Feedback received from {sender}: {message} at {timestamp}")
    
#     # Respond back to the frontend
#     return jsonify({'status': 'success', 'message': 'Feedback received!'}), 200

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Feedback model
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(100), nullable=False)
    recipient = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.String(50), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    sender = data.get('sender', 'Anonymous')
    recipient = data.get('recipient', 'Priyanka Hulsure')
    message = data.get('message')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_feedback = Feedback(sender=sender, recipient=recipient, message=message, timestamp=timestamp)
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Feedback submitted!'})

@app.route('/feedbacks/<username>')
def view_feedback(username):
    feedbacks = Feedback.query.filter_by(recipient=username).order_by(Feedback.id.desc()).all()
    return render_template('feedback_view.html', user=username, feedbacks=feedbacks)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
