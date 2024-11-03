from typing import List
import issue

class User:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.issues: List[issue.Issue] = []