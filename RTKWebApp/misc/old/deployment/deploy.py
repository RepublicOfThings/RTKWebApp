from rtk import Filter, Sensor
from rtk.instances import instance as dev, errors
from .base import BaseInstanceManager


ACTIVE_PROCESS = 1
INACTIVE_PROCESS = 0
UNINIT_PROCESS = -1


MSG = {
        "stopped": "Stopped '{0}'.",
        "started": "Started '{0}'.",
        "created": "Deployed '{0}'.",
        "start_error": "Failed to start '{0}': {1}.",
        "restart_error": "Failed to restart '{0}': {1}.",
        "stop_error": "Failed to stop '{0}': {1}."
    }


def error_handler(func):
    def wrapped(*args, **kwargs):
        """
        
        Parameters
        ----------
        try:
            return func(*args, **kwargs)
        except errors.RTKInstanceError as error:
            return {"status": dev.ERROR, "msg": error.message}
        except errors.RTKConfigurationError as error:
            return {"status": dev.ERROR, "msg": error.message}
        except Exception as error:
            return {"status": dev.ERROR, "msg": error.message}

        Returns
        -------

        """
        return func(*args, **kwargs)
    return wrapped


class InstanceManager(BaseInstanceManager):
    __variants = {"sensor": Sensor, "filter": Filter}
    __codes = {"abort": "lemontree", "reset": "eisenhower"}

    def __init__(self, *args, **kwargs):
        super(InstanceManager, self).__init__(*args, **kwargs)

    @error_handler
    def create(self, variant, **kwargs):
        id_ = kwargs.get("id")
        if self._exists(id_):
            raise errors.RTKInstanceError("Could not create instance: instance with id {0} already exists.".format(id_))
        else:
            instance = self.__variants[variant].from_dict(kwargs)
            self._instances.add(instance)
            self._log(MSG["created"].format(instance.id))
            return instance.status

    @error_handler
    def start(self, id_, **kwargs):

        process = self._process(id_)

        try:

            if process is None or not process.is_alive():
                self._log("Starting Process {0}: No existing process found, starting a new one.".format(id_))
                self._instances.link_process(id_, self._instance(id_).start())
                self.instance(id_).state = dev.ACTIVE
                return "started instance '{0}'".format(id_)
            else:
                self._log("Starting Process {0}: Encountered a fatal error.".format(id_))
                raise errors.RTKInstanceError(MSG["start_error"].format(id_, "The instance is already active"))

        except Exception as e:
            raise e

    @error_handler
    def restart(self, id_):
        try:
            process = self._process(id_)
        except Exception as e:
            raise errors.RTKInstanceError("SUPER SMASHING GREAT.")

        try:
            if process is not None or not process.is_alive():
                self._instances.link_process(id_, self._instance(id_).start())
                self.instance(id_).state = dev.ACTIVE
                return "restarted instance '{0}'".format(id_)
            else:
                raise errors.RTKInstanceError(MSG["start_error"].format(id_))
        except Exception as e:
            raise errors.RTKInstanceError("OTHER ERROR IN THIS BLOCK")

    @error_handler
    def stop(self, id_):
        process = self._process(id_)
        if process.is_alive():
            self._instances.process(id_).terminate()
            self.instance(id_).state = dev.PAUSED
            return "stopped instance '{0}'".format(id_)
        else:
            raise errors.RTKInstanceError("Failed to stop '{0}': it is either already stopped or uninitialised.".format(id_))

    @error_handler
    def start_all(self):
        return self.batch_execution(self.start)

    @error_handler
    def stop_all(self):
        return self.batch_execution(self.stop)

    @error_handler
    def delete_all(self):
        return self.batch_execution(self.delete)

    @error_handler
    def batch_execution(self, func, *args, **kwargs):
        responses = []
        for instance in self.instances:
            try:
                msg = func(instance.id, *args, **kwargs)
            except errors.RTKInstanceError as error:
                msg = {"id": instance.id, "status": dev.ERROR, "config": {"msg": error}}
            except errors.RTKConfigurationError as error:
                msg = {"id": instance.id, "status": dev.ERROR, "config": {"msg": error}}
            finally:
                responses.append(msg)
        return responses

    @error_handler
    def delete(self, id_):
        try:
            if self._process(id_) is not None and self._process(id_).is_alive():
                self.stop(id_)
        finally:
            self._instances.remove(id_)

    @error_handler
    def abort(self, code):
        if code == self.__codes["abort"]:
            return self._instances.clear()
        else:
            raise errors.RTKAuthorisationError("Invalid pass code for abort command.")

    @error_handler
    def reset(self, code):
        if code == self.__codes["reset"]:
            return self._instances.reset()
        else:
            raise errors.RTKAuthorisationError("Invalid pass code for reset command.")

    @error_handler
    def update(self, id_, **kwargs):
        if self._exists(id_):
            status = self._process_status(id_)
            instance = self._instance(id_)
            self._validate_update(instance, kwargs)
            if status == ACTIVE_PROCESS:
                self._log("Updating '{0}': Encountered active process - shutting it down.".format(id_))
                self.stop(id_)
                self._log("Updating '{0}': Updating the instance's configuration.".format(id_))
                instance.update_config(**kwargs)
                self._log("Updating '{0}': Restarting process...".format(id_))
                self.restart(id_)
                self._log("Updating '{0}': Restarted.".format(id_))
            else:
                self._log("Updating '{0}': Updating the instance's configuration.".format(id_))
                instance.update_config(**kwargs)
            try:
                self._instances.update_key(id_, instance.id)
            except KeyError as e:
                raise KeyError("BANG BANG")
        else:
            raise errors.RTKInstanceError("Couldn't update '{0}': No such instance exists.".format(id_))

    @error_handler
    def cache(self, id_):
        try:
            return self._instance(id_).cache
        except AttributeError:
            raise errors.RTKInstanceError("Instance '{0}' does not have an accessible data cache.".format(id_))

    @error_handler
    def available(self, summary=True):
        if summary:
            output = []
            for instance in self.instances:
                status = {k: v for k, v in instance.status.items() if k != "config"}
                status["name"] = instance.status["config"]["name"]
                output.append(status)
            return output
        else:
            return [x.status for x in self.instances]

    def inputs(self, id_):
        return {"id": id_, "inputs": self.instance(id_).inputs}

    def outputs(self, id_):
        return {"id": id_, "outputs": self.instance(id_).outputs}

    def to_json(self):
        pass

    def to_dict(self):
        pass

    @classmethod
    def from_json(cls):
        pass

    @classmethod
    def from_dict(cls):
        pass

    def _validate_update(self, instance, kwargs):
        old_id, new_id = instance.id, kwargs.get("id")
        if new_id is not None:
            if old_id != new_id:
                if new_id in self.ids:
                    msg = "Invalid Update '{0}': new id '{1}' is not unique.".format(old_id, new_id)
                    raise errors.RTKInstanceError(msg)
