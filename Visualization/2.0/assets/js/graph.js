var color;
var force;
var svg;

window.onload=function(){
    //Constants for the SVG
    var width = 1000,
        height = 600;

    //Set up the colour scale
    color = d3.scale.category20();

    //Set up the force layout
    force = d3.layout.force()
        .charge(-120)
        .linkDistance(function(d) { 
            return(1/(d.value+1) * 300); 
        })
        .size([width, height]);

    //Append a SVG to the body of the html page. Assign this SVG as an object to svg
    svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);
};

function readGraphJSON(filename){
    // Gets data from JSON file
    d3.json(filename, function(error, graph) {
        if (error) throw error;

        //Creates the graph data structure out of the json data
        force.nodes(graph.nodes)
            .links(graph.links)
            .start();

        //Create all the line svgs but without locations yet
        var link = svg.selectAll(".link")
            .data(graph.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function (d) {
            return Math.sqrt(d.value);
        });

        //Do the same with the circles for the nodes - no 
        var node = svg.selectAll(".node")
            .data(graph.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .attr("r", 8)
            .style("fill", function (d) {
            return color(d.group);
        });

        node.append("text")
              .attr("dx", 10)
              .attr("dy", ".35em")
              .attr("font-family", "Arial")
              .attr("font-size", "15px")
              .text(function(d) { return d.name })
              .style("stroke", "rgb(50,50,50)")
              .style("opacity", "0")
              .style("z-index", 2000);

        node.on("mouseover", mouseover)
            .on("mouseout", mouseout)

        //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
        force.on("tick", function () {
            link.attr("x1", function (d) {
                return d.source.x;
            })
                .attr("y1", function (d) {
                return d.source.y;
            })
                .attr("x2", function (d) {
                return d.target.x;
            })
                .attr("y2", function (d) {
                return d.target.y;
            });
            d3.selectAll("circle").attr("cx", function (d) {
                return d.x;
            })
                .attr("cy", function (d) {
                return d.y;
            });
            d3.selectAll("text").attr("x", function (d) {
                return d.x;
            })
                .attr("y", function (d) {
                return d.y;
            });
        });
    });
}

function mouseover() {
    d3.select(this).select("text").transition()
      .style("opacity", "1")
}

function mouseout() {
    d3.select(this).select("text").transition()
      .style("opacity", "0")
}