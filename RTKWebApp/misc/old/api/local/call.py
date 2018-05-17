

class CallBuilder(object):
    def __init__(self, client, path="", method="GET"):
        self.__client = client
        self.__path = path
        self.__method = method

    def __call__(self, *args, **kwargs):
        method = kwargs.get("method", None) or self.__method
        if self.__method == "POST":
            self.__path = self.__path[1:]
        return self.__client(self.__path, method=method, **kwargs)

    def __getattr__(self, item):
        return CallBuilder(self.__client, "{0}/{1}".format(self.__path, item), method=self.__method)