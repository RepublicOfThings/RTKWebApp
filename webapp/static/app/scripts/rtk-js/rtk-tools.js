

function RTKDefaultColors(label){
    var mapping = {
        "success": "#00C851",
        "danger": "#ff4444",
        "warning": "#ffbb33",
        "info": "#33b5e5",
        "dsuccess": "#007E33"
    };
    return mapping[label];
}


function updateUUIDFields(elementIds, apiEndpoint){
    if (rest === undefined || rest === null){
        var rest = new RTKInterface(apiEndpoint || endpoint)
    }
    rest.getGenerateUUID('filter', function(msg){
        msg = JSON.parse(msg);
        for (var i = 0; i < elementIds.length; i++){
            $('#'+elementIds[i]).val(msg.payload);
        }

    });
}



function updateStatusElements(textElements, colorElements, versionElements, apiEndpoint){
    if (rest === undefined || rest === null){
        var rest = new RTKInterface(apiEndpoint || endpoint)
    }
    var mapping = {
        "0": {color: RTKDefaultColors("success"), text: "Active"},
        "-1": {color: RTKDefaultColors("warning"), text: "Offline"},
        "-2": {color: RTKDefaultColors("danger"), text: "Unavailable"}
    };

    rest.getApiStatus(function(msg){
        msg = JSON.parse(msg);
        var details = mapping[String(msg.payload.status)];
        updateElementColors(colorElements, details.color);
        updateElementText(textElements, details.text);
        updateElementVersion(versionElements, msg.payload.version);
    });
}


function updateElementColors(elementIds, color){
    for (var i = 0; i < elementIds.length; i++){
        $("#"+elementIds[i]).css("background", color);
    }
}


function updateElementText(elementIds, text){
        for (var i = 0; i < elementIds.length; i++){
            $("#"+elementIds[i]).text(text);
    }
}


function updateElementVersion(elementIds, version){
        for (var i = 0; i < elementIds.length; i++){
        $("#"+elementIds[i]).text(version);
    }
}



function defaultMQTTClientConfig(id){
    return {
        client_id: null,
        host: "iot.eclipse.org",
        port: 1883,
        clean_session: true,
        userdata: null,
        transport: 'tcp',
        protocol: 4,
        subscriptions: [],
        topics: []
    }
}


function defaultPipeConfig(id){
    return {

    }
}


function defaultDataGeneratorConfig(id){
    return {

    }
}


function defaultNormalGeneratorConfig(id){
    return {

    }
}


function defaultFilterInstance(id){
    return {

    }
}


function defaultSensorInstance(id){
    return {

    }
}




// config helpers

function getInputValue(inputElementId, defaultValue, parseFunc){
    var element = $("#"+inputElementId);
    var value = null;

    // extract element from input
    if (element.val() === ""){
        if (defaultValue === undefined || defaultValue === null){
            value = element.attr("placeholder");
        } else {
            value = element.val();
        }
    } else {
        value = element.val();
    }

    // apply parsing function if provided
    if (parseFunc !== undefined){
        return parseFunc(value);
    } else {
        return value;
    }
}