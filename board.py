from enum import Enum
import uuid
from typing import List
from collections import deque

class State(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

class Type(Enum):
    EPIC = 0
    STORY = 1
    TASK = 2

class User:
    def __init__(self, name):
        self.name = name

class Issue:
    def __init__(self, id, title, type: Type):
        self.id = id
        self.title = title
        self._state = State.TODO
        self._type = type
        self._parent: Issue = None
        self.children: List[Issue] = []
        self.assignee: User = None
    
    # type cant be changed which is why we dont have a setter
    @property
    def type(self):
        return self._type
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, state: State):
        self._state = state
    
    @parent.setter
    def parent(self, parent):
        self._parent = parent
    
    def remove_refs(self):
        for child in self.children:
            child.parent = self.parent 
        if self.parent:
            self.parent.children.remove(self)
    
    def add_child(self, child):
        self.children.append(child)

class Board:
    def __init__(self):
        self.issues = {}
    
    def add_issue(self, title, type: Type):
        id = str(uuid.uuid4())
        issue = Issue(id, title, type)
        self.issues[id] = issue
        return id
    
    def get_issue(self, issue_id):
        return self.issues.get(issue_id)
    
    def remove_issue(self, issue_id):
        issue = self.get_issue(issue_id)
        issue.remove_refs()

        self.issues.pop(issue_id)
    
    def check_all_done(self, issue):
        stack = deque()
        stack.append(issue)
        while len(stack) > 0:
            curr_issue = stack.pop()
            if curr_issue.id != issue.id and curr_issue.state != State.DONE:
                return False
            for child in curr_issue.children:
                stack.append(child)
        return True

    def set_issue_state(self, issue_id, state):
        issue = self.get_issue(issue_id)

        curr_issue = issue
        if state == State.DONE:
            if not self.check_all_done(curr_issue):
                raise ValueError("Not all children are done")

        issue.state = state
    
    def set_parent_issue(self, issue_id, parent_issue_id):
        child = self.get_issue(issue_id)
        parent = self.get_issue(parent_issue_id)

        if child.type == Type.EPIC:
            raise ValueError("Epics cannot have parents")
        if child.type == Type.STORY and parent.type != Type.EPIC:
            raise ValueError("Stories can only have epics as parents")
        if child.type == Type.TASK and parent.type == Type.TASK:
            raise ValueError("Tasks cannot have tasks as parents")
            
        child.parent = parent
        parent.add_child(child)