

function NetworkMonitor(url){
    this.target = url;
    this.tableView = null;
    this.graphView = null;
    this.cacheSize = 5;
    this.connection = new WebSocket(this.target);
    this.connection.monitor = this;
    this.nodes = [];

    this.connection.onmessage = function(event){
        var message = JSON.parse(event.data);
        switch (message.type){
            case "sensor":
                this.monitor.consumeNode(message);
                break;
            case "action":
                this.monitor.consumeAction(message);
                break;
            default:
                this.monitor.consumeError(message)
        }

    };
    this.connection.onopen = function(event){
        this.monitor.active = true;
        $("#state").text("Connected");
        $("#state").addClass("label-success");
    };
    this.connection.onclose = function(event){
        this.monitor.active = false;
        $("#state").text("Disconnected");
        $("#state").addClass("label-danger");
    };

    this.consumeNode = function(message){
        var node = message.payload;
        var target = node;
        if (!this.monitoring(target)){
            target.cache = [];  // add cache to target
            console.log("Oo, a new node! Hello", target.uuid);
            this.acquireNode(target);
        }

        var cachedNode = this.node(target.uuid);
        cachedNode.cache.push(node.value);
        while (cachedNode.cache.length > this.cacheSize){
            cachedNode.cache.shift();
        }
        this.updateNode(node);
    };

    this.consumeAction = function(message){
        if (message.data.kill != null) {
            var target = message.data.kill;
            if (this.monitoring(target)) {
                var index = this.nodes.indexOf(this.node(target.uuid));
                if (index != -1){
                    this.nodes.splice(index, 1);
                    this.tableView.delRowById(target.uuid);
                    $("#device_count").text(this.tableView.numRows);
                    console.log("Sorry to see you go! Goodbye", target.uuid, " | ", this.nodes.length, "remain.");
                }
            }
        }
    };

    this.consumeError = function(message){

    };

    this.monitoring = function(node){
        for (var i = 0; i < this.nodes.length; i++){
            if (node.uuid == this.nodes[i].uuid){
                return true;
            }
        }
        return false;
    };

    this.addTable = function(table){
        this.tableView = table;
        this.tableView.monitor = this;
    };

    this.addGraph = function(graph){
        this.graphView = graph;
        this.graphView.monitor = this;
    };

    this.acquireNode = function(data){
        this.nodes.push(data)
    };

    this.updateNode = function(node){
        // generalise this
        if (this.tableView !== null){
            if (this.tableView.rowIds().includes(node.uuid)){
                var i = this.tableView.rowIndex(node.uuid);
                var keys = this.tableView.columns();
                for (var j = 0; j < keys.length; j++){
                    this.tableView.cell(i, keys.indexOf("Value")).text(node.value);
                    this.tableView.cell(i, keys.indexOf("Confidence")).text(node.conf);
                    this.tableView.cell(i, keys.indexOf("Set Confidence")).text(node.sconf);
                }
            } else {
                this.tableView.addRow([ node.cid,
                    node.value,
                    node.units,
                    node.conf,
                    node.sconf,
                    "<span class='material-icons' style='color: green;'>done</span>",
                    "<a class='material-icons' style='cursor: hand;'>info_outline</a>",
                    node.uuid], node.uuid)
            }
            $("#device_count").text(this.tableView.numRows);
        } else if (this.graphView !== null) {
            if (this.graphView.graph.includes("RTKSensor"+node.uuid)) {
                if (node.value > 0.0) {
                    this.graphView.setNodeStyle("RTKSensor"+node.uuid, "fill", "#8DFF33");
                    this.graphView.setNodeStyle("RTKFilter"+node.uuid, "stroke", "#8DFF33");
                    this.graphView.setEdgeStyle("RTKSensor"+node.uuid+"_RTKFilter"+node.uuid, "stroke", "#8DFF33");
                    this.graphView.setEdgeStyle("RTKHub_RTKFilter"+node.uuid, "stroke", "#999");
                    this.graphView.setEdgeStyle("RTKHub_RTKFilter"+node.uuid, "stroke-width", "4");

                } else {
                    this.graphView.setNodeStyle("RTKSensor"+node.uuid, "fill", "#FF3333");
                    this.graphView.setNodeStyle("RTKFilter"+node.uuid, "stroke", "#FF3333");
                    this.graphView.setEdgeStyle("RTKSensor"+node.uuid+"_RTKFilter"+node.uuid, "stroke", "#FF3333");
                    this.graphView.setEdgeStyle("RTKHub_RTKFilter"+node.uuid, "stroke-width", "5");
                    this.graphView.setEdgeStyle("RTKHub_RTKFilter"+node.uuid, "stroke", "#38dcd4");
                }
            } else {
                this.graphView.addNode("RTKSensor"+node.uuid, 500, 500, 8);
                this.graphView.addNode("RTKFilter"+node.uuid, 500, 500, 10);
                this.graphView.addEdge("RTKSensor"+node.uuid, "RTKFilter"+node.uuid, 2);
                this.graphView.addEdge("RTKHub", "RTKFilter"+node.uuid, 4);
                this.graphView.setNodeStyle("RTKSensor"+node.uuid, "fill", "#999");
                this.graphView.setNodeStyle("RTKFilter"+node.uuid, "fill", "#999");
                this.graphView.setEdgeStyle("RTKHub_RTKFilter"+node.uuid, "stroke", "#999");
                this.graphView.setEdgeStyle("RTKSensor"+node.uuid+"_RTKFilter"+node.uuid, "stroke", "#999");
            }
        }
    };

    this.node = function(uuid) {
        for (var i = 0; i < this.nodes.length; i++){
            if (uuid == this.nodes[i].uuid){
                return this.nodes[i];
            }
        }
    };
}

