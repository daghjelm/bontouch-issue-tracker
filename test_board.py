import pytest
from board import Board, State, Type
import datetime

@pytest.fixture
def board():
    return Board()

def test_add_issue(board):
    id = board.add_issue("test issue", Type.EPIC)
    assert board.get_issue(id).title == "test issue"
    assert board.get_issue(id).type == Type.EPIC
    assert board.get_issue(id).state == State.TODO

def test_set_parent_issue(board):
    # Test that an epic cannot have a parent
    task_id = board.add_issue("task", Type.TASK)
    task_id2 = board.add_issue("task2", Type.TASK)
    epic_id = board.add_issue("epic", Type.EPIC)
    story_id = board.add_issue("story", Type.STORY)

    with pytest.raises(ValueError):
        board.set_parent_issue(epic_id, epic_id)
    with pytest.raises(ValueError):
        board.set_parent_issue(story_id, task_id)
    with pytest.raises(ValueError):
        board.set_parent_issue(task_id, task_id2)
    
    # Test that a story can have an epic parent
    board.set_parent_issue(story_id, epic_id)
    assert board.get_issue(story_id).parent.id == epic_id

def test_remove_issue(board):
    parent_id = board.add_issue("parent issue", Type.STORY)
    child_id = board.add_issue("child issue", Type.TASK)

    # check that removing a parent issue 
    # removes the child's parent reference
    board.set_parent_issue(child_id, parent_id)
    board.remove_issue(parent_id)
    child = board.get_issue(child_id)

    assert child.parent == None
    assert board.get_issue(parent_id) == None

    # check that removing a parent issue
    # gives the child the parent's parent as parent
    new_parent_id = board.add_issue("new parent issue", Type.STORY)
    grandparent_id = board.add_issue("grandparent", Type.EPIC)

    board.set_parent_issue(child_id, new_parent_id)
    board.set_parent_issue(new_parent_id, grandparent_id)
    board.remove_issue(new_parent_id)

    assert child.parent.id == grandparent_id

def test_set_issue_state(board):
    epic_id = board.add_issue("epic", Type.EPIC)
    story_id = board.add_issue("story", Type.STORY)
    task_id = board.add_issue("task", Type.TASK)
    task_id2 = board.add_issue("task2", Type.TASK)

    board.set_parent_issue(task_id, story_id)
    board.set_parent_issue(task_id2, story_id)
    board.set_parent_issue(story_id, epic_id)

    board.set_issue_state(task_id, State.IN_PROGRESS)
    board.set_issue_state(task_id2, State.IN_PROGRESS)
    assert board.get_issue(task_id).state == State.IN_PROGRESS

    board.set_issue_state(story_id, State.IN_PROGRESS)
    board.set_issue_state(epic_id, State.IN_PROGRESS)

    with pytest.raises(ValueError):
        board.set_issue_state(story_id, State.DONE)

    board.set_issue_state(task_id, State.DONE)

    with pytest.raises(ValueError):
        board.set_issue_state(story_id, State.DONE)

    board.set_issue_state(task_id2, State.DONE)

    # tasks are done, but story is not so we cannot set epic to done yet
    with pytest.raises(ValueError):
        board.set_issue_state(epic_id, State.DONE)

    board.set_issue_state(story_id, State.DONE)
    board.set_issue_state(epic_id, State.DONE)

    assert board.get_issue(epic_id).state == State.DONE

def test_add_user(board):
    id = board.add_user("test user")
    assert board.users[id].name == "test user"

def test_remove_user(board):
    user_id = board.add_user("test user")
    issue_id = board.add_issue("test issue", Type.EPIC)
    board.assign_user(user_id, issue_id)
    board.remove_user(user_id)
    assert board.get_issue(issue_id).assignee == None

def test_assign_user(board):
    user_id = board.add_user("test user")
    issue_id = board.add_issue("test issue", Type.EPIC)
    board.assign_user(user_id, issue_id)
    assert board.get_issue(issue_id).assignee.id == user_id

def test_get_users(board):
    user_id = board.add_user("test user")
    assert list(board.get_users())[0].name == "test user"

def test_get_issue(board):
    issue_id = board.add_issue("test issue", Type.EPIC)
    assert board.get_issue(issue_id).title == "test issue"

def test_get_issues(board):
    issue_id1 = board.add_issue("test issue1", Type.EPIC)
    issue_id2 = board.add_issue("test issue2", Type.STORY)
    issue_id3 = board.add_issue("test issue3", Type.TASK)
    user_id = board.add_user("test user")
    board.assign_user(user_id, issue_id1)

    issue2 = board.get_issue(issue_id2)
    issue2.created_at = issue2.created_at.replace(year=2022)
    issue3 = board.get_issue(issue_id3)
    issue3.created_at = issue3.created_at.replace(year=2021)

    date = datetime.datetime.now().replace(year=2020)
    date2 = datetime.datetime.now().replace(year=2023)

    assert len(list(board.get_issues())) == 3
    assert len(board.get_issues(user_id=user_id)) == 1
    assert len(board.get_issues(issue_types=[Type.EPIC])) == 1
    assert len(board.get_issues(issue_types=[Type.STORY, Type.TASK])) == 2

    assert len(board.get_issues(start_date=date, end_date=date2)) == 2


