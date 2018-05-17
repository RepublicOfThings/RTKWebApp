

function setActiveElements(activePageId, availablePages){
    for (var i = 0; i < availablePages.length; i++){
        $("#"+availablePages[i]).removeClass("active");
    }
    $("#"+activePageId).addClass("active");
}