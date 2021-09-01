from flask import render_template

from todo_list import app
from todo_list.app import Task, TaskStates, flask_app, info


def test_response_home():
    client = flask_app.test_client()
    response = client.get('/')
    assert response.status_code == 200


def test_home_page():
    with flask_app.test_request_context(
        '/', method='POST', data={'input_form': 'new_task_test'}
    ):
        save = app.login(False)
        assert save == render_template(
            'homepage.html',
            tableDict={1: Task('new_task_test', TaskStates.UNFINISHED)},
            which_list=info.which_list,
            task_states=TaskStates,
        )


def test_home_page_empty_str():
    with flask_app.test_request_context('/', method='POST', data={'input_form': ''}):
        save = app.login(False)
        assert save == render_template(
            'homepage.html',
            tableDict={1: Task('new_task_test', TaskStates.UNFINISHED)},
            which_list=info.which_list,
            task_states=TaskStates,
        )


def test_process_data():
    with flask_app.test_request_context(
        '/process_data/', method='POST', data={'index': 1}
    ):
        app.doit(False)
        with flask_app.test_request_context(
            '/', method='POST', data={'input_form': ''}
        ):
            save = app.login(False)
            assert save == render_template(
                'homepage.html',
                tableDict={},
                which_list=info.which_list,
                task_states=TaskStates,
            )


def test_home_page_after_disabled():
    with flask_app.test_request_context('/tasks?status=completed', method='POST'):
        app.change_status()

    with flask_app.test_request_context('/', method='POST', data={'input_form': ''}):
        save = app.login(False)
        assert save == render_template(
            'homepage.html',
            tableDict={-1: Task('new_task_test', TaskStates.COMPLETED)},
            which_list=info.which_list,
            task_states=TaskStates,
        )


def test_home_page_after_enable():
    with flask_app.test_request_context('/tasks?status=unfinished', method='POST'):
        app.change_status()

    with flask_app.test_request_context(
        '/', method='POST', data={'input_form': 'new_task_test_2'}
    ):
        save = app.login(False)
        assert save == render_template(
            'homepage.html',
            tableDict={2: Task('new_task_test_2', TaskStates.UNFINISHED)},
            which_list=info.which_list,
            task_states=TaskStates,
        )


def test_home_page_all_tasks():
    with flask_app.test_request_context('/tasks?status=all', method='POST'):
        app.change_status()

    with flask_app.test_request_context(
        '/', method='POST', data={'input_form': 'new_task_test_3'}
    ):
        save = app.login(False)  #
        assert save == render_template(
            'homepage.html',
            tableDict={
                -1: Task('new_task_test', TaskStates.COMPLETED),
                2: Task('new_task_test_2', TaskStates.UNFINISHED),
                3: Task('new_task_test_3', TaskStates.UNFINISHED),
            },
            which_list=info.which_list,
            task_states=TaskStates,
        )
