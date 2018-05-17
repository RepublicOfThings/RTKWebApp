/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKPipeConfig(variant){
    var config = {};
    if (variant === "kalman"){
        config = {
                    burn: 0,
                    n: 1,
                    m: 1,
                    qs: 1,
                    rs: 1
        }
    }

    this.updateConfigForm = function(config, burn, obs, hid, proc, meas){
        setFormInputValue(burn || "burnInput", config.burn);
        setFormInputValue(obs || "obsInput", config.n);
        setFormInputValue(hid || "hidInput", config.m);
        setFormInputValue(proc || "procInput", config.qs);
        setFormInputValue(meas || "measInput", config.rs);
    };

    this.extractConfig = function(burn, obs, hid, proc, meas){
        config.burn = getFormInputValue(burn || "burnInput", undefined, parseInt);
        config.n = getFormInputValue(obs || "obsInput", undefined, parseInt);
        config.m = getFormInputValue(hid || "hidInput", undefined, parseInt);
        config.qs = getFormInputValue(proc || "procInput", undefined, parseInt);
        config.rs = getFormInputValue(meas || "measInput", undefined, parseInt);
        return config;
    };

    this.getConfig = function(){
        return config;
    }

}
