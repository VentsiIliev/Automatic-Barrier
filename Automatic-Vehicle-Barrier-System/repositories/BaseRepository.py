from abc import ABC, abstractmethod


class BaseRepository(ABC):
    @abstractmethod
    def get(self, query):
        pass

    @abstractmethod
    def insert(self, query, params):
        pass

    @abstractmethod
    def delete(self, query, params):
        pass
