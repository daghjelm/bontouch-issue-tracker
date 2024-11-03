from enum import Enum
import uuid
from collections import deque
from issue import Issue, State, Type
from user import User
from typing import Dict, List
import datetime

class Board:
    def __init__(self):
        self.issues: Dict[str, Issue] = {}
        self.users: Dict[str, User] = {}
    
    def add_issue(self, title, type: Type):
        id = str(uuid.uuid4())
        issue = Issue(id, title, type)
        self.issues[id] = issue
        return id
    
    def get_issue(self, issue_id):
        return self.issues.get(issue_id)
    
    def remove_issue(self, issue_id):
        issue: Issue = self.get_issue(issue_id)
        for child in issue.children:  
            child.parent = issue.parent
        if issue.parent:
            issue.parent.children.remove(issue)

        self.issues.pop(issue_id)
    
    def check_all_done(self, issue: Issue):
        stack: deque[Issue] = deque()
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
    
    def add_user(self, name):
        id = str(uuid.uuid4())
        user = User(id, name)
        self.users[id] = user
        return id
    
    def remove_user(self, user_id):
        user: User = self.users.get(user_id)
        for issue in user.issues:
            issue.assignee = None
        self.users.pop(user_id)
    
    def get_users(self):
        return self.users.values()
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def assign_user(self, user_id, issue_id):
        user = self.get_user(user_id)
        issue = self.get_issue(issue_id)

        issue.assignee = user
        user.issues.append(issue)
    
    def get_issues(
        self,
        user_id=None,
        issue_types: List[Type]=None,
        start_date: datetime.datetime=None,
        end_date: datetime.datetime=None,
        ):

        issues = self.issues.values()
        if user_id:
            issues = filter(
                lambda issue: issue.assignee and issue.assignee.id == user_id,
                issues)
        if issue_types:
            issues = filter(
                lambda issue: issue.type in issue_types,
                issues)
        if start_date:
            issues = filter(
                lambda issue: issue.created_at >= start_date,
                issues)
        if end_date:
            issues = filter(
                lambda issue: issue.created_at < end_date,
                issues)
        
        return list(issues)
