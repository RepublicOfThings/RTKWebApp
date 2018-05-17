

function RTKApp(endpoint, scheme){
    this.endpoint = endpoint || "http://localhost:8080/";
    this.colorScheme = new RTKColorScheme(scheme);
    this.api = new RTKInterface(this.endpoint);
    this.updateAPIStatus = function(callback, color, text, version, scheme){
        var colorScheme = this.colorScheme;
        this.api.getApiStatus(function(msg){
            msg = JSON.parse(msg);
            if (callback === undefined){
                callback = RTKAPIStatusHandler
            }
            callback(msg.payload, color, text, version, scheme || colorScheme);
        });
    };

    this.forceRedirect = function(url){
        location.href = url;
    };

}


function RTKColorScheme(scheme){
    // scheme.getElementColor("success");
    // probably should use css!
    this.schemes = {
        "default": {
            "success": "#00C851",
            "primary": "blue",
            "danger": "#FF4444",
            "warning": "#FFBB33",
            "info": "#33B5E5",
            "navbg": "#454545",
            "navtext": "#FFFFFF"
        }
    };
    this.scheme = this.schemes[scheme];
    this.getElementColor = function(element, scheme){
        if (scheme !== undefined){
            return this.schemes[scheme][element];
        } else {
            return this.scheme[element];
        }
    }

}


function RTKAPIStatusHandler(msg, colorElements, textElements, versionElements, scheme){
    var elements = {
        color: colorElements || ["apiStatusBadge", "apiVersionBadge"],
        text: textElements || ["apiStatusBadge"],
        version: versionElements || ["apiVersionBadge"]
    };
    var mapping = {
        "0": {color: RTKDefaultColors("success"), text: "Active"},
        "-1": {color: RTKDefaultColors("warning"), text: "Offline"},
        "-2": {color: RTKDefaultColors("danger"), text: "Unavailable"}
    };

    this.updateText = function(text){
        for (var i = 0; i < elements.text.length; i++){
            $("#"+elements.text[i]).text(text);
        }
    };

    this.updateColor = function(color){
        for (var i = 0; i < elements.color.length; i++){
            $("#"+elements.color[i]).css("background", color);
        }
    };

    this.updateVersion = function(version){
        for (var i = 0; i < elements.version.length; i++){
            $("#"+elements.version[i]).text(version);
        }
    };

    var statusMap = mapping[String(msg.status)];
    this.updateText(statusMap.text);
    this.updateColor(statusMap.color);
    this.updateVersion(msg.status.version)

}
