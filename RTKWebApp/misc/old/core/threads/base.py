import threading
import multiprocessing


class RTKProcess(threading.Thread):
    def __init__(self, id_, *args, **kwargs):
        super(RTKProcess, self).__init__(*args, **kwargs)
        self.id = id_


def threaded(func):
    def wrapped_func(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapped_func


def parallel(func):
    def wrapped_func(*args, **kwargs):
        thread = multiprocessing.Process(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapped_func
