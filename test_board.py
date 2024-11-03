import pytest

from board import Board, State, Type

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
    epic_id = board.add_issue("epic", Type.EPIC)
    story_id = board.add_issue("story", Type.STORY)
    with pytest.raises(ValueError):
        board.set_parent_issue(epic_id, story_id)
    
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

    board.set_parent_issue(task_id, story_id)
    board.set_parent_issue(story_id, epic_id)

    board.set_issue_state(task_id, State.IN_PROGRESS)
    assert board.get_issue(task_id).state == State.IN_PROGRESS

    board.set_issue_state(story_id, State.IN_PROGRESS)
    board.set_issue_state(epic_id, State.IN_PROGRESS)

    with pytest.raises(ValueError):
        board.set_issue_state(epic_id, State.DONE)
    
    with pytest.raises(ValueError):
        board.set_issue_state(story_id, State.DONE)

    board.set_issue_state(task_id, State.DONE)

    # task is done, but story is not so we cannot set epic to done yet
    with pytest.raises(ValueError):
        board.set_issue_state(epic_id, State.DONE)

    board.set_issue_state(story_id, State.DONE)
    board.set_issue_state(epic_id, State.DONE)
    assert board.get_issue(epic_id).state == State.DONE
    assert board.get_issue(story_id).state == State.DONE
    assert board.get_issue(task_id).state == State.DONE