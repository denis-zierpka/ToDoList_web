from enum import Enum

from flask import Flask, redirect, render_template, request, url_for

flask_app = Flask(__name__)


class TaskStates(Enum):
    UNFINISHED = 0
    COMPLETED = 1
    ALL = 2


class Task:
    def __init__(self, value, status):
        self.value = value
        self.status = status


class Information:
    tableDict = {}

    def __init__(self):
        self.identifier = 1

    @property
    def key(self):
        return self.identifier

    @key.setter
    def key(self, value):
        self.identifier = value

    which_list = TaskStates.UNFINISHED


info = Information()


@flask_app.route('/', methods=['post', 'get'])
def login(reload_page_after_request=True):
    if request.method == 'POST':
        input_form = request.form.get('input_form')  # запрос к данным формы
        if input_form != '':
            info.tableDict[info.key] = Task(input_form, TaskStates.UNFINISHED)
            info.key = info.key + 1

        if reload_page_after_request:
            return redirect(url_for('login'))

    to_post = {}
    if info.which_list == TaskStates.ALL:
        to_post = info.tableDict
    else:
        for key, val in info.tableDict.items():
            if val.status == info.which_list:
                to_post[key] = val

    return render_template(
        'homepage.html',
        tableDict=to_post,
        which_list=info.which_list,
        task_states=TaskStates,
    )


@flask_app.route('/process_data/', methods=['POST'])
def doit(reload_page_after_request=True):
    index = request.form['index']
    info.tableDict[-1 * int(index)] = Task(
        info.tableDict[int(index)].value, TaskStates.COMPLETED
    )
    info.tableDict.pop(int(index))
    if reload_page_after_request:
        return redirect(url_for('login'))
    return True


@flask_app.route('/tasks', methods=['POST'])
def change_status(reload_page_after_request=True):
    if request.args['status'] == 'completed':
        info.which_list = TaskStates.COMPLETED
    elif request.args['status'] == 'unfinished':
        info.which_list = TaskStates.UNFINISHED
    else:
        info.which_list = TaskStates.ALL
    if reload_page_after_request:
        return redirect(url_for('login'))
    return True
