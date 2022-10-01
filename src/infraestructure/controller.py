from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def initialize(self):
        pass