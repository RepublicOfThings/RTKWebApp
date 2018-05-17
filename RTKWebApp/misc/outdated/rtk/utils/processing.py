import pandas as pd
from .errors import JSONParsingError
import json


def unpack_sensors(filename, target="temp"):
    """
    Helper function to unpack a sensor csv file into a Python dictionary.
    Note: this helper function only supports extracting a single feed from the csv file.

    Parameters
    ----------
    filename : string
        String containing the path to the target file.
    target : string, optional
        String indicating the column heading to extract from the csv file.

    Returns
    -------
    dict : dictionary
        Contains map of {'apartment_str': apartment_data}.

    """
    data = pd.DataFrame.from_csv(filename)
    apartments = data.apartment.unique()
    return {k: list(data[data.apartment == k][target].values) for k in apartments}


def json_message(func):
    """
    Decorator for Thing-like objects, parses any messages as json and converts to dict. (target: Thing.on_message)

    Decorated methods will receive a dictionary and should return either a dictionary or a valid JSON string.

    """
    def wrapped_method(obj, socket, message, *args, **kwargs):

        if not isinstance(type(message), str):
            message = str(message).decode("utf-8")

        try:
            json_msg = json.loads(message)
        except ValueError as error:
            error.message += " in JSON({0})".format(message)
            raise JSONParsingError(error.message)

        output = func(obj, socket, json_msg, *args, **kwargs)

        try:
            if isinstance(output, dict):
                output = json.dumps(output)
            json.loads(output)  # check it is valid JSON.
        except ValueError as error:
            error.message += " in JSON({0})".format(output)
            raise JSONParsingError(error.message)

        return output

    return wrapped_method


def json_output(func):
    """
    Decorator for Thing-like objects, converts output data to stringified JSON data. (target: Thing.send)

    """
    def wrapped_method(obj, data, *args, **kwargs):

        try:
            if isinstance(data, dict):
                data = json.dumps(data)
            json.loads(data)  # check it is valid JSON.
        except ValueError as error:
            error.message += " in JSON({0})".format(data)
            raise JSONParsingError(error.message)

        return func(obj, data, *args, **kwargs)

    return wrapped_method


def mqtt_json_input(func):
    """
    Converts MQTT message from JSON to dict.
    """
    def wrapped_method(self, client, user_data, message):
        message = json.loads(message.payload)
        return func(self, client, user_data, message)
    return wrapped_method

