/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKClientConfig(variant, subPrefix, pubPrefix){
    var subPrefix = subPrefix || "/rtk/mqtt/";
    var pubPrefix = pubPrefix || "/rtk/mqtt/";
    this.config = {
        port: 1883,
        host: "iot.eclipse.org",
        client_id: "",
        clean_session: true,
        protocol: 4,
        transport: "tcp",
        subscriptions: [],
        topics: [],
        userdata: null
    };

    this.updateConfigForm = function(config, port, host, subs, pubs) {
        setFormInputValue(port || "portInput", config.port);
        setFormInputValue(host || "hostInput", config.host);
        if (config.subscriptions.length > 0){
            var sub = config.subscriptions[0].topic.slice(3+"rtk/mqtt/".length, config.subscriptions[0].topic.length);
            setFormInputValue(subs || "subInput", sub);
        }
        var pub = config.topics[0].slice(3+"rtk/mqtt/".length, config.topics[0].length);
        setFormInputValue(pubs || "pubInput", pub);
    };

    this.extractConfig = function(port, host, client_id, subs, pubs){
        this.config.port = getFormInputValue(port || "portInput");
        this.config.host = getFormInputValue(host || "hostInput");
        if (variant === "filter"){
            this.config.client_id = "f:"+getFormInputValue(client_id)
        } else {
            this.config.client_id = "s:"+getFormInputValue(client_id)
        }
        this.config.subscriptions = this.extractSubscribe(subs || "subInput");
        this.config.topics = this.extractPublish(pubs || "pubInput");

    };

    this.extractSubscribe = function(subs){
        if (variant === "filter") {
            return [{topic: subPrefix+"s:"+getInputValue(subs), qos:2}]
        } else {
            return []
        }
    };

    this.extractPublish = function(pubs){
        if (variant === "filter") {
            return [pubPrefix+"f:"+getInputValue(pubs)]
        } else {
            return [pubPrefix+"s:"+getInputValue(pubs)]
        }
    };

    this.getConfig = function(){
        return this.config;
    };

}