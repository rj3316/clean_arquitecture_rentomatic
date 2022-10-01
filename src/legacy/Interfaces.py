
from abc import ABC, abstractmethod

class Interface(ABC):
    pass

class IService(Interface):
    pass

class IQueueManager(Interface):
    @abstractmethod
    def get_queues(self):
        pass

    @abstractmethod
    def read_queue(self):
        pass
        
    @abstractmethod
    def send(self, *args, **kwargs):
        pass

class IStateManager(Interface):
    @abstractmethod
    def set_functions(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_substates(self, *args, **kwargs):
        pass

    @abstractmethod
    def exec_state(self):
        pass

    @abstractmethod
    def exec_substate(self):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_substate(self):
        pass

    @abstractmethod
    def is_exiting(self):
        pass

class IErrorManager(Interface):
    @abstractmethod
    def error_handler(self, *args, **kwargs):
        pass

class ILogManager(Interface):
    @abstractmethod
    def create_log(self):
        pass

    @abstractmethod
    def write_log(self):
        pass

    @abstractmethod
    def close_log(self):
        pass

class IDatabase(Interface):
    @abstractmethod
    def check_connection_status(self):
        pass

    @abstractmethod
    def select(self, *args, **kwargs):
        pass

    @abstractmethod
    def insert(self, *args, **kwargs):
        pass
    @abstractmethod
    def update(self, *args, **kwargs):
        pass
    @abstractmethod
    def delete(self, *args, **kwargs):
        pass

class IModbus(Interface):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def get_connection_status(self, *args, **kwargs):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, *args, **kwargs):
        pass

    @abstractmethod # Metodo dudoso
    def get_sockets(self):
        pass

class IMqtt(Interface):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def reconnect(self):
        pass

    @abstractmethod
    def get_connection_status(self):
        pass

    @abstractmethod
    def subscribe(self):
        pass
    
    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def on_message(self, *args, **kwargs):
        pass