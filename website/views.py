from crypt import methods
import imp
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Todo
from . import db

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)


@views.route('/todos', methods=['GET', 'POST'])
@login_required
def todos():
    if request.method == 'POST':
        todoContent = request.form.get('content')
        if not todoContent or len(todoContent) < 1:
            flash('Todo is too short.', category='error')
            return redirect(url_for('views.todos'))

        new_todo = Todo(content=todoContent, user_id=current_user.id)
        db.session.add(new_todo)
        db.session.commit()
        flash('Todo added!', category='success')
        return redirect(url_for('views.home'))
    return render_template('todos.html', user=current_user)

@views.route('/delete-todo', methods=['POST'])
@login_required
def deleteTodo():
    todo = request.form.get('id')
    todo = Todo.query.get(id=int(todo), user_id=current_user.id).first()
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash('Todo deleted.', category='success')
    else:
        flash('Todo does not exist or you do not has permission to delete this todo.', category='error')
    return redirect(url_for('views.home'))