import abc
import importlib


class BaseProvider(abc.ABCMeta):
    drivers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.drivers[instance.name] = instance

    @classmethod
    def get(cls, name):
        if name not in cls.things:
            try:
                importlib.import_module('providers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.things[name]


class Driver(metaclass=BaseProvider):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
