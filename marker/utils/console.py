from abc import ABC, abstractmethod

class ConsoleABC(ABC):

    @abstractmethod
    def error(self, *args, **kwargs):
        pass

    @abstractmethod
    def log(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def get(self, prompt, **kwargs):
        pass

    @abstractmethod
    def ask(self, prompt, default=False, **kwargs):
        pass
    
    @abstractmethod
    def track(self, tasks, label):
        pass

    @abstractmethod
    async def track_async(self, tasks, label):
        pass