import json
from .call import CallBuilder
from requests import Session


class API(object):
    def __init__(self,
                 auth=(),
                 target="http://api.douthwaite.io/rtk"):
        """
        A simple API wrapper for the RTK REST API. 
        
        Parameters
        ----------
        auth:
        target: str
            The target (i.e. base) url for the API.
            
        Examples
        --------
        >>> config = json.load(open("filter_config.json", "r"))  # filter with id 'f:0'
        >>> api = API(target="localhost:8080")
        >>> api.post.create.filter(data=config)  # returns requests Response object.
            <Response[200]>
        >>> api.post.start(params="i=f:0")
            <Response[200]>
        >>> api.instance(params="i=f:0")  # get the current configuration of the filter instance (1)
            <Response[200]>
            
        Notes
        -----
        (1) Unless specified, calls will be made using the 'get' method by default.
            
        """

        self._session = Session()
        self._target_url = target
        self._auth = auth

    @property
    def target(self):
        """
        Get the target url for the wrapper.
        
        Returns
        -------
        out: str
            The target url.

        """
        return self._target_url

    def __call__(self, path, method="GET", suffix="", unpack=False, **kwargs):
        """
        Makes a call to the target_url provided.

        Parameters
        ----------
        path: str
            The url path for the current API call.
        method: str
            The method to be used for the API call.
        suffix: str
            A suffix to be applied to the url.

        Returns
        -------
        resp: Session.request
            The response to the API call made through the requests.Session object.


        """
        url = "{base}/{path}{suffix}".format(**{"base": self._target_url,
                                                "path": path,
                                                "suffix": suffix})

        if not unpack:
            return self._session.request(method, url, **kwargs)
        else:
            return json.loads(self._session.request(method, url, **kwargs).content)

    @property
    def get(self):
        """
        Helper method, prepares a GET request.
        """
        return CallBuilder(self)

    @property
    def post(self):
        """
        Helper method, prepares a POST request.
        """
        return CallBuilder(self, method='POST')

    def __getattr__(self, item):
        """
        Provides access to a CallBuilder. Intended to make a simple, intuitive approach to building request urls.

        Parameters
        ----------
        item: str
            An url element.

        Returns
        -------
        call_element: CallBuilder
            The base element of an API call.

        Examples
        --------

        """
        return CallBuilder(self, path=item)

    def __getitem__(self, item):
        """
        An alternate method for building paths.
        
        Parameters
        ----------
        item: str
            An url element.
            
        Returns
        -------
        out: CallBuilder
            The call builder associated with the current call path.

        """
        return self.__getattr__(item)
