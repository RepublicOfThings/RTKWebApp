"""
Taken from 'Nix (Version 0.0.5)'
Copyright Mark Douthwaite 2017
Permission is not granted to replicate, or disseminate this code.
"""

import sys
import os
import json
import csv
import io


class Stream(object):
    def __init__(self, sid=-1, forget=False, authorise=False):
        self._current = None
        self.id = sid
        self.forget = forget
        self.authorised=authorise
        self._data = []

    @property
    def current(self):
        if isinstance(self._current, csv.DictReader):
            self._current = [x for x in self._current]
        return self._current

    @current.setter
    def current(self, obj):
        self._current = obj

    @property
    def set(self):
        return self._data

    def ingest(self, source=None, content_type=None, stdin=False, data=None, **kwargs):
        if source:
            self.__file_data(source, content_type, **kwargs)
        elif stdin:
            self.__stdin_data(content_type)
        elif data:
            if content_type is "json":
                self._current = json.loads(data)
            elif content_type is "csv":
                self._current = csv.reader(io.StringIO(data))
            else:
                self._current = data
        else:
            raise ValueError("Stream {0}: Invalid ingestion configuration.".format(self.id))

        if not self.forget:
            self._data.append(self.current)
        else:
            self._data = self.current

    def __file_data(self, source, file_type, persist=True):
        target = open(source, 'rU')

        if file_type == "json":
            self._current = json.load(target)
        elif file_type == "csv":
            self._current = csv.DictReader(target)
        else:
            self._current = target.read()

        if not persist:
            os.remove(source)

    def __stdin_data(self, content_type):
        if content_type is "json":
            self._current = json.load(sys.stdin)
        elif content_type is "csv":
            self._current = csv.DictReader(sys.stdin)
        else:
            self._current = sys.stdin.read()

    def pipe(self, i=None, o=None):

        if i is not None and isinstance(i, dict):
            self.ingest(**i)

        # do something?

        if o is not None and isinstance(o, dict):
            return self.egest(**o)

    def egest(self, target=None, stdout=False, overwrite=True, content_type=None, suffix=None, data=False, **kwargs):
        if stdout:
            sys.stdout.write(self.current)
        if data:
            return self.current
        elif target is not None:
            filepath, filename = os.path.split(target)
            if not os.path.exists(filepath) and filepath != "":
                if self.authorised:
                    os.makedirs(filepath)
                else:
                    user = input("Stream {0}: No such directory '{1}', create directory? Y/n".format(self.id, filepath))
                    if user == "Y":
                        os.makedirs(filepath)
                    else:
                        raise IOError("Stream {0}: Could not write out due to invalid filepath {1}.".format(self.id, filepath))

            if os.path.isfile(filename):
                if not overwrite and suffix is None:
                    raise IOError("Stream {0}: Could not write to file -- specify unique file name.".format(self.id))

            if suffix is not None:
                filename, ext = os.path.splitext(filename)
                filename += suffix
                filename += ext

            target = filepath + "/" + filename

            if content_type == "json":
                jstream = kwargs.get("json_stream") or None
                if jstream is not None:
                    f = open(target, "a")
                    json_str = json.dumps(self.current)+"\n"
                    f.write(json_str)
                else:
                    json.dump(self.current, open(target, 'w'), **kwargs)

            elif content_type == "csv":
                if issubclass(type(self.current), dict):
                    keys = [str(x) for x in self.current.keys()]
                    target_file = csv.DictWriter(open(target, 'w'), fieldnames=keys, **kwargs)
                else:
                    target_file = csv.DictWriter(open(target, 'w'), fieldnames=self.current[0].keys(), **kwargs)
                target_file.writeheader()
                target_file.writerows(self.current)

            else:
                open(target, 'w').write(self._current)


