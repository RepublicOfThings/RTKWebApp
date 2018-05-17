/**
 * Created by MarkDouthwaite on 03/08/2017.
 */


function RTKTimeSeries(container, data){
    this.container = container;
    this.data = data;

    this.graph = null;

    this.preRender = function () {
        var m = [20, 80, 20, 20]; // margins
		var w = 0.8 * $(window).width() - m[1] - m[3]; // width
		var h = 0.6 * $(window).height() - m[0] - m[2]; // height
        var graph = d3.select("#"+this.container)
			      .attr("width", w + m[1] + m[3])
			      .attr("height", h + m[0] + m[2])
			    .append("svg:g")
			      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

        this.graph = graph;
    };

    this.clear = function(){
        this.graph.selectAll("*").remove()
    };

    this.render = function(){
        //box = $("#"+);
        //var height = 250;
        //    width = box.width();

        xData = [];
        yData = [];

        logData = [];
        smoothData = [];

        for (var i = 0; i < this.data.length; i++){
            yData.push(parseFloat(this.data[i].readings[0].value));
            xData.push(parseFloat(i));
        }

        for (var i = 0; i < this.data.length; i++){
            // console.log(this.data[i].meta.loglikelihood);
            logData.push(parseFloat(this.data[i].meta.r_squared));
        }

		for (var i = 0; i < this.data.length; i++){
            console.log(this.data[i].meta.smoothed);
            smoothData.push(parseFloat(this.data[i].meta.smoothed));
        }

		var m = [20, 80, 20, 20]; // margins
		var w = 0.8 * $(window).width() - m[1] - m[3]; // width
		var h = 0.6 * $(window).height() - m[0] - m[2]; // height

		// create a simple data array that we'll plot with a line (this array represents only the Y values, X will just be the index location)
		var data = yData;

		// console.log(data);

		// X scale will fit all values from data[] within pixels 0-w
		var x = d3.scale.linear().domain([0, data.length]).range([0, w]);
		// Y scale will fit values from 0-10 within pixels h-0 (Note the inverted domain for the y-scale: bigger is up!)

        // console.log(Math.min(...data), Math.max(...data));
		var y = d3.scale.linear().domain([Math.min(...data)-10, Math.max(...data)+10]).range([h, 0]);
			// automatically determining max range can work something like this
			// var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

                // console.log(Math.min(...data), Math.max(...data));
		var y2 = d3.scale.linear().domain([Math.min(...logData)-10, Math.max(...logData)+10]).range([h, 0]);
		var y3 = d3.scale.linear().domain([Math.min(...smoothData)-10, Math.max(...smoothData)+10]).range([h, 0]);
			// automatically determining max range can work something like this
			// var y = d3.scale.linear().domain([0, d3.max(data)]).range([h, 0]);

		// create a line function that can convert data[] into x and y points
		var line = d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) {
				// verbose logging to show what's actually being done
				// console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i);
			})
			.y(function(d) {
				// verbose logging to show what's actually being done
				// console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
				// return the Y coordinate where we want to plot this datapoint
				return y(d);
			});

			// Add an SVG element with the desired dimensions and margin.
        var graph = d3.select("#"+this.container)
			      .attr("width", w + m[1] + m[3])
			      .attr("height", h + m[0] + m[2])
			    .append("svg:g")
			      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

			// create yAxis
        var xAxis = d3.svg.axis().scale(x).tickSize(-h).tickSubdivide(true);
			// Add the x-axis.
			graph.append("svg:g")
			      .attr("class", "x axis")
			      .attr("transform", "translate(0," + h + ")")
			      .call(xAxis);


			// create left yAxis
        var yAxisLeft = d3.svg.axis().scale(y).ticks(4).orient("left");
			// Add the y-axis to the left
			graph.append("svg:g")
			      .attr("class", "y axis")
			      .attr("transform", "translate(-25,0)")
			      .call(yAxisLeft);

  			// Add the line by appending an svg:path element with the data line we created above
			// do this AFTER the axes above so that the line is above the tick-lines


        var line2= d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) {
				// verbose logging to show what's actually being done
				// console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i);
			})
			.y(function(d) {
				// verbose logging to show what's actually being done
				// console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
				// return the Y coordinate where we want to plot this datapoint
				return y2(d);
			});

        var line3 = d3.svg.line()
			// assign the X function to plot our line as we wish
			.x(function(d,i) {
				// verbose logging to show what's actually being done
				// console.log('Plotting X value for data point: ' + d + ' using index: ' + i + ' to be at: ' + x(i) + ' using our xScale.');
				// return the X coordinate where we want to plot this datapoint
				return x(i);
			})
			.y(function(d) {
				// verbose logging to show what's actually being done
				// console.log('Plotting Y value for data point: ' + d + ' to be at: ' + y(d) + " using our yScale.");
				// return the Y coordinate where we want to plot this datapoint
				return y3(d);
			});

        graph.append("svg:path").attr("d", line(data)).attr("class", "seriesLine");
        graph.append("svg:path").attr("d", line2(logData)).attr("class", "probLine");
		graph.append("svg:path").attr("d", line3(smoothData)).attr("class", "smoothLine");
        this.graph = graph;
    };

}