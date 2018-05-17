import copy


class InstanceStore(object):
    def __init__(self):
        self._data = {}

    def __getitem__(self, item):
        return self._data[item]

    def __setitem__(self, key, value):
        if key in self._data.keys():
            raise KeyError("Key must be unique.")
        else:
            self._data[key] = value

    def __len__(self):
        return len(self._data)

    def keys(self):
        return list([x for x in self._data.keys()])

    def values(self):
        return list([x for x in self._data.values()])

    def processes(self):
        return [v["process"] for v in self.values()]

    def objects(self):
        return [v["object"] for v in self.values()]

    def process(self, key):
        return self[key]["process"]

    def link_process(self, key, process):
        # p-c
        self[key]["process"] = process

    def object(self, key):
        return self[key]["object"]

    def add(self, obj, process=None, key=None):
        self[key or str(obj.id)] = {"object": obj, "process": process}

    def update_key(self, old_key, new_key):
        if old_key != new_key:
            self[new_key] = copy.copy(self[old_key])
            del self._data[old_key]

    def remove(self, key):
        del self._data[key]

    def clear(self):
        # check this works as intended
        self._data.clear()

    def reset(self):
        for key, value in self._data.items():
            print key, value["object"]
            self._data[key]["process"] = None
            self._data[key]["object"] = type(value["object"]).from_dict(value["object"].to_dict())
