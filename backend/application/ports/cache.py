from abc import ABC, abstractmethod

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass