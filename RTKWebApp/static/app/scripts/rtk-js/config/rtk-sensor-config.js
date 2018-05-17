/**
 * Created by MarkDouthwaite on 03/08/2017.
 */



/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKSensorHelper(api, refresh){
    var configData;
    var rtkApi = api|| new RTKInterface();
    var client = new RTKClientConfig("sensor");
    var generator = new RTKGeneratorConfig("data");

    this.refreshIfRequired = function (name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas) {
        if (configData === undefined){
            this.refreshConfig(name, uuid, type, host, port, subs, pubs, burn, obs, hid, proc, meas);
        }
    };

    this.refreshConfig = function(name, uuid, type, host, port, subs, pubs, wait){
        configData = {};
        client.extractConfig(port, host, uuid, subs, pubs);
        generator.extractConfig(wait);
        configData.name = getFormInputValue(name || "nicknameInput");
        configData.id = "s:"+getFormInputValue(uuid || "uuidInput");
        configData.client = client.getConfig();
        configData.client.client_id = configData.id;
        configData.generator = generator.getConfig();
        configData.data_model = "apartment";
        configData.client_type = "mqtt";
        configData.gen_type = "data";
        return configData
    };

    this.updateConfigForm = function(config, name, uuid, host, port, subs, pubs, wait){
        setFormInputValue(name || "nicknameInput", config.name);
        setFormInputValue(uuid || "uuidInput", config.id.slice(2, config.id.length));
        client.updateConfigForm(config.client, host, port, subs, pubs);
        generator.updateConfigForm(config.generator, wait);
        this.refreshConfig(name, uuid);
    };

    this.status = function(api, previousId, callback, raiseAlert){
        this.refreshIfRequired();
        getInstance(previousId || configData.id, api || rtkApi, callback, raiseAlert)
    };

    this.update = function(previousId, api, callback, raiseAlert){
        this.refreshIfRequired();
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
        deleteInstance(target, api || rtkApi, callback, raiseAlert);
        // deleteInstance(configData.id, api || rtkApi, callback, raiseAlert)
    };

    this.getConfig = function(){
        return configData;
    };

    this.setConfig = function(config){
        configData = config;
    };

    this.loadData = function(event, raiseAlert, alertMsg){
        return generator.loadData(event, raiseAlert, alertMsg);
    };

    if (refresh){
        this.refreshConfig();
    }

}