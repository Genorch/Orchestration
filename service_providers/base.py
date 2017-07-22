import abc
import importlib


class BaseServiceProvider(abc.ABCMeta):
    service_providers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.service_providers[instance.name] = instance

        return instance

    @classmethod
    def get(cls, name):
        if name not in cls.service_providers:
            try:
                importlib.import_module('service_providers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.service_providers[name]


class ServiceProvider(metaclass=BaseServiceProvider):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
