/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKGeneratorConfig(variant){
    var config = {};
    if (variant === "data"){
        config = {
                    path: null,
                    wait: 1,
                    data: null
        }
    }

    this.updateConfigForm = function(config, wait){
        setFormInputValue(wait || "waitInput", config.wait);
    };

    this.extractConfig = function(wait){
        config.wait = getFormInputValue(wait || "waitInput", undefined, parseFloat);
    };

    this.loadData = function(event, raiseAlert, alertMsg){
        var file = event.target.files[0];
        if (file){
            var reader = new FileReader();
            reader.onload = function(e){
                config.path = file.name;
                config.data = e.target.result;
                if (raiseAlert) {
                    alert(alertMsg || "CSV File "+file.name+" successfully loaded.")
                }
            };
            reader.readAsText(file);
        } else {
            if (raiseAlert) {
                alert("Failed to load CSV File.")
            }
        }
    };

    this.getConfig = function(){
        return config;
    }
}