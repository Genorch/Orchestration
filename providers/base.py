import abc
import importlib


class BaseProvider(abc.ABCMeta):
    providers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.providers[instance.name] = instance

        return instance

    @classmethod
    def get(cls, name):
        if name not in cls.providers:
            try:
                importlib.import_module('providers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.providers[name]


class Provider(metaclass=BaseProvider):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
