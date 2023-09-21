from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy #SQLAlchemy is an open-source SQL toolkit and object-relational mapper for the Python programming language released under the MIT License
from datetime import datetime


# initialize the app
app = Flask(__name__)

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


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
		# get the thing and location from the form ## Creating New Todo item
		thing_name = request.form['thing']
		thing_location = request.form['location']
		new_thing = Todo(thing=thing_name, location=thing_location)

		try:
			# Adding new Todo item to the database
			db.session.add(new_thing)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding your thing and / or its location'
	else:
		# get all the tasks from the database ## Reading Todo items
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template('index.html', tasks = tasks, font_url='https://fonts.googleapis.com/css2?family=Syne&display=swap')

# Route for deleting a Todo item
@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
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
		except:
			return 'There was a problem updating your task'
	else:
		return render_template('update.html', task=task, font_url='https://fonts.googleapis.com/css2?family=Syne&display=swap')

# Run the app
if __name__ == "__main__":
	app.run(debug=True)