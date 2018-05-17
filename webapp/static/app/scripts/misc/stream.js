/**
 * Created by MarkDouthwaite on 19/03/2017.
 */


function RTKClient(sim){
    this.getLayout = function getLayout() {
        var xhr = new XMLHttpRequest();
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4 && xhr.status == 200){
                return JSON.parse(xhr.responseText);
            }
        };
        xhr.open("GET", "layout", true);
    };

    this.startStream = function startStream(){
        var xhr = new XMLHttpRequest();
        var start = 0;  // initial index from response.

        xhr.onreadystatechange = function(){
            if (xhr.readyState == 3) {
                var end = xhr.responseText.length;
                data = JSON.parse(xhr.responseText.substring(start, end));
                sim.update(data);
                start = end;
            }
        };
        xhr.open("GET", url, true);
        xhr.send();
    };

}

