from pyrestful.rest import RestHandler, get, post, delete, mediatypes
from rtk.deployment import InstanceManager
from rtk.instances import errors
import rtk
from .response import ResponseModel
import json
import uuid


MANAGER = InstanceManager()


class RESTHandler(RestHandler):
    def __init__(self, *args, **kwargs):
        """
        A REST interface handler for interactions with the RTKInstanceManager object.
                
        See Also
        --------
        pyrestful.rest.RestHandler
        
        """

        super(RESTHandler, self).__init__(*args, **kwargs)
        self.__manager = MANAGER

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    @get(_path="/rtk/status", _produces=mediatypes.APPLICATION_JSON)
    def status(self):
        """
        Request the status of the REST API.
        
        Returns
        -------
        out: None

        """
        return self.write(ResponseModel(0, "okay", {"version": rtk.__version__, "status": 0}).json)

    @get(_path="/rtk/uuid/{obj}", _produces=mediatypes.APPLICATION_JSON)
    def generate_uuid(self, obj):
        return self._handle_request(lambda: str(uuid.uuid4()))

    @get(_path="/rtk/instance",
         _types=[str],
         _produces=mediatypes.APPLICATION_JSON)
    def instance(self, i):
        return self._handle_request(self.__manager.status, i)

    @get(_path="/rtk/instance/cache",
         _types=[str],
         _produces=mediatypes.APPLICATION_JSON)
    def cache(self, i):
        return self._handle_request(self.__manager.cache, i)

    @get(_path="/rtk/instance/inputs", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def inputs(self, i):
        return self._handle_request(self.__manager.inputs, i)

    @get(_path="/rtk/instance/outputs", _types=[str], _produces=mediatypes.APPLICATION_JSON)
    def outputs(self, i):
        return self._handle_request(self.__manager.outputs, i)

    @get(_path="/rtk/instances", _produces=mediatypes.APPLICATION_JSON)
    def instances(self):
        return self._handle_request(self.__manager.available, summary=True)

    @post(_path="/rtk/update",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def update(self, i):
        return self._handle_request(self.__manager.update, i, **json.loads(self.request.body))

    @post(_path="/rtk/create/{obj}",
          _produces=mediatypes.APPLICATION_JSON)
    def create_object(self, obj):
        return self._handle_request(self.__manager.create, obj, **json.loads(self.request.body))

    @post(_path="/rtk/start",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def start(self, i):
        if i == "all":
            return self._handle_request(self.__manager.start_all)
        else:
            return self._handle_request(self.__manager.start, i)

    @post(_path="/rtk/stop",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def stop(self, i):
        if i == "all":
            return self._handle_request(self.__manager.stop_all)
        else:
            return self._handle_request(self.__manager.stop, i)

    @post(_path="/rtk/delete",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def terminate(self, i):
        if i == "all":
            return self._handle_request(self.__manager.delete_all)
        else:
            return self._handle_request(self.__manager.delete, i)

    @post(_path="/rtk/reset",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def reset(self, auth):
        self._handle_request(self.__manager.reset, auth)

    @post(_path="/rtk/abort",
          _types=[str],
          _produces=mediatypes.APPLICATION_JSON)
    def abort(self, auth):
        self._handle_request(self.__manager.abort, auth)

    def _handle_request(self, method, *args, **kwargs):
        message = ResponseModel(-2, "UnknownError", "Encountered and unknown error.")
        try:
            message = ResponseModel(0, "okay", method(*args, **kwargs))
        except errors.InstanceError as e:
            message = ResponseModel(-2, e.message, "An error occurred with the target instance.")
        except errors.ConfigurationError as e:
            message = ResponseModel(-2, e.message, "A configuration error occurred with the target instance.")
        except errors.AuthorisationError as e:
            message = ResponseModel(-2, e.message, "An authorisation error occurred.")
        except Exception as e:
            message = ResponseModel(-2, type(e).__name__, e.message)
        finally:
            return self.write(message.json)

