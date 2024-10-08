
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.firebase_connect import get_firestore_client
import uuid  

views = Blueprint('views', __name__)
db = get_firestore_client()

@views.route('/')
def index():
    user = session.get('user_email', None)
    tasks = []

    if user:
        tasks_ref = db.collection('tasks').where('user', '==', user).stream()
        tasks = [{'id': task.id, **task.to_dict()} for task in tasks_ref]
    else:
        tasks = session.get('tasks', [])

    return render_template('index.html', tasks=tasks, user=user)

@views.route('/add_task', methods=['POST'])
def add_task():
    task_text = request.form.get('task')

    if 'user_email' in session:
        user = session['user_email']
        db.collection('tasks').add({
            'user': user,
            'content': task_text,
            'completed': False
        })
    else:
        tasks = session.get('tasks', [])
        task_id = str(uuid.uuid4()) 
        tasks.append({'id': task_id, 'content': task_text, 'completed': False})
        session['tasks'] = tasks

    return redirect(url_for('views.index'))

@views.route('/delete_task/<task_id>', methods=['POST'])
def delete_task(task_id):
    if 'user_email' in session:
        db.collection('tasks').document(task_id).delete()
    else:
        tasks = session.get('tasks', [])
        updated_tasks = [task for task in tasks if task['id'] != task_id]  
        session['tasks'] = updated_tasks

    return redirect(url_for('views.index'))

@views.route('/toggle_task/<task_id>', methods=['POST'])
def toggle_task(task_id):
    if 'user_email' in session:
        task_ref = db.collection('tasks').document(task_id)
        task = task_ref.get().to_dict()
        task_ref.update({'completed': not task['completed']})
    else:
        tasks = session.get('tasks', [])
        for task in tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
        session['tasks'] = tasks

    return redirect(url_for('views.index'))
