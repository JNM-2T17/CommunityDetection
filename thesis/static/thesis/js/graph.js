var Graph = {
    color : null,
    force : null,
    svg : null,
    width : null,
    height : null,
    lastClicked : null,
    minSize : 25,
    maxSize : 100,
    graph : null,
    nodeGroupMap : {}, // Map of node name to group number
    withLinks : false,

    generateGraph : function(graph){
        console.log("Graph.generateGraph: start");
        var w = window;
        var d = document;
        var e = d.documentElement;
        var g = d.getElementsByTagName('body')[0];
        Graph.width = (w.innerWidth || e.clientWidth || g.clientWidth) - 380;
        Graph.height = (w.innerHeight|| e.clientHeight|| g.clientHeight) - 90;

        directed = graph.directed;
    
        if(graph != null && directed != null){
            console.log("Graph.generateGraph: setup graph");

            //Set up the colour scale
            color = d3.scale.category20();

            //Set up the force layout
            Graph.force = d3.layout.force()
                .charge(-120)
                .linkDistance(function(d) { 
                    return(1/(d.value+1) * 500); 
                })
                .size([Graph.width, Graph.height]);

            //Append a SVG to the body of the html page. Assign this SVG as an object to svg
            graphSVG = d3.select("#graph").append("svg")
                .attr("width", Graph.width)
                .attr("height", Graph.height);

            if(directed == "true"){
                graphSVG.append("defs").selectAll("#graph marker")
                    .data(["suit", "licensing", "resolved"])
                  .enter().append("marker")
                    .attr("id", function(d) { return d; })
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 25)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                  .append("path")
                    .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
                    .style("stroke", "rgb(100,100,100)")
                    .style("opacity", "0.6");
            }

            //Creates the graph data structure out of the json data
            Graph.force.nodes(graph.nodes)
                .links(graph.links)
                .start();

            console.log("Graph.generateGraph: create graph links");

            //Create all the line svgs but without locations yet
            var link = graphSVG.selectAll("#graph .link")
                .data(graph.links)
                .enter().append("line")
                .attr("class", "link")
                .style("marker-end",  "url(#suit)")
                .style("stroke-width", function (d) {
                    return 1;
                // return Math.sqrt(d.value);
            });

            console.log("Graph.generateGraph: create graph nodes");

            //Do the same with the circles for the nodes - no 
            var node = graphSVG.selectAll("#graph .node")
                .data(graph.nodes)
                .enter().append("g")
                .attr("class", "node")
                .call(Graph.force.drag);

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
                  .style("stroke", "rgb(0,0,0)")
                  .style("opacity", "0")
                  .style("z-index", 2000);

            node.on("mouseover", Graph.mouseover)
                .on("mouseout", Graph.mouseout)
                .on("click", Graph.click);

            // node.on('click', datum => {
            //     alert("hi");
            //     alert(datum);
            //     console.log(datum); // the datum for the clicked circle
            // });

            //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
            Graph.force.on("tick", function () {
                console.log("Graph.generateGraph: set coordinates");
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
                d3.selectAll("#graph circle").attr("cx", function (d) {
                    return d.x;
                })
                    .attr("cy", function (d) {
                    return d.y;
                });
                d3.selectAll("#graph text").attr("x", function (d) {
                    return d.x;
                })
                    .attr("y", function (d) {
                    return d.y;
                });
            });
        }
    },

    mouseover : function(elem) {
        if(elem.name >= 0){
            d3.select(this).select("text").transition()
              .style("opacity", "1");
        }
    },

    mouseout : function(elem) {
        if(elem.name >= 0){
            d3.select(this).select("text").transition()
              .style("opacity", "0");
        }
    },

    click : function(elem) {
        console.log(elem)
    },

    generateCommunities : function(graph) {
        console.log("Graph.generateCommunities: start");

        var w = window;
        var d = document;
        var e = d.documentElement;
        var g = d.getElementsByTagName('body')[0];
        Graph.width = (w.innerWidth || e.clientWidth || g.clientWidth) - 380;
        Graph.height = (w.innerHeight|| e.clientHeight|| g.clientHeight) - 90;

        directed = graph.directed;
        Graph.graph = graph;
    
        if(graph != null && directed != null){

            console.log("Graph.generateCommunities: setup graph");

            //Set up the colour scale
            color = d3.scale.category20();

            //Set up the force layout
            Graph.force = d3.layout.force()
                .charge(-120)
                .linkDistance(function(d) { 
                    return(1/(d.value+1) * 500); 
                })
                .size([Graph.width, Graph.height]);

            //Append a SVG to the body of the html page. Assign this SVG as an object to svg
            var graphSVG = d3.select("#graph").append("svg")
                .attr("width", Graph.width)
                .attr("height", Graph.height);

            if(directed == "true"){
                graphSVG.append("defs").selectAll("#graph marker")
                    .data(["suit", "licensing", "resolved"])
                  .enter().append("marker")
                    .attr("id", function(d) { return d; })
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 25)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                  .append("path")
                    .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
                    .style("stroke", "rgb(100,100,100)")
                    .style("opacity", "0.6");
            }

            // console.log(graph.links);
            // console.log(graph.communityLinks);

            console.log("Graph.generateCommunities: creat graph structure");

            //Creates the graph data structure out of the json data
            Graph.force.nodes(graph.communities)
                // .links(graph.communityLinks)
                .start();

            Graph.force.gravity(0);
            // Graph.force.linkDistance(Graph.height/100);
            // Graph.force.linkStrength(0.1);
            Graph.force.charge(function(node) {
               return node.graph === 0 ? -30 : -300;
            });

            //Create all the line svgs but without locations yet
            // var link = graphSVG.selectAll("#graph .link")
            //     .data(graph.links)
            //     .enter().append("line")
            //     .attr("class", "link")
            //     .style("marker-end",  "url(#suit)")
            //     .style("stroke-width", function (d) {
            //         return 1;
            //     // return Math.sqrt(d.value);
            // });

            console.log("Graph.generateCommunities: create graph nodes");

            //Do the same with the circles for the nodes - no 
            var node = graphSVG.selectAll("#graph .node")
                .data(graph.communities)
                .enter().append("g")
                .attr("class", "node")
                .call(Graph.force.drag);

            node.append("circle")
                .attr("r", function(d) {
                    return getR(d.size);
                })
                .style("fill", function (d) {
                    return color(d.name);
                });

            function getR(nodeSize){
                if(graph.info.maxSize == graph.info.minSize){
                    return Graph.maxSize;
                }
                else{
                    return (nodeSize - graph.info.minSize) / (graph.info.maxSize - graph.info.minSize) * (Graph.maxSize - Graph.minSize) + Graph.minSize;
                }
            }
            // node.append("text")
            //       .attr("dx", 10)
            //       .attr("dy", ".35em")
            //       .attr("font-family", "Arial")
            //       .attr("font-size", "15px")
            //       .text(function(d) { return d.name })
            //       .style("stroke", "rgb(0,0,0)")
            //       .style("opacity", "0")
            //       .style("z-index", 2000);

            // node.on("mouseover", Graph.mouseover)
            //     .on("mouseout", Graph.mouseout)
            //     .on("click", Graph.click);

            node.on('click', Graph.clickGC);

            //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
            Graph.force.on("tick", function () {
                console.log("Graph.generateCommunities: set coordinates");
                d3.selectAll("#graph circle").attr("cx", function (d) {
                    return d.x = Math.max(getR(d.size), Math.min(Graph.width - getR(d.size), d.x));
                })
                    .attr("cy", function (d) {
                    return d.y = Math.max(getR(d.size), Math.min(Graph.height - getR(d.size), d.y));
                });
            });
        }
    },

    clickGC : function(elem) {
        console.log("clickGC");
        $("div.communityOptions").remove();
        $("div#main").append("\n\
            <div class=\"communityOptions\" style=\"top: " + elem.y + "px; left: " + elem.x + "px;\">\n\
                <button class=\"viewCommunityNodes\">View users in this community</button>\n\
                <button class=\"viewRelatedNodes\">View users connected to and in this community</button>\n\
            </div>");

        setTimeout(function(){
            $("div.communityOptions").remove();
        }, 5000);

        $("button.viewCommunityNodes").unbind("click");
        $("button.viewRelatedNodes").unbind("click");
        $("button.viewCommunityNodes").bind("click", function(){
            console.log("viewCommunityNodes click");
            Graph.selectCommunityOptions(elem, false);
            $("div.communityOptions").remove();
        });
        $("button.viewRelatedNodes").bind("click", function(){
            console.log("viewRelatedNodes click");
            Graph.selectCommunityOptions(elem, true);
            $("div.communityOptions").remove();
        });
    },

    selectCommunityOptions : function(elem, withLinks){
        console.log("selectCommunity");
        Graph.force.stop();
        $("#graph svg").remove();
        Graph.generateCommunityGraph(Graph.graph, elem["group"], withLinks);

        Graph.selectCommunity(elem["group"]);

        $("div#options").append("<button class='viewAllButton'>View All Communities</button>");
        $("div#options button.viewAllButton").bind("click", function(){
            Graph.force.stop();
            $("#graph svg").remove();
            Graph.generateCommunities(Graph.graph);
            $("div#options button").remove();
            Graph.selectCommunity(0);
        });
    },

    generateCommunityGraph : function(graph, communityNum, withLinks){
        console.log("generateCommunityGraph");
        var w = window;
        var d = document;
        var e = d.documentElement;
        var g = d.getElementsByTagName('body')[0];
        Graph.width = (w.innerWidth || e.clientWidth || g.clientWidth) - 380;
        Graph.height = (w.innerHeight|| e.clientHeight|| g.clientHeight) - 90;

        var directed = graph.directed;
        Graph.withLinks = withLinks;
    
        if(graph != null && directed != null){
            //Set up the colour scale
            var color = d3.scale.category20();

            //Set up the force layout
            Graph.force = d3.layout.force()
                .charge(-120)
                .linkDistance(function(d) { 
                    return(1/(d.value+1) * 500); 
                })
                .size([Graph.width, Graph.height]);

            //Append a SVG to the body of the html page. Assign this SVG as an object to svg
            var graphSVG = d3.select("#graph").append("svg")
                .attr("width", Graph.width)
                .attr("height", Graph.height);

            if(directed == "true"){
                graphSVG.append("defs").selectAll("#graph marker")
                    .data(["suit", "licensing", "resolved"])
                  .enter().append("marker")
                    .attr("id", function(d) { return d; })
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 25)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                  .append("path")
                    .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
                    .style("stroke", "rgb(100,100,100)")
                    .style("opacity", "0.6");
            }

            //Filters by community
            var filteredGraph = Graph.filterByCommunity(graph, communityNum, withLinks);

            console.log(filteredGraph);

            //Creates the graph data structure out of the json data
            Graph.force.nodes(filteredGraph.nodes)
                .links(filteredGraph.links)
                .start();

            //Create all the line svgs but without locations yet
            var link = graphSVG.selectAll("#graph .link")
                .data(filteredGraph.links)
                .enter().append("line")
                .attr("class", "link")
                .style("marker-end",  "url(#suit)")
                .style("stroke-width", function (d) {
                    return 1;
                // return Math.sqrt(d.value);
            });

            //Do the same with the circles for the nodes
            var node = graphSVG.selectAll("#graph .node")
                .data(filteredGraph.nodes)
                .enter().append("g")
                .attr("class", "node")
                .call(Graph.force.drag);

            node.append("circle")
                .attr("r", 8)
                .style("fill", function (d){
                    return color(d.group);
                })
                .style("display", function(d){
                    if(d.name < 0){
                        return "none";
                    }
                    else{
                        return "default";
                    }
            });

            node.append("text")
                  .attr("dx", 10)
                  .attr("dy", ".35em")
                  .attr("font-family", "Arial")
                  .attr("font-size", "15px")
                  .text(function(d) { return d.name })
                  .style("stroke", "rgb(0,0,0)")
                  .style("opacity", "0")
                  .style("z-index", 2000);

            node.on("mouseover", Graph.mouseover)
                .on("mouseout", Graph.mouseout)
                .on("click", Graph.clickNode);

            // node.on('click', datum => {
            //     alert("hi");
            //     alert(datum);
            //     console.log(datum); // the datum for the clicked circle
            // });

            //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
            Graph.force.on("tick", function () {
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
                d3.selectAll("#graph circle").attr("cx", function (d) {
                    return d.x;
                })
                    .attr("cy", function (d) {
                    return d.y;
                });
                d3.selectAll("#graph text").attr("x", function (d) {
                    return d.x;
                })
                    .attr("y", function (d) {
                    return d.y;
                });
            });
        }
    },

    clickNode : function(elem){
        Graph.force.stop();
        $("#graph svg").remove();
        Graph.generateNodeGraph(Graph.graph, elem.name, elem.group);

        prevCommunityNum = $("div.community.active").attr("data-cnum");

        Graph.selectCommunity(0);

        $("div#options").append("<button class='viewCommunityButton'>Back to Viewing Community " + prevCommunityNum + "</button>");
        $("div#options button.viewCommunityButton").bind("click", function(){
            Graph.force.stop();
            $("#graph svg").remove();
            Graph.generateCommunityGraph(Graph.graph, prevCommunityNum, Graph.withLinks);
            $(this).remove();
            Graph.selectCommunity(prevCommunityNum);
        });
    },

    generateNodeGraph : function(graph, nodeNum, communityNum){
        var w = window;
        var d = document;
        var e = d.documentElement;
        var g = d.getElementsByTagName('body')[0];
        Graph.width = (w.innerWidth || e.clientWidth || g.clientWidth) - 380;
        Graph.height = (w.innerHeight|| e.clientHeight|| g.clientHeight) - 90;

        var directed = graph.directed;
    
        if(graph != null && directed != null){
            //Set up the colour scale
            var color = d3.scale.category20();

            //Set up the force layout
            Graph.force = d3.layout.force()
                .charge(-120)
                .linkDistance(function(d) { 
                    return(1/(d.value+1) * 500); 
                })
                .size([Graph.width, Graph.height]);

            //Append a SVG to the body of the html page. Assign this SVG as an object to svg
            var graphSVG = d3.select("#graph").append("svg")
                .attr("width", Graph.width)
                .attr("height", Graph.height);

            if(directed == "true"){
                graphSVG.append("defs").selectAll("#graph marker")
                    .data(["suit", "licensing", "resolved"])
                  .enter().append("marker")
                    .attr("id", function(d) { return d; })
                    .attr("viewBox", "0 -5 10 10")
                    .attr("refX", 25)
                    .attr("refY", 0)
                    .attr("markerWidth", 6)
                    .attr("markerHeight", 6)
                    .attr("orient", "auto")
                  .append("path")
                    .attr("d", "M0,-5L10,0L0,5 L10,0 L0, -5")
                    .style("stroke", "rgb(100,100,100)")
                    .style("opacity", "0.6");
            }

            //Filters by community
            var filteredGraph = Graph.filterByNode(graph, nodeNum, communityNum);

            console.log(filteredGraph);

            //Creates the graph data structure out of the json data
            Graph.force.nodes(filteredGraph.nodes)
                .links(filteredGraph.links)
                .start();

            //Create all the line svgs but without locations yet
            var link = graphSVG.selectAll("#graph .link")
                .data(filteredGraph.links)
                .enter().append("line")
                .attr("class", "link")
                .style("marker-end",  "url(#suit)")
                .style("stroke-width", function (d) {
                    return 1;
                // return Math.sqrt(d.value);
            });

            //Do the same with the circles for the nodes
            var node = graphSVG.selectAll("#graph .node")
                .data(filteredGraph.nodes)
                .enter().append("g")
                .attr("class", "node")
                .call(Graph.force.drag);

            node.append("circle")
                .attr("r", function(d){
                    if(d.name == nodeNum){
                        return 16;
                    }
                    else{
                        return 8;
                    }
                })
                .style("fill", function(d){
                    return color(d.group);
                })
                .style("display", function(d){
                    if(d.name < 0){
                        return "none";
                    }
                    else{
                        return "default";
                    }
            });

            node.append("text")
                  .attr("dx", 10)
                  .attr("dy", ".35em")
                  .attr("font-family", "Arial")
                  .attr("font-size", "15px")
                  .text(function(d) { return d.name })
                  .style("stroke", "rgb(0,0,0)")
                  .style("opacity", "0")
                  .style("z-index", 2000);

            node.on("mouseover", Graph.mouseover)
                .on("mouseout", Graph.mouseout)
                .on("click", Graph.click);

            // node.on('click', datum => {
            //     alert("hi");
            //     alert(datum);
            //     console.log(datum); // the datum for the clicked circle
            // });

            //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
            Graph.force.on("tick", function () {
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
                d3.selectAll("#graph circle").attr("cx", function (d) {
                    return d.x;
                })
                    .attr("cy", function (d) {
                    return d.y;
                });
                d3.selectAll("#graph text").attr("x", function (d) {
                    return d.x;
                })
                    .attr("y", function (d) {
                    return d.y;
                });
            });
        }
    },

    filterByCommunity : function(graph, communityNum, withLinks){
        var nodes = [];
        var links = [];
        var nodeMap = {}; // Map of node name to index

        for(var i = 1; i <= graph.communities.length; i++){
            nodes.push({name: i * -1, group: i});
        }

        for(i = 0; i < graph.nodes.length; i++){
            if(graph.nodes[i]["group"] == communityNum){
                nodes.push(graph.nodes[i]);
                nodeMap[graph.nodes[i]["name"]] = nodes.length - 1;
                console.log(graph.nodes[i]["name"]);
            }
            Graph.nodeGroupMap[graph.nodes[i]["name"]] = graph.nodes[i]["group"];
        }

        for(i = 0; i < graph.links.length; i++){
            if(Graph.nodeGroupMap[graph.links[i]["source"]] == communityNum
                || Graph.nodeGroupMap[graph.links[i]["target"]] == communityNum){

                if(withLinks){
                    if(Graph.nodeGroupMap[graph.links[i]["source"]] == communityNum){
                        if(!(graph.links[i]["target"] in nodeMap)){
                            nodes.push({
                                         name  : graph.links[i]["target"],
                                         group : Graph.nodeGroupMap[graph.links[i]["target"]]
                                       });
                            nodeMap[graph.links[i]["target"]] = nodes.length - 1;
                        }
                    }
                    if(Graph.nodeGroupMap[graph.links[i]["target"]] == communityNum){
                        if(!(graph.links[i]["source"] in nodeMap)){
                            nodes.push({
                                         name  : graph.links[i]["source"],
                                         group : Graph.nodeGroupMap[graph.links[i]["source"]]
                                       });
                            nodeMap[graph.links[i]["source"]] = nodes.length - 1;
                        }
                    }
                }
                
                if(withLinks
                    || (Graph.nodeGroupMap[graph.links[i]["source"]] == communityNum
                        && Graph.nodeGroupMap[graph.links[i]["target"]] == communityNum)){
                    links.push({
                                 source : nodeMap[graph.links[i]["source"]],
                                 target : nodeMap[graph.links[i]["target"]],
                                 value  : graph.links[i]["value"]
                               });
                }
            }
        }

        return {nodes: nodes, links: links};
    },

    filterByNode : function(graph, nodeNum, communityNum){
        var nodes = [];
        var links = [];
        var nodeMap = {}; // Map of node name to index

        for(var i = 1; i <= graph.communities.length; i++){
            nodes.push({name: i * -1, group: i});
        }

        nodes.push({name: nodeNum, group: communityNum});
        nodeMap[nodeNum] = nodes.length - 1;

        for(i = 0; i < graph.links.length; i++){
            if(graph.links[i]["source"] == nodeNum
                || graph.links[i]["target"] == nodeNum){

            if(graph.links[i]["source"] == nodeNum){
                if(!(graph.links[i]["target"] in nodeMap)){
                    nodes.push({
                                 name  : graph.links[i]["target"],
                                 group : Graph.nodeGroupMap[graph.links[i]["target"]]
                               });
                    nodeMap[graph.links[i]["target"]] = nodes.length - 1;
                }
            }
            if(graph.links[i]["target"] == nodeNum){
                if(!(graph.links[i]["source"] in nodeMap)){
                    nodes.push({
                                 name  : graph.links[i]["source"],
                                 group : Graph.nodeGroupMap[graph.links[i]["source"]]
                               });
                    nodeMap[graph.links[i]["source"]] = nodes.length - 1;
                }
            }

            links.push({
                         source : nodeMap[graph.links[i]["source"]],
                         target : nodeMap[graph.links[i]["target"]],
                         value  : graph.links[i]["value"]
                       });
            }
        }

        return {nodes: nodes, links: links};
    },

    selectCommunity : function(communityNum){
        $("div.community").removeClass("active");

        if(communityNum > 0){
            $("div.community[data-cnum=" + communityNum + "]").addClass("active");
        }
    },

    hideAllExtraOptions : function(){
        $("div.communityOptions").remove();
    }
}






// Set-up the export button
// $(document).ready(function(){
//     $("#saveButton").click(function(){
//         console.log("saveButton");
//         var svgString = getSVGString(svg.node());
//         svgString2Image( svgString, 2*width, 2*height, 'png', save ); // passes Blob and filesize String to the callback

//         function save( dataBlob, filesize ){
//             saveAs( dataBlob, 'D3 vis exported to PNG.png' ); // FileSaver.js function
//         }
//     });
// });


// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
// function getSVGString( svgNode ) {
//     svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
//     var cssStyleText = getCSSStyles( svgNode );
//     appendCSS( cssStyleText, svgNode );

//     var serializer = new XMLSerializer();
//     var svgString = serializer.serializeToString(svgNode);
//     svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
//     svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

//     return svgString;

//     function getCSSStyles( parentElement ) {
//         var selectorTextArr = [];

//         // Add Parent element Id and Classes to the list
//         selectorTextArr.push( '#'+parentElement.id );
//         for (var c = 0; c < parentElement.classList.length; c++)
//                 if ( !contains('.'+parentElement.classList[c], selectorTextArr) )
//                     selectorTextArr.push( '.'+parentElement.classList[c] );

//         // Add Children element Ids and Classes to the list
//         var nodes = parentElement.getElementsByTagName("*");
//         for (var i = 0; i < nodes.length; i++) {
//             var id = nodes[i].id;
//             if ( !contains('#'+id, selectorTextArr) )
//                 selectorTextArr.push( '#'+id );

//             var classes = nodes[i].classList;
//             for (var c = 0; c < classes.length; c++)
//                 if ( !contains('.'+classes[c], selectorTextArr) )
//                     selectorTextArr.push( '.'+classes[c] );
//         }

//         // Extract CSS Rules
//         var extractedCSSText = "";
//         for (var i = 0; i < document.styleSheets.length; i++) {
//             var s = document.styleSheets[i];
            
//             try {
//                 if(!s.cssRules) continue;
//             } catch( e ) {
//                     if(e.name !== 'SecurityError') throw e; // for Firefox
//                     continue;
//                 }

//             var cssRules = s.cssRules;
//             for (var r = 0; r < cssRules.length; r++) {
//                 if ( contains( cssRules[r].selectorText, selectorTextArr ) )
//                     extractedCSSText += cssRules[r].cssText;
//             }
//         }
        

//         return extractedCSSText;

//         function contains(str,arr) {
//             return arr.indexOf( str ) === -1 ? false : true;
//         }

//     }

//     function appendCSS( cssText, element ) {
//         var styleElement = document.createElement("style");
//         styleElement.setAttribute("type","text/css"); 
//         styleElement.innerHTML = cssText;
//         var refNode = element.hasChildNodes() ? element.children[0] : null;
//         element.insertBefore( styleElement, refNode );
//     }
// }


// function svgString2Image( svgString, width, height, format, callback ) {
//     var format = format ? format : 'png';

//     var imgsrc = 'data:image/svg+xml;base64,'+ btoa( unescape( encodeURIComponent( svgString ) ) ); // Convert SVG string to data URL

//     var canvas = document.createElement("canvas");
//     var context = canvas.getContext("2d");

//     canvas.width = width;
//     canvas.height = height;

//     var image = new Image();
//     image.onload = function() {
//         context.clearRect ( 0, 0, width, height );
//         context.drawImage(image, 0, 0, width, height);

//         // canvas.toBlob( function(blob) {
//         //     var filesize = Math.round( blob.length/1024 ) + ' KB';
//         //     if ( callback ) callback( blob, filesize );
//         // });

//         var imgPreview = document.createElement("div");
//             imgPreview.appendChild(image);
//             document.querySelector("body").appendChild(imgPreview);

//         $("svg").remove();
        
//     };

//     image.src = imgsrc;
// }