/**
 * Created by MarkDouthwaite on 04/08/2017.
 */


function RTKInstanceManager(){
    this.table = table
}


function addInstanceRow(api, table, data, configUrl){
    var configTargetUrl = configUrl.replace(/unknown/, data.id);
    var settingsElement = "<a class='material-icons control_button' href='"+configTargetUrl+"'>settings</a>";
    var deleteElement = "<a class='material-icons control_button' href='' onclick='deleteTargetInstance(\"" + data.id + "\")'>delete</a>";
    var startElement = "<a class='material-icons control_button' href='' onclick='startTargetInstance(\"" + data.id + "\")'>play_arrow</a>";
    var endElement = "<a class='material-icons control_button' href='' onclick='stopTargetInstance(\"" + data.id + "\")'>stop</a>";
    var controlElements = startElement + endElement + settingsElement + deleteElement;
    var rowData = [data.name, data.id, translateStatus(data.status, true), controlElements];
    table.addRow(rowData);
}

function deleteTargetInstance(id){
    deleteInstance(id, rest);
    location.reload();
}

function startTargetInstance(id, alertUser){
    startInstance(id, rest, undefined, alertUser || false);
}

function stopTargetInstance(id, alertUser){
    stopInstance(id, rest, undefined, alertUser || false);
}

function translateStatus(status, html){
    status = String(status);
    var statuses = {
        "0": ["Initialised", "primary"],
        "1": ["Inactive", "warning"],
        "2": ["Active", "success"],
        "-1": ["Unitialised", "danger"]
    };

    if (html === true){
        return "<span class='badge badge-"+statuses[status][1]+"'>"+statuses[status][0]+"</span>";
    } else {
        return statuses[status];
    }
}
