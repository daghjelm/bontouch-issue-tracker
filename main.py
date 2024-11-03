from board import Board, State, Type

if __name__ == "__main__":
    board = Board()

    epic_id = board.add_issue("epic", Type.EPIC)
    story_id = board.add_issue("story", Type.STORY)
    task_id = board.add_issue("task", Type.TASK)

    board.set_parent_issue(task_id, story_id)
    board.set_parent_issue(story_id, epic_id)

    print(board.get_issue(task_id).parent.title)
    print(board.get_issue(story_id).parent.title)

    board.set_issue_state(task_id, State.IN_PROGRESS)
    board.set_issue_state(story_id, State.IN_PROGRESS)
    board.set_issue_state(epic_id, State.IN_PROGRESS)
    
    board.set_issue_state(task_id, State.DONE)
