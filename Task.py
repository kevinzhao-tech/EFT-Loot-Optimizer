from typing import List
from pytarkovdata import send_query

class Task:
    def __init__(self, id: str) -> None:
        self.id = id
