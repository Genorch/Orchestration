import abc
import importlib


class BaseClusterProvider(abc.ABCMeta):
    cluster_providers = {}

    def __new__(cls, name, bases, namespace):
        instance = abc.ABCMeta.__new__(cls, name, bases, namespace)

        if isinstance(instance.name, str):
            cls.cluster_providers[instance.name] = instance

        return instance

    @classmethod
    def get(cls, name):
        if name not in cls.cluster_providers:
            try:
                importlib.import_module('cluster_providers.%s' % name)
            except ImportError as e:
                print(e)
        return cls.cluster_providers[name]


class ClusterProvider(metaclass=BaseClusterProvider):
    def __init__(self):
        pass

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplemented()
