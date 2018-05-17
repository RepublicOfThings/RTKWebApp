from rtk import RTKFilter, RTKSensor
from apogee.tools import deprecated
from rtk.instances import instance as dev, errors
import logging
import json
import uuid


ACTIVE_PROCESS = 1
INACTIVE_PROCESS = 0
UNINIT_PROCESS = -1


def error_handler(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except errors.RTKInstanceError as error:
            return error
        except errors.RTKConfigurationError as error:
            return error
    return wrapped


class RTKInstanceManager(object):

    __instance_objects = {"sensor": RTKSensor, "filter": RTKFilter}

    def __init__(self, headers=None, level=logging.DEBUG, max_load=50):
        self._instances = {}
        self._headers = headers or {}
        self._logger = logging.getLogger("{0}({1})".format(RTKInstanceManager.__name__, str(uuid.uuid4())))
        self._max_load = max_load
        logging.basicConfig(level=level)

    # Core methods

    @property
    def instance_count(self):
        return len(self._instances)

    @property
    def process_count(self):
        return [x for x in self._instances if x["process"] is not None]

    @property
    def instance_ids(self):
        return list(self._instances.keys())

    @error_handler
    def add(self, variant, **kwargs):
        id_ = kwargs.get("id")
        if self._check_unique(id_):
            instance = self.__instance_objects[variant].from_dict(kwargs)
            self._acquire_instance(instance)
        else:
            raise errors.RTKConfigurationError("An instance with id {0} has already been deployed.".format(id_))

    def restart(self, id_, throw=False):
        if self._process(id_) is not None:
            self.start(id_)
        else:
            if throw:
                msg = "Restart Error: Could not restart '{0}' - process must be started normally first".format(id_)
                raise errors.RTKInstanceError(msg)
            else:
                return self._instance(id_).status

    @error_handler
    def update(self, id_, **kwargs):
        if self._check_exists(id_):

            init_status = self._process_status(id_)

            if init_status == ACTIVE_PROCESS:
                self.stop(id_)  # stop if the instance is active

            instance = self._instance(id_)
            self._validate_update(instance, kwargs)
            instance.update_config(**kwargs)

            if init_status == ACTIVE_PROCESS:
                self.restart(id_)  # restart if the instance was inactive

        else:
            raise errors.RTKInstanceError("UpdateError: Could not update '{0}' - instance does not exists.".format(id_))

    def remove(self, id_):
        if self._instances.get(id_, None) is not None:
            # stop the instance's associated processes if they're alive.
            if self._process_status(id_) == ACTIVE_PROCESS:
                self.stop(id_)
            # cleanup
            del self._instances[id_]
            self._log("Deleted instance with id: {0}".format(id_))
        return {"id": id_, "status": dev.DELETED, "config": None}

    def launch(self):
        statuses = []
        for id_ in self._instances.keys():
            try:
                statuses.append(self.start(id_))
            except:
                statuses.append({"id": id_, "status": dev.ERROR, "config": None})
        return statuses

    def shutdown(self):
        statuses = []
        for id_ in self._instances.keys():
            try:
                statuses.append(self.stop(id_))
            except:
                statuses.append({"id": id_, "status": dev.ERROR, "config": None})
        return statuses

    def stop(self, id_):
        process = self._process(id_)
        instance = self._instance(id_)
        if process is not None:
            if process.is_alive():
                process.terminate()
                self._log("Stopped instance with id: {0}".format(id_))
                instance.state = dev.PAUSED
            else:
                self._log("Failed to stop instance with id: {0}".format(id_))
                raise errors.RTKInstanceError(
                    "ThreadError: Failed to stop Instance {0}. It has already been stopped.".format(id_))

        return instance.status

    def start(self, id_):
        instance = self._instance(id_)
        process = self._process(id_)
        if process is None:
            self._instances[id_]["process"] = instance.start()
            self._log("Started instance with id: {0}".format(id_))
        elif instance.state == dev.PAUSED:
            self._instances[id_]["process"] = self._instances[id_]["object"].start()
        elif process.is_alive():
            raise errors.RTKInstanceError(
                "ThreadError: Failed to start Instance {0}. It has already been started.".format(id_))
        elif not process.is_alive():
            self._instances[id_]["process"] = self._instances[id_]["object"].start()
            self._log("Restarted instance with id: {0}".format(id_))

        instance.state = dev.ACTIVE
        return instance.status

    def instance(self, id_):
        for instance in self.instances():
            if instance.id == id_:
                return instance.status
        return json.dumps({"id": id_, "status": dev.ERROR, "config": {"msg": "no matching instance config available"}})

    @property
    def processes(self):
        return [x["process"] for x in self._instances.values()]

    def cache(self, id_):
        try:
            return self._instance(id_).cache
        except AttributeError:
            raise errors.RTKInstanceError("Instance '{0}' does not have an accessible data cache.")

    @property
    def filters(self):
        return [x["object"].status for x in self._instances.values() if isinstance(x["object"], RTKFilter)]

    @property
    def sensors(self):
        return [x["object"].status for x in self._instances.values() if isinstance(x["object"], RTKSensor)]

    def instances(self, unpack=False):
        if not unpack:
            return [x["object"] for x in self._instances.values()]
        else:
            return [x["object"].status for x in self._instances.values()]

    # I/O methods

    def load(self, variant, path, launch=False):
        data = json.load(open(path, "r"))
        return self.add(variant, **data)

    @classmethod
    def from_json(cls, string, launch=False, **kwargs):
        data = json.loads(string)

        net = cls(headers=data["headers"])

        for config in data["filters"]:
            net.add("filter", **config)

        for config in data["sensors"]:
            net.add("sensor", **config)

        return net

    def to_json(self, path=None, **kwargs):
        if path is None:
            return json.dumps(self.to_dict(), **kwargs)
        else:
            return json.dump(self.to_dict(), open(path, "w"), **kwargs)

    def to_dict(self):
        data = {"filters": [], "sensors": [], "headers": self._headers}
        for instance in self.instances():
            if isinstance(instance, RTKFilter):
                data["filters"].append(instance.to_dict())
            elif isinstance(instance, RTKSensor):
                data["sensors"].append(instance.to_dict())
            else:
                raise TypeError("Invalid instance type: {0}".format(type(instance)))
        return data

    # Helper methods

    def _acquire_instance(self, instance):
        if self.instance_count < self._max_load:
            self._instances[instance.id] = {"object": instance, "process": None}
            self._log("Added instance: {0}".format(instance.id))
        else:
            raise errors.RTKManagerError("Failed to add instance '{0}': Max load reached.")

    def _validate_update(self, instance, kwargs):
        old_id, new_id = instance.id, kwargs.get("id")
        if new_id is not None:
            if old_id != new_id:
                if new_id in self.instance_ids:
                    msg = "Invalid Update '{0}': new id '{1}' is not unique.".format(old_id, new_id)
                    raise errors.RTKInstanceError(msg)

    def _check_unique(self, id_):
        if id_ in self.instance_ids:
            return False
        else:
            return True

    def _check_exists(self, id_):
        if id_ in self.instance_ids:
            return True
        else:
            return False

    def _log(self, message, level=logging.DEBUG):
        self._logger.log(level, message)

    def _process_status(self, id_):
        if self._process(id_) is None:
            return UNINIT_PROCESS
        elif self._process(id_).is_alive():
            return ACTIVE_PROCESS
        else:
            return INACTIVE_PROCESS

    def _process(self, id_):
        return self._instances[id_].get("process", None)

    def _instance(self, id_):
        return self._instances[id_].get("object", None)

    def __getitem__(self, item):
        for instance in self.instances():
            if instance.id == item:
                return instance

    def __repr__(self):
        return "{0}(Sensors: {1}, Filters: {2})".format(type(self).__name__,
                                                        len(self.sensors),
                                                        len(self.filters))

    # Deprecated methods

    @deprecated
    def _update(self, instance, launch=False):
        self._instances[instance.id] = {}
        self._instances[instance.id]["object"] = instance
        if launch:
            self.start(instance.id)
        self._log("Added instance: {0}".format(instance.id))
        return instance.status

    @deprecated
    def _handle_update(self, instance, launch):
        if len(self.instances()) >= self._max_load:
            raise errors.RTKInstanceError(
                "MaxLoad: Could not add {0}, delete instances to add more.".format(instance.id))

        if isinstance(instance, dict):
            raise errors.RTKInstanceError("Error" + instance["error"])

        if self._is_unique(instance):
            return self._update(instance, launch)
        else:
            raise errors.RTKInstanceError("ID: A instance with id '{0}' has already been deployed.".format(instance.id))

    @deprecated
    def _is_unique(self, instance):
        for other in self.instances():
            if instance.id == other.id:
                return False
        return True

    @deprecated
    def _update(self, id_, **kwargs):

        try:
            if self._instances.get(id_, None) is not None:
                self._log("Updating instance '{0}'".format(id_))

                try:
                    self.stop(id_)
                except errors.RTKInstanceError as e:
                    self._log("Updating '{0}': Instance processes are already inactive or paused. ({1})".format(id_, e))

                instance = self._instance(id_)
                process_status = self._process_status(id_)
                if kwargs.get("id") is not None:
                    new_id = kwargs.get("id")
                    if new_id != id_:
                        if new_id in [x for x in self._instances.keys()]:
                            raise errors.RTKInstanceError("Could not update instance with id '{0}', the new id '{1}' is not unique.".format(id_, new_id))

                instance.update_config(**kwargs)
                if process_status != UNINIT_PROCESS:
                    try:
                        self.start(id_)
                    except errors.RTKInstanceError as e:
                        self._log("Updating '{0}': Instance processes are already inactive or paused. ({1})".format(id_, e))
                else:
                    self._log("Updating '{0}': Don't need to restart this instance. Woop.".format(id_))

            else:
                raise errors.RTKInstanceError("UpdateError: Could not update '{0}' - no such instance exists.".format(id_))

        except Exception as e:
            raise errors.RTKInstanceError("UpdateError: Could not update '{0}' - encountered unknown error. ({1})".format(id_, e))
