from enum import Enum
from typing import List
import user
import datetime

class State(Enum):
    TODO = 0
    IN_PROGRESS = 1
    DONE = 2

class Type(Enum):
    EPIC = 0
    STORY = 1
    TASK = 2

class Issue:
    def __init__(self, id, title, type: Type):
        self.id = id
        self.title = title
        self._state = State.TODO
        self._type = type
        self._parent: Issue = None
        self.children: List[Issue] = []
        self.assignee: user.User = None
        self.created_at = datetime.datetime.now()
    
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
    
    def add_child(self, child):
        self.children.append(child)