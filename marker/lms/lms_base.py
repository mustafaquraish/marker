from abc import ABC, abstractmethod

class LMS(ABC):

    @abstractmethod
    async def download_submission(self, session, student):
        pass

    @abstractmethod
    async def upload_mark(self, session, student, mark_list):
        pass

    @abstractmethod
    async def upload_report(self, session, student):
        pass
