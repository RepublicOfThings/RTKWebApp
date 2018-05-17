

function GraphView(parent, height, width){
    this.graph = new Graph();
    this.viewWidth = width;
    this.viewHeight = height;
    this.monitor = null;
    var forceActive = false;
    var svg = setupCanvas(parent, width, height);
    var force = d3.layout.force();

    function setupCanvas (parent, w, h) {
        svg = d3.select("#"+parent).append("svg");
        svg.attr("width", w);
        svg.attr("height", h);
        svg.append("g").attr("id", "edges").attr("class", "canvas");
        svg.append("g").attr("id", "nodes").attr("class", "canvas");

        return svg
    };

    this.loadData = function (data) {
        this.graph.loadGraph(data);
        this.update();
    };

    this.addNode = function (id, x, y, r) {
        if (forceActive) { force.stop(); }
        this.graph.addNode(id, x, y, r);
        this.update();
        if (forceActive) { force.start(); }
    };

    this.update = function () {

        var link = svg.select("#edges").selectAll("line").data(this.graph.edges);

        link.enter().append("line")
            .attr("class", "edge")
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; })
            .attr("id", function(d) { return d.id; })
            .attr("stroke", "black")
            .attr("stroke-width", function(d) { return d.weight; });

        // console.log(this.graph.nodes);

        var node = svg.select("#nodes").selectAll("circle")
            .data(this.graph.nodes, function(d) { return d.id;});

        node.enter().append("circle")
            .attr("r", function(d) { return d.radius; })
            .attr("class", "node")
            .attr("fill", function(d) { return d.fill;})
            .attr("id", function(d) { return d.id; })
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });

        node.enter().append("text")
            .attr("dx",12)
            .attr("class", "node")
            .attr("dy",".35em")
            .text(function(d){return d.id});

    };

    this.addEdge = function (a, b, weight) {
        if (forceActive) { force.stop(); }
        this.graph.addEdge(a, b, weight);
        this.update();
        if (forceActive) { force.start(); }
    };

    this.delEdge = function (edge) {
        // console.log(edge);
        this.graph.delEdge(edge.source.id, edge.target.id);
        $("#"+edge.id).remove();
    };

    this.delNode = function (nodeID) {
        var edges = this.graph.nodeEdges(nodeID);

        for (var i = 0; i < edges.length; i++) {
            this.delEdge(edges[i]);
        }

        this.graph.delNode(nodeID);
        $("#"+nodeID).remove();

        this.update();
    };

    this.getNode = function(nodeIdentifier){
        for (var i = 0; i < this.graph.nodes.length; i++){
            if (this.graph.nodes[i].id == nodeIdentifier){
                return this.graph.nodes[i]
            }
        }
    };

    this.getNodeElement = function(nodeIdentifier) {
        if (this.getNode(nodeIdentifier) !== nodeIdentifier){
            return $("#"+String(nodeIdentifier));
        }
    };

    this.getEdge = function(a, b){
        //a and b are identifiers
        var a = this.getNode(a),
            b = this.getNode(b);
        return this.graph.getEdge(a.id, b.id);
    };

    this.toggleInteractive = function(){
        if (forceActive) {
            force.stop();
            forceActive = false;
        } else {
            forceActive = true;
            force.size([this.viewWidth, this.viewHeight])
                .nodes(this.graph.nodes) // initialize with a single node
                .links(this.graph.edges)
                .linkDistance(200)
                .on("tick", forceStep)
                .charge(-1000);
            force.start();
        }

    };

    function forceStep() {

        getEdges().attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        getNodes().attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; })
            .call(force.drag);

        svg.select("#nodes").selectAll("text").attr("transform", function(d) { return "translate(" + d.x+2 + "," + d.y + ")"; });
    }

    this.setForceDistance = function (value) {
        force.linkDistance(value);
        if (forceActive) {
            force.start();
        }
    };

    this.setForceCharge = function (value) {
        force.charge(value);
        if (forceActive) {
            force.start();
        }
    };

    this.setNodeStyle = function (nodeID, style, value) {
        $(document.getElementById(nodeID)).css(style, value);

        // this.getNode(nodeID)[style] = value;
        // this.update();
    };

    this.setEdgeStyle = function (edgeID, style, value) {
        $(document.getElementById(edgeID)).css(style, value);
    };

    this.setEdgeStyles = function (style, value) {
        // console.log(this.graph.edges);
        for (var i = 0; i < this.graph.edges.length; i++) {
            // console.log(this.graph.edges[i]);
            this.setEdgeStyle(this.graph.edges[i].id, style, value);
        }
    };

    var getNodes = function(){
        return svg.select("#nodes").selectAll("circle");
    };

    var getEdges = function(){
        return svg.select("#edges").selectAll("line");
    };

}