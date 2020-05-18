from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Task
from flaskblog.tasks.forms import TaskForm
from flaskblog.users.utils import save_picture
tasks = Blueprint('tasks', __name__)


@tasks.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    tasks = Task.query.filter_by(author=current_user).all()
    if len(tasks) >= 50:
        flash('You can not add more than 50 tasks', 'danger')
        return redirect(url_for('users.home'))
    else:
        form = TaskForm()
        if form.validate_on_submit():
            file = None
            if form.file.data:
                file = save_picture(form.file.data)
            task = Task(title=form.title.data, content=form.content.data, author=current_user,
                        due_date = form.due_date.data, completion = form.completion.data,
                        completion_date = form.completion_date.data, attachment = file)

            print('lol : ', file)
            db.session.add(task)
            db.session.commit()
            flash('Your task has been created!', 'success')
            return redirect(url_for('users.home'))
        return render_template('create_task.html', title='New Task',
                               form=form, legend='New Task')


@tasks.route("/task/<int:task_id>")
def task(task_id):
    task = Task.query.get_or_404(task_id)
    return render_template('task.html', title=task.title, post=task)


@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    form = TaskForm()
    if form.validate_on_submit():
        task.title = form.title.data
        task.content = form.content.data
        db.session.commit()
        flash('Your task has been updated!', 'success')
        return redirect(url_for('tasks.task', task_id=task.id))
    elif request.method == 'GET':
        form.title.data = task.title
        form.content.data = task.content
    return render_template('create_task.html', title='Update Task',
                           form=form, legend='Update Task')


@tasks.route("/task/<int:task_id>/delete", methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.author != current_user:
        abort(403)
    db.session.delete(task)
    db.session.commit()
    flash('Your task has been deleted!', 'success')
    return redirect(url_for('users.home'))
