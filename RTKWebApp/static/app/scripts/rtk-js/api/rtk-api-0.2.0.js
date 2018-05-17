/*
    A set of JavaScript functions and a wrapper for the RTK REST API.
 */

function RTKInterface(endpoint){
    // A jQuery-based HTTP interface wrapper for the RTK REST API.

    this.endpoint = endpoint;
    this.getRequest = function(path, data, handler){
        $.get(this.endpoint+path, data, function(data){
            handler(data);
        });
    };

    this.postRequest = function(path, data, handler){
        // console.log(this.endpoint, "|", this.endpoint+path);
        $.post(this.endpoint+path, data, function(data){
            handler(data)
        });
    };

    this.getInstanceIds = function(handler){
        this.getRequest("rtk/launch", null, handler);
    };

    this.getInstance = function(id, handler){
        // /rtk/instance/{id}
        this.getRequest("rtk/instance?i="+id, null, handler);
    };

    this.getInstances = function(handler){
        // /rtk/instance/{id}
        this.getRequest("rtk/launch", null, handler);
    };

    this.getInstanceCache = function(id, handler){
        this.getRequest("rtk/instance/cache?i="+id, null, handler);
    };

    this.getGenerateUUID = function(variant, handler){
        this.getRequest("rtk/uuid/"+variant, null, handler);
    };

    this.getApiStatus = function(handler){
        // /rtk/status
        this.getRequest("rtk/status", null, handler);
    };

    this.getInstanceInputs = function(id, handler){
        this.getRequest("rtk/instance/inputs?i="+id, null, handler);
    };

    this.getInstanceOutputs = function(id, handler){
        this.getRequest("rtk/instance/outputs?i="+id, null, handler);
    };

    this.postCreateInstance = function(variant, data, handler) {
        // /rtk/create/{variant}
        this.postRequest("rtk/create/"+variant, data, handler);
    };

    this.postStartInstance = function(id, handler) {
        // /rtk/start/{id}
        this.postRequest("rtk/start?i="+id, null, handler);
    };

    this.postStopInstance = function(id, handler) {
        // /rtk/stop/{id}
        this.postRequest("rtk/stop?i="+id, null, handler);
    };

    this.postUpdateInstance = function(id, data, handler) {
        // /rtk/stop/{id}
        this.postRequest("rtk/update?i="+id, data, handler);
    };

    this.postDeleteInstance = function(id, handler) {
        // rtk/delete?{id}
        this.postRequest("rtk/delete?i="+id, null, handler);
    };

    this.postStartInstances = function(handler){
        this.postRequest("rtk/start?i=all", null, handler);
    };

    this.postStopInstances = function(handler){
        this.postRequest("rtk/stop?i="+"all", null, handler);
    };

    this.postDeleteInstances = function(handler){
        this.postRequest("rtk/delete?i="+"all", null, handler);
    };

    this.postHardReset = function(code, handler){
        this.postRequest("rtk/reset?auth="+code, null, handler);
    };

    this.postForceQuit = function(code, handler){
        this.postRequest("rtk/abort?auth="+code, null, handler);
    };

    this.responseHandler = function(msg, callback, alertUser){
        // converts to json, handles errors.
        msg = JSON.parse(msg);
        if (msg.statusCode >= 0){
            if (alertUser !== undefined && alertUser === true) {
                alert("Successfully executed.");
            }

            if (callback !== undefined && callback !== null){
                // callback(msg);
            }
        } else {
            alert(msg.payload+"\n("+msg.responseMsg+")");
        }

    };

}


// API Helpers


function generateUUID(variant, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }
    api.getGenerateUUID(variant, function(msg){
        // console.log(msg);
        api.responseHandler(msg, callback, alertUser);
    });
}


function getInstance(instanceId, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }

    api.getInstance(instanceId, callback, function (msg) {
        api.responseHandler(msg, callback, alertUser);
    });
}


function createInstance(variant, config, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }
    config = JSON.stringify(config);
    api.postCreateInstance(variant, config, function(msg){
        api.responseHandler(msg, callback, alertUser);
    });
}


function startInstance(id, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }
    api.postStartInstance(id, function(msg){
        // console.log(callback, "internal");
        api.responseHandler(msg, callback, alertUser);
    });
}


function stopInstance(id, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }
    api.postStopInstance(id, function(msg){
        api.responseHandler(msg, callback, alertUser);
    });
}


function deleteInstance(id, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }

    api.postDeleteInstance(id, function(msg){
        api.responseHandler(msg, callback, alertUser);
    });
}


function updateInstance(id, oldID, config, api, callback, alertUser){
    if (api === undefined){
        api = new RTKInterface();
    }

    config = JSON.stringify(config);

    if (oldID !== "f:None" && oldID !== undefined && oldID !== "s:None"){
        id = oldID;
    }
    // console.log(id, oldID);
    api.postUpdateInstance(id, config, function(msg){
        api.responseHandler(msg, callback, alertUser);
    });
}