/**
 * Created by MarkDouthwaite on 17/07/2017.
 */



function RTKFormHelper(formById, variant){
    this.form = $("#"+formById);
    this.variant = variant;
    this.getValueById = function(){

    };
    this.setValueById = function(){

    };
    this.setElementStateById = function(){

    };
}


        var getKalmanConfig = function (){
            return {
                burn: getInputValue("optInput", undefined, parseInt),
                n: getInputValue("obsInput", undefined, parseInt),
                m: getInputValue("hiddenInput", undefined, parseInt),
                qs: getInputValue("processInput", undefined, parseFloat),
                rs: getInputValue("measureInput", undefined, parseFloat)
            }
        }



                var rest = new RTKInterface("http://localhost:8080/");
        var config = {};

        var getFilterConfig = function(){
            config.id = "f:"+getInputValue("uuidInput");
            config.name = getInputValue("nicknameInput");
            config.filter_type = "kalman";
            config.client = getClientConfig();
            config.filter = getKalmanConfig();
            config.client.client_id = config.id;
            console.log(config);
        };

        var displayMessage = function(msg){
            $.notify(msg, { allow_dismiss: false, type: 'success'});
        };

        var redirectUser = function(url){
            location.href = url;
        };


                    function updateConfiguration(data){
                        $("#nicknameInput").val(data.name);
                        $("#uuidInput").val(data.id.slice(2,data.id.length));
                        $("#hostInput").val(data.client.host);
                        $("#portInput").val(data.client.port);
                        var sub = data.client.subscriptions[0].topic.slice(3+"rtk/mqtt/".length, data.client.subscriptions[0].topic.length);
                        var pub = data.client.topics[0].slice(3+"rtk/mqtt/".length, data.client.topics[0].length);
                        $("#subInput").val(sub);
                        $("#pubInput").val(pub);
                        // $("#")
                        $("#processInput").val(parseFloat(data.filter.qs));
                        $("#measureInput").val(parseFloat(data.filter.rs));
                        $("#obsInput").val(data.filter.n);
                        $("#hiddenInput").val(data.filter.m);
                    }


                    // console.log("{{ id }}");
                    rest.getInstance("f:{{ id }}", function(msg){
                        updateConfiguration(msg.config);
                    });
        var getSensorConfig = function(){
            config.id = "s:"+getInputValue("uuidInput");
            config.client = getClientConfig();
            config.generator = getGeneratorConfig();
            // config.client.subscriptions = [];
            config.data_model = "apartment";
            config.gen_type = "data";
            config.client_type = "mqtt";
            console.log("CONFIG", config);
        };