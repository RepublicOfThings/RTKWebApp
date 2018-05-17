/**
 * Created by MarkDouthwaite on 06/06/2017.
 */


function Graph(){
    this.nodes = [];
    this.edges = [];

    this.addNode = function(nodeID, x, y, radius){
        if (typeof radius === "undefined") { radius = 5; }
        this.nodes.push({id: String(nodeID), x: x, y: y, radius: radius});
    };

    this.delNode = function (nodeID) {

        this.nodes = this.nodes.filter(function (d) {return d.id !== nodeID});

    };

    this.nodeEdges = function (nodeID) {
        var edges = [];
        for (var i = 0; i < this.edges.length; i++) {
            if (this.edges[i].source.id === nodeID || this.edges[i].target.id === nodeID) {
                edges.push(this.edges[i]);
            }
        }
        return edges;
    };

    this.getNode = function (nodeID) {
        for (var i = 0; i < this.nodes.length; i++){
            if (this.nodes[i].id == nodeID){
                return this.nodes[i]
            }
        }
    };

    this.addEdge = function (sourceID, targetID, weight, directed) {1
        edgeID = sourceID+"_"+targetID;
        if (typeof weight === "undefined") { weight = 1.0; }
        if (typeof directed === "undefined") { directed = false; }

        this.edges.push({source: this.getNode(sourceID),
                         target: this.getNode(targetID),
                         weight: weight,
                         directed: directed,
                         id: edgeID});

    };

    this.delEdge = function (sourceID, targetID) {
        edgeID = sourceID+"_"+targetID;
        altID = targetID+"_"+sourceID;
        this.edges = this.edges.filter(function (d) {return (d.id !== edgeID && d.id !== altID)});
    };

    this.getEdge = function (sourceID, targetID){
        edgeID = sourceID+"_"+targetID;

        for (var i = 0; i < this.edges.length; i++){
            if (this.edges[i].id == edgeID){
                return this.edges[i]
            }
        }

    };

    this.loadGraph = function (data) {
        this.nodes = data.nodes;
        var edges = [];
        for (var i = 0; i < data.edges.length; i++){
            edges.push({"source": this.getNode(data.edges[i].source),
                        "target": this.getNode(data.edges[i].target),
                        "directed": data.edges[i].directed,
                        "weight": data.edges[i].weight})
        }
        this.edges = edges;
        console.log(edges);
    };

    this.includes = function (nodeID) {
        for (var i = 0; i < this.nodes.length; i++) {
            if (this.nodes[i].id === nodeID) {
                return true;
            }
        }
        return false;
    };
}