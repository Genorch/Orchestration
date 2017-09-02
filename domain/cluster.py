from cluster_providers.base import BaseProvider
from database import db
from utils import common


class Cluster:
    def __init__(self, _id, vms, provider):
        self._id = _id
        self.vms = vms
        self.provider = BaseProvider.get(provider)(self.vms)

    def create(self):
        self.cluster = self.provider.create_cluster()

        # Store the created cluster inside database
        cluster_data = {
            "_id": self._id,
            "vms": self.vms,
            "provider": self.provider.name
            }

        db.clusters.insert(cluster_data)

    def add_worker(self, vm_id):
        pass

    def add_manager(self, vm_id):
        pass

    def delete(self):
        self.provider.delete_server(self._id)
