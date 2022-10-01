#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
#----------------------------------------------------------------------------
# Created By  : Igor Usunariz
# Created Date: 2022/07/16
# version ='1.0'
# Mail = 'i.usunariz.lopez@gmail.com'
#
# ---------------------------------------------------------------------------
# 
# MODULE PARENT CLASS for LOOP
#
# Dependencies
#   auxiliars.dump_configuration, auxiliars.send_message
# 
# ---------------------------------------------------------------------------
'''
from abc import ABC
from dataclasses import dataclass, field
from typing import List
from queue import Queue, Empty
from sys import exc_info

class Module(ABC):
    _modules  = dict()
    queue_ready = False
    _log_list = list()

    @property
    def log_list(self):
        return Module._log_list
    
    @log_list.setter
    def log_list(self, value):
        if isinstance(value, str) or isinstance(value, tuple): value = [value]

        if isinstance(value, list):
            if bool(value): Module._log_list += value
            else: Module._log_list = list()

    @property
    def modules(self):
        return Module._modules

    @modules.setter
    def modules(self, value):
        c = Checker()
        c.c = self.data.caller == 'Main'
        c.c = self.data.caller == ''
        if  c.c_and: module = 'Main'
        else: module = self.data.classname
        
        Module._modules[module] = value

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        if isinstance(value, DSModule): self._data = value
        
    def __init__(self, config = None):
        try:
            self._init_process(config)
        except Exception as e:
            self._error_handler(f"Module {self.data.tag} instantiation error")
       
    # INSTANTIATION
    def _init_process(self, config = None):
            self.__initialization()
            self.__configuration(config)
            self.__setting()

            c = Checker()
            c.c = (config is not None)
            try   : c.c = self.data.config['welcome']
            except: pass
            if c.c_and: self.__welcome()

            self.__finish_initialization()

            self.add_module()

    def __initialization(self):
        try:
            self._messager = None
            self._data     = DSModule()

            # Configuración estructural de la instancia del módulo
            self.data.classname, self.data.basenames = get_class_herency(self)
            self.data.tag = self.data.classname.lower()

            self._initialization()
        except AttributeError:
            pass
        except Exception as e:
            self._error_handler("Error on module initialization")
        finally:
            self.data.initialize = False

    def __configuration(self, config = None):
        if config is not None:
            self.set_configuration(config)
        try:
            self._configuration()
        except AttributeError:
            pass
        except Exception as e:
            payload = f"Error on module configuration"
            self._error_handler(payload)
        finally:
            self.__after_configuration()

    def __after_configuration(self):
        if 'debug' in self.data.config:
            self.data.debug = self.data.config['debug']
            self.data.config.pop('debug')

        try:
            self._after_configuration()
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        except Exception as e:
            self._error_handler('Error on module after configuration')

    def __setting(self):
        try:
            config = {
                'queue' : self.data.classname,
                'caller': self.data.tag,
            }
            self._messager = Messager(config)

            self._setting()
        except AttributeError:
            pass
        except Exception as e:
            self._error_handler("Error on module setting up")
    
    def __welcome(self):
        payloads = self.data.payloads
        self.data.payloads = list()

        self.data.payloads = (f"* {self.data.tag.upper()} module created [{self}]", 30)
        self.data.payloads = (f"Debug: {self.data.debug}", 20)

        try:
            self._welcome()
        except AttributeError:
            pass
        except TypeError:
            pass
        except Exception as e:
            self._error_handler("Error on module welcome")
        finally:
            self.data.payloads = payloads
            self.send()

    def welcome(self):
        self.__welcome()
        
    def __finish_initialization(self):
        try:
            self._finish_initialization()
        except AttributeError as e:
            pass
        except TypeError as e:
            pass
        except Exception as e:
            self._error_handler('Error on module initialization finish')

    def tmp(self):
        # Método temporal para ejecutar eval
        pass
    
    # PUBLIC METHODS
    def set_configuration(self, config = None):
        if isinstance(config, dict):
            for key, value in config.items():
                if not isinstance(value, dict):
                    setattr(self.data, key, value)
                else:
                    self.data.config = value

    def upgrade(self):
        ret_val = self.read_queue()
        
        try:
            self._upgrade()
        except AttributeError:
            pass
        except Exception as e:
            self._error_handler('Error on module welcome')

        return ret_val

    def read_queue(self):
        messages = list()

        try: messages = self._messager.read_queue()
        except: pass
        
        try:
            self._check_messages(messages)
        except AttributeError:
            pass
        except Exception as e:
            self._error_handler("Error checking messages")

    def get_classname(self):
        return self.data.classname

    def get_basenames(self):
        return self.data.basenames

    def welcome_module(self):
        self.__welcome()

    # UPDATE
    def _upgrade(self):
        # Polymorphic method
        return None

    def _check_messages(self, messages):
        # Polymorphic method
        return messages

    # ERROR HANDLER
    def _error_handler(self, *args, **kwargs):
        details = self.__get_error_info(*args, **kwargs)

        error_handler = ErrorHandler()
        details = error_handler.get_error_info(details)

        no_manager = True
        try:
            if isinstance(self._messager, Messager):
                self._send_error(details)
                self.modules['ErrorManager'].error_handler(details = details)
                no_manager = False
        except: pass
            
        if no_manager: print(details)
        
    def __get_error_info(self, *args, **kwargs):
        ret_val = {}
        ret_val['caller'] = self.data.caller
        ret_val['tag']    = self.data.tag

        if not 'info' in kwargs:
            if isinstance(args[0], str): ret_val['info'] = args[0]
        else: ret_val['info'] = kwargs['info']

        if not 'warning' in kwargs:
            try:
                if isinstance(args[1], bool): ret_val['warning'] = args[1]
            except: ret_val['warning'] = False
        else: ret_val['warning'] = kwargs['warning']

        return ret_val

    # INTERNAL MESSAGER INTERFACE
    def _send_debug(self, *args, **kwargs):
        kwargs['level'] = 10
        self.send(*args, **kwargs)

    def _send_info(self, *args, **kwargs):
        kwargs['level'] = 20
        self.send(*args, **kwargs)

    def _send_warning(self, *args, **kwargs):
        kwargs['level'] = 30
        self.send(*args, **kwargs)

    def _send_error(self, *args, **kwargs):
        kwargs['level'] = 40
        self.send(*args, **kwargs)

    def _send_critical(self, *args, **kwargs):
        kwargs['level'] = 50
        self.send(*args, **kwargs)

    def event_X(send_function):
        def wrapper(self, *args, **kwargs):
            kwargs = self.fit_kwargs_to_message(*args, **kwargs)

            return send_function(self, *args, **kwargs)
       
        return wrapper

    def send_X(send_function):
        def wrapper(self, *args, **kwargs):
            kwargs = self.fit_kwargs_to_message(*args, **kwargs)

            return send_function(self, *args, **kwargs)
       
        return wrapper

    def fit_kwargs_to_message(self, *args, **kwargs):
        # Corregimos payloads
        try:
            if not 'payloads' in kwargs.keys(): kwargs['payloads'] = args[0]
        except:
            kwargs['payloads'] = self.data.payloads
            self.data.payloads = list()
        
        # Corregimos level
        try:
            if not 'level' in kwargs.keys(): kwargs['level'] = args[1]
        except: kwargs['level'] = 'NOTSET'

        # Corregimos topic
        default_topic = 'log'
        try:
            if not 'topic' in kwargs.keys(): kwargs['topic'] = args[2]
        except: kwargs['topic'] = default_topic

        # Corregimos queue
        default_queue = 'LogManager'
        try:
            if not 'queue' in kwargs.keys(): kwargs['queue'] = args[3]
        except: kwargs['queue'] = default_queue

        # Corregimos sender
        kwargs['sender'] = self.data.classname

        # Comprobamos que QueueManager ha sido creado	
        default_manager = 'QueueManager'

        try: kwargs['ref'] = self.modules[default_manager]
        except: kwargs['ref'] = None

        return kwargs

    @send_X
    def send(self, *args, **kwargs):
        c0 = Module.queue_ready
        c1 = isinstance(self._messager, Messager)

        if c0 and c1: self._messager.send(*args, **kwargs)
        else: 
            try: self.log_list = kwargs['payloads']
            except Exception as e:print(e)

    @event_X
    def event(self, *args, **kwargs):
        try:
            self._event(*args, **kwargs)
        except AttributeError:
            pass
        except Exception as e:
            payload = f"Error on module event: {e}"
            self._send_error(payload)
    
    # MODULE MANAGEMENT
    def get_module_base_configuration(self):
        ret_val = {
            'caller' : self.data.tag,
            'caller_classname' : self.data.classname,
            'verbose': self.data.verbose,
            'debug'  : self.data.debug,
            'event'  : self.event,
            'config' : {},
        }
        return ret_val

    def get_module_configuration(self, config = None, module = None):
        ret_val = dict
        
        try:
            if config is None:
                if module in self.data.config.keys():
                    config = self.data.config[module]
                else:
                    config = {}
        except Exception as e:
            print(e)

        ret_val = self.get_module_base_configuration()
        ret_val['config'] = config

        return ret_val
    
    def add_module(self, module = None):
        if self.data.caller == '': return None

        if self.data.tag == 'service' or 'sma' in self.data.tag:
            pause = True

        try: 
            if module is None: self.data.event = self.event
            else: self.data.event = module.event
        except Exception as e:
            self.data.event = self.event

        if module is None: module = self
        self.modules = module

    def delete_module(self, module = None):
        if module is None:
            module = self.modules[-1]

        if module in self.modules: self.modules.pop(module)

@dataclass
class Message:
    payload  : str = ''
    level    : str = 'DEBUG'
    topic    : str = 'log'
    queue    : str = 'LogManager'
    sender   : str = None

class Messager():
    queues = None

    def __init__(self, config = None):
        self._queue  = None
        self._caller = None

        if config is not None:
            if 'queue' in config.keys():
                self._queue  = config['queue']
            if 'caller' in config.keys():
                self._caller = config['caller']

    # INTERFACES
    def get_queues(self):
        return Messager.queues

    def set_queues(self, queues = None):
        self._set_queues(queues)

    def _set_queues(self, queues = None):
        ret_val = False

        c = True
        if isinstance(queues, dict):
            for _, queue in queues.items():
                c = c and isinstance(queue, Queue)

                if not c: break

        if c:
            Messager.queues = queues
            ret_val = True
        
        return ret_val

    def read_queue(self):
        ret_val = list()

        if (Messager.queues is not None) and (self._queue is not None):

            # Comprobamos la queue de mensajes
            try:
                # Get messages (maximum set by max_elements_per_read)
                while True:
                    # Leemos el mensaje y lo procesamos
                    message = Messager.queues[self._queue].get_nowait()
                    # message = self._queues[queue].get_nowait()
                    ret_val.append(message)
            except Empty:
                # When no message is in queue, exception is raised
                pass
            except Exception as e:
                self._error_handler(f"Error checking module queue \'{self._queue}\'")
        
        return ret_val

    def send(self, *args, **kwargs):
        # Construimos los mensajes y lo enviamos
        messages = self.build_messages(*args, **kwargs)

        for message in messages:
            self._send_message(message)              
    
    def is_ok(self):
        return Messager.queues is not None

    # QUEUE
    def build_messages(self, *args, **kwargs):
        ret_val = list()

        if 'payloads' in kwargs.keys():
            if kwargs['payloads'] is not None:
                # Corregimos payloads
                payloads = kwargs['payloads']
                if not isinstance(payloads, list): payloads = [payloads]

                # Corregimos level
                def_level = 'NOTSET'
                if 'level' in kwargs.keys():
                    if (kwargs['level'] is not None):
                        def_level = self._parse_message_level(kwargs['level'])

                # Corregimos topic
                topic = 'log'
                if 'topic' in kwargs.keys():
                    if (kwargs['topic'] is not None):
                        topic = kwargs['topic']

                # Corregimos queue
                queue = 'LogManager'
                if 'queue' in kwargs.keys():
                    if (kwargs['queue'] is not None):
                        queue = kwargs['queue']

                # Corregimos sender 
                sender = self._caller
                if 'sender' in kwargs.keys():
                    if (kwargs['sender'] is not None):
                        sender = kwargs['sender']
                    
                ret_val = list()
                for payload in payloads:
                    if isinstance(payload, tuple):
                        level   = self._parse_message_level(payload[1])
                        payload = payload[0]
                    else:
                        level = def_level
                    
                    ret_val.append(Message(payload, level, topic, queue, sender))
                    
        return ret_val

    def _parse_message_level(self, level):
        ret_val = level

        if isinstance(ret_val, int):
            if (ret_val == 10) or (ret_val == 1):
                ret_val = 'DEBUG'
            elif (ret_val == 20) or (ret_val == 2):
                ret_val = 'INFO'
            elif (ret_val == 30) or (ret_val == 3):
                ret_val = 'WARN'
            elif (ret_val == 40) or (ret_val == 4):
                ret_val = 'ERROR'
            elif (ret_val == 50) or (ret_val == 5):
                ret_val = 'CRITICAL'
        else:
            if isinstance(ret_val, str) and (ret_val == 'WARNING'):
                ret_val = 'WARN'                
            
        return ret_val
    
    def _send_message(self, message):
        ret_val = False
        no_messager = False
        try:
            if Messager.queues is not None:
                queue = Messager.queues[message.queue]
                queue.put_nowait(message)

                # payload = f"Message sent: [{message.queue}] {message.topic} - {message.payload}"
                # print(payload)
            else:
                no_messager = True

            ret_val = True
        except Exception as e:
            no_messager = True
            
        if no_messager:
            payload = f"[{message.sender.upper()} -> {message.queue}]: {message.payload}"
            print(payload)

        return ret_val

    def _error_handler(self, details = None, queue = None):
        message = Message(payload = details, level = 40, topic = 'error')

        if queue is None:
            try:    queue = 'ErrorManager'
            except: queue = None
        
        self._send_message(message, queue)

class DSModule:
    def __init__(self):
        self._initialize = True

        self._tag       = ''
        self._register  = True
        self._caller           = ''
        self._caller_classname = ''
        self._classname        = ''
        self._basenames        = list()
        self._debug     = False
        self._verbose   = False
        self._config    = dict()
        self._payloads  = list()

        self._event = None

    @property
    def initialize(self):
        return self._initialize
    
    @initialize.setter
    def initialize(self, value):
        if isinstance(value, bool): self._initialize = value

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, value):
        self._tag = value
    
    @property
    def caller(self):
        return self._caller

    @caller.setter
    def caller(self, value):
        self._caller = value

    @property
    def caller_classname(self):
        return self._caller_classname

    @caller_classname.setter
    def caller_classname(self, value):
        self._caller_classname = value

    @property
    def register(self):
        return self._caller

    @register.setter
    def register(self, value):
        if isinstance(value, bool): self._register = value

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value
        
    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, value):
        if isinstance(value, dict):
            # self.concatenate_dictionaries(value, self.config)
            config, payloads = self.concatenate_dictionaries(value, self._config)
            self._config  = config
            self.payloads = payloads

    @property
    def payloads(self):
        return self._payloads
    
    @payloads.setter
    def payloads(self, value):
        if isinstance(value, str) or isinstance(value, tuple): value = [value]

        if isinstance(value, list):
            if bool(value): self._payloads += value
            else: self._payloads = list()
    
    @property
    def event(self):
        return self._event
    
    @event.setter
    def event(self, value):
        if callable(value): self._event = value
    
    @classmethod
    def concatenate_dictionaries(cls, parameters, ret_val = None):
        if not isinstance(ret_val, dict):
            ret_val = dict()

        ret_payloads = list()

        if isinstance(parameters, dict):
            for key, value in parameters.items():
                if isinstance(value, dict):
                    if not key in ret_val.keys():
                        ret_val[key] = dict()

                    # cls.concatenate_payloads(f"[EXPANDING {key}]")
                    ret_payloads.append(f"[EXPANDING {key}]")
                    ret_val[key], payloads = cls.concatenate_dictionaries(parameters = value, ret_val = ret_val[key])
                    ret_payloads += payloads
                else:
                    try:
                        ret_val[key] = value
                        # cls.concatenate_payloads(cls.create_parameter_payload(key, value))
                        ret_payloads.append(cls.create_parameter_payload(key, value))
                    except Exception as e:
                        pass
                
        return ret_val, ret_payloads

    @classmethod
    def create_parameter_payload(cls, key, value):
        if isinstance(value, list) and (len(value) > 5): value = 'DataTooLong'
    
        ret_val = f"  [PARAMETER CONFIGURATION] {key} = {value}"
        return ret_val

class ErrorHandler():
    # INTERFACES
    def get_error_info(self, details = None):
        ret_val = get_error_info()

        if not details is None:
            if isinstance(details, dict):
                for key, value in details.items(): ret_val[key] = value
            elif isinstance(details, str):
                ret_val['info'] = details
        
        return ret_val    

    # PARTICULAR
    def _get_error_info():
        type_error, value, traceback = exc_info() # most recent (if any) by default

        ret_val = {
            'filename' : traceback.tb_frame.f_code.co_filename,
            'function' : traceback.tb_frame.f_code.co_name,
            'lineno'   : traceback.tb_lineno,
            'msg'	   : value,
            'error'    : type_error,
        }

        if type_error == KeyError:
            ret_val['msg'] = f"KeyError {ret_val['msg']}"

        ret_val['filename'] = ret_val['filename'].split('\\')[-1]

        return ret_val

def get_class_herency(obj = None):
    if not obj is None:
        # Classname
        classname = type(obj).__name__
        # Basename
        bns       = type(obj).__bases__
        basenames = list()
        name = bns[0].__name__
        while not name == 'object':
            basenames.append(name)
            bns = bns[0].__bases__
            name = bns[0].__name__
        basenames.reverse()

        if not basenames: basenames = [classname]

        ret_val = [classname, basenames]
    else:
        ret_val = None
    
    return ret_val

def get_error_info():
    error_type, value, traceback = exc_info() # most recent (if any) by default

    ret_val = {
        'filename' : traceback.tb_frame.f_code.co_filename,
        'function' : traceback.tb_frame.f_code.co_name,
        'lineno'   : traceback.tb_lineno,
        'msg'	   : value,
        'error'    : error_type,
    }

    if error_type == KeyError:
        ret_val['msg'] = f"KeyError {ret_val['msg']}"

    ret_val['filename'] = ret_val['filename'].split('\\')[-1]

    return ret_val


@dataclass
class Checker:
    # _c: field(default_factory=list)
    _c: List = field(default_factory=lambda: [])

    @property
    def c(self):
        return self._c
    
    @c.setter
    def c(self, value):
        if self._c is None: self._c = list()

        if isinstance(value, bool):
            self._c.append(value)
    
    @property
    def c_and(self):
        value = all(self._c)
        self.clear
        self._c = [value]
        return value


    @property
    def c_or(self):
        value = any(self._c)
        self.clear
        self._c = [value]
        return value

    @property
    def clear(self, value = None):
        self._c = list()
        return self._c
