from abc import ABC, abstractmethod

class LoggerPort(ABC):
    @abstractmethod
    def error(self, message: str):
        raise NotImplementedError
    
    @abstractmethod
    def warning(self, message: str):
        raise NotImplementedError
    
    @abstractmethod
    def info(self, message: str):
        raise NotImplementedError
    
    @abstractmethod
    def debug(self, message: str):
        raise NotImplementedError