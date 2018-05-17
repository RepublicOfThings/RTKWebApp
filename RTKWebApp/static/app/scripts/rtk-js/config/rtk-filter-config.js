/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKFilterHelper(api, refresh){
    var configData;
    var rtkApi = api|| new RTKInterface();
    var client = new RTKClientConfig("filter");
    var filter = new RTKPipeConfig();

    this.refreshIfRequired = function (name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas) {
        if (configData === undefined){
            this.refreshConfig(name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas);
        }
    };

    this.refreshConfig = function(name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas){
        configData = {};
        client.extractConfig(port, host, uuid, subs, pubs);
        filter.extractConfig(burn, obs, hid, proc, meas);
        configData.name = getFormInputValue(name || "nicknameInput");
        configData.id = "f:"+getFormInputValue(uuid || "uuidInput");
        configData.filter_type = type || "kalman";
        configData.client = client.getConfig();
        configData.client.client_id = configData.id;
        configData.filter = filter.getConfig();
        return configData
    };

    this.updateConfigForm = function(config, name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas){
        setFormInputValue(name || "nicknameInput", config.name);
        setFormInputValue(uuid || "uuidInput", config.id.slice(2, config.id.length));
        client.updateConfigForm(config.client, host, port, subs, pubs);
        filter.updateConfigForm(config.filter, burn, obs, hid, proc, meas);
        this.refreshConfig(name, uuid);
    };

    this.status = function(api, previousId, callback, raiseAlert){
        this.refreshIfRequired();
        getInstance(previousId || configData.id, api || rtkApi, callback, raiseAlert)
    };

    this.update = function(previousId, api, callback, raiseAlert){
        this.refreshConfig();
        updateInstance(configData.id, previousId, configData, api || rtkApi, callback, raiseAlert);
    };

    this.create = function(variant, api, callback, raiseAlert){
        this.refreshIfRequired();
        createInstance(variant, configData, api || rtkApi, callback, raiseAlert)
    };

    this.start = function(previousId, api, callback, raiseAlert){
        this.refreshIfRequired();
        startInstance(configData.id, api || rtkApi, callback, raiseAlert)
    };

    this.stop = function(previousId, api, callback, raiseAlert){
        this.refreshIfRequired();
        stopInstance(configData.id, api || rtkApi, callback, raiseAlert);
    };

    this.kill = function(target, api, callback, raiseAlert){
        this.refreshIfRequired();
        deleteInstance(target, api || rtkApi, callback, raiseAlert)
    };

    this.getConfig = function(){
        return configData;
    };

    this.setConfig = function(config){
        configData = config;
    };

    if (refresh){
        this.refreshConfig();
    }

}