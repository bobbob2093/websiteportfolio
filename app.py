from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.description}>'

def init_db():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created.")

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

app = create_app()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('home.html', tasks=tasks)

@app.route('/sebastian')
def sebastian():
    tasks = Task.query.all()
    return render_template('sebastian.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    description = request.form['task']
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
    new_task = Task(description=description, due_date=due_date)
    db.session.add(new_task)
    db.session.commit()
    return home()

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return home()

@app.route('/toggle/<int:task_id>')
def toggle_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return home()



if __name__ == '__main__':
    app.run(debug=True)
