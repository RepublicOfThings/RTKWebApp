function drawThingsNetwork(n,target) {
    var jsonNetwork=generateThingsNetwork(n);
    console.log("Drawing...");
    var width=document.getElementById(target).clientWidth;
    var height=screen.height;
    var svg=d3.select("#"+target).append("svg");
    svg.attr("width",width);svg.attr("height",width);
    var force=d3.layout.force();
    force.gravity(0.05);
    force.distance(40);
    force.charge(-1000);
    force.linkDistance(100);
    force.size([width,height]);
    var net=jsonNetwork;
    force.nodes(net.nodes);
    force.links(net.links);
    force.start();
    force.nodes(jsonNetwork.nodes).links(jsonNetwork.links).start();

    var link= svg.selectAll(".link")
                    .data(jsonNetwork.links)
                        .enter().append("line")
                        .attr("class","link")
                        .style("stroke-width",function(d){return Math.sqrt(d.weight);});

    var node=svg.selectAll(".node").data(jsonNetwork.nodes).enter().append("g").attr("class","node").call(force.drag);

    node.append("circle").on("click",click).attr("r","5");
    node.append("text").attr("dx",12).attr("dy",".35em").text(function(d){return d.name});
    force.on("tick",function(){
        link.attr("x1",function(d){
            return d.source.x;})
                .attr("y1",function(d){return d.source.y;})
                .attr("x2",function(d){return d.target.x;})
                .attr("y2",function(d){return d.target.y;});
        node.attr("transform",function(d){return"translate("+d.x+","+d.y+")";});});
    }
    function click(){
        var args=Array.prototype.slice.call(arguments);
        console.log("click!",this.id,args);
        // d3.select(this).transition().duration(750).attr("r",30).style("fill","lightsteelblue");
    }
    function onMouseOver(){
        console.log("MOUSEY");
    }

function generateNetworkCoordinates(n,r){var coordinates=[];var step=2.0*Math.PI/n;var sqrt_r=Math.sqrt(r);for(var i=0;i<n;i++){coordinates.push([sqrt_r*Math.cos(step*i),sqrt_r*Math.sin(step*i)]);}
    return coordinates;}

/*
function GraphView(){

    this.graph = null;
    this.draw = function(){

    };
    this.addNode = function(){

    };

}

*/

function generateThingsNetwork(n){
    var nodes=[];var connections=[];console.log("Generating...");
    var sensorCoords=generateNetworkCoordinates(n,100.0);
    var filterCoords=generateNetworkCoordinates(n,50.0);
    var coords=[];
    for(var i=0;i<2.0*n;i++){if(i<n){coords.push(sensorCoords[i]);}else{coords.push(filterCoords[i-n]);}}
    for(var i=0;i<n;i++){var sensor={name:"RTKSensor"+i,id:i,group:0,x:coords[i][0],y:coords[i][1]};
        var filter={name:"RTKFilter"+i,id:i+n,group:1,x:coords[i+n][0],y:coords[i+n][1]};
        var connection={source:i,target:i+n,weight:1.0};
        nodes.push(sensor);
        nodes.push(filter);
        connections.push(connection);
    }
    var hub={name:"RTKDataHub",id:2*n,group:2,x:0.0,y:0.0}
    nodes.push(hub)
    for(var i=0;i<n;i++){var connection={source:i+n,target:2*n,weight:1.0};connections.push(connection)}
    var network={"nodes":nodes,"links":connections};
    return network;}