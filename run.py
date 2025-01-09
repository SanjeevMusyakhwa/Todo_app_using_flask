from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Configure the SQLite database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'{self.name}'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    tasks = Task.query.all()  # Fetch all tasks from the database
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST', 'GET'])
def create_task():
    if request.method == 'POST':
        task_name = request.form.get('task')
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_task.html')

@app.route('/delete/<int:id>', methods=['GET'])
def delete_task(id):
    task = Task.query.get(id)  # Find the task by id
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
