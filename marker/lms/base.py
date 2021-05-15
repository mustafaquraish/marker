from abc import ABC, abstractmethod
from functools import cached_property
from ..utils.token import get_or_prompt_token, save_token

class LMS(ABC):
    def __init__(self, name, identifier):
        self.__name = name
        self.__identifier = identifier

    @cached_property
    def token(self):
        return get_or_prompt_token(self.console, self.__name, self.__identifier)

    def save_token(self, token):
        save_token(self.__name, self.__identifier, token)

    @abstractmethod
    async def download_submission(self, session, student):
        pass

    @abstractmethod
    async def upload_mark(self, session, student, mark_list):
        pass

    @abstractmethod
    async def upload_report(self, session, student):
        pass
    
