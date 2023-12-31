from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the app
app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

font_url = 'https://fonts.googleapis.com/css2?family=Syne&display=swap'

# Define the Todo database model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thing = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

# Home route, allows both GET and POST requests
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        thing_name = request.form['thing']
        thing_location = request.form['location']
        new_thing = Todo(thing=thing_name, location=thing_location)
        
        try:
            db.session.add(new_thing)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            return 'There was an issue adding your thing and / or its location'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, font_url=font_url)

# Route for deleting a Todo item
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        logging.error(f"Exception occurred: {e}")
        return 'There was a problem deleting that task'

# Route for updating a Todo item
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.thing = request.form['thing']
        task.location = request.form['location']

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            logging.error(f"Exception occurred: {e}")
            return 'There was a problem updating your task'
    else:
        return render_template('update.html', task=task, font_url=font_url)

with app.app_context():
    db.create_all()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
