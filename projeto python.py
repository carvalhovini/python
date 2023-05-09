from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    priority = db.Column(db.Integer, nullable=False, default=1)
    due_date = db.Column(db.Date)
    done = db.Column(db.Boolean, default=False)

@app.route('/')
def index():
    tasks = Task.query.order_by(Task.priority).all()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = int(request.form['priority'])
        due_date = request.form['due_date']
        task = Task(title=title, description=description, priority=priority, due_date=due_date)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_task(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = int(request.form['priority'])
        task.due_date = request.form['due_date']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/delete/<int:id>')
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
