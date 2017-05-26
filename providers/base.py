import abc
import importlib


class BaseDriver(abc.ABCMeta):
    drivers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.drivers[instance.name] = instance

    @classmethod
    def get(cls, name):
        if name not in cls.things:
            try:
                importlib.import_module('drivers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.things[name]


class Driver(metaclass=BaseDriver):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
