from abc import ABC, abstractmethod

class Repo(ABC):
    def __init__(self, *args, **kwargs):
        self._initialize(*args, **kwargs)
    
    def _initialize(self, *args, **kwargs):
        # Polymorphic method
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def initialize(self):
        pass