/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function getFormInputValue(inputElementId, defaultValue, parseFunc){
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


function setFormInputValue(inputElementId, value){
    var element = $("#"+inputElementId);
    element.val(value);
}


