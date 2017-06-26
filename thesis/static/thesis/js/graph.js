var MODE_COMMUNITIES = 0;
var MODE_COMMUNITYNODES = 1;
var MODE_SINGLENODE = 2;

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
    nodeGroupMap : {},
    currentMode : MODE_COMMUNITIES,
    backtrackStack : [],

    Communities : {

        generateCommunities : function(graph) {
            console.log("Graph.Communities.generateCommunities");

            if(Graph.force != null){
                Graph.force.stop();
                $("#graph svg").remove();
            }

            Graph.currentMode = MODE_COMMUNITIES;
            Graph.backtrackStack.push({mode : MODE_COMMUNITIES});

            var w = window;
            var d = document;
            var e = d.documentElement;
            var g = d.getElementsByTagName('body')[0];
            Graph.width = (w.innerWidth || e.clientWidth || g.clientWidth) - 380;
            Graph.height = (w.innerHeight|| e.clientHeight|| g.clientHeight) - 90;

            directed = graph.directed;
            Graph.graph = graph;
        
            if(graph != null && directed != null){

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

                node.on('click', Graph.Communities.nodeClick);

                //Now we are giving the SVGs co-ordinates - the force layout is generating the co-ordinates which this code is using to update the attributes of the SVG elements
                Graph.force.on("tick", function () {
                    d3.selectAll("#graph circle").attr("cx", function (d) {
                        return d.x = Math.max(getR(d.size), Math.min(Graph.width - getR(d.size), d.x));
                    })
                        .attr("cy", function (d) {
                        return d.y = Math.max(getR(d.size), Math.min(Graph.height - getR(d.size), d.y));
                    });
                });
            }
        },

        nodeClick : function(elem){
            console.log("Graph.Communities.nodeClick");

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
                Graph.Communities.selectCommunityOptions(elem, false);
                $("div.communityOptions").remove();
            });
            $("button.viewRelatedNodes").bind("click", function(){
                Graph.Communities.selectCommunityOptions(elem, true);
                $("div.communityOptions").remove();
            });
        },

        selectCommunityOptions : function(elem, withLinks){
            console.log("Graph.Communities.selectCommunityOptions");

            Graph.CommunityNodes.generateCommunityGraph(Graph.graph, elem["group"], withLinks);
            Graph.selectCommunity(elem["group"]);
            Graph.changeOptions();
        },
    },

    CommunityNodes : {

        currentCommunity : 0,
        withLinks : false,

        generateCommunityGraph : function(graph, communityNum, withLinks){
            console.log("Graph.CommunityNodes.generateCommunityGraph");

            Graph.force.stop();
            $("#graph svg").remove();

            Graph.currentMode = MODE_COMMUNITYNODES;
            Graph.backtrackStack.push({ mode : MODE_COMMUNITYNODES,
                                        communityNum : communityNum,
                                        withLinks : withLinks
                                      });
            Graph.currentCommunity = communityNum;
            Graph.CommunityNodes.withLinks = withLinks;

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
                var filteredGraph = Graph.CommunityNodes.filterByCommunity(graph, communityNum, withLinks);

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
                    .on("click", Graph.CommunityNodes.nodeClick);

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

        nodeClick : function(elem){
            console.log("Graph.CommunityNodes.nodeClick");

            Graph.SingleNode.generateNodeGraph(Graph.graph, elem.name, elem.group);
            Graph.changeOptions();

            // prevCommunityNum = $("div.community.active").attr("data-cnum");

            // Graph.selectCommunity(0);

            // Graph.appendViewAllCommunities();
            // $("div#options").append("<button class='viewCommunityButton'>Go back to viewing community " + prevCommunityNum + "</button>");
            // $("div#options button.viewCommunityButton").bind("click", function(){
            //     Graph.changeOptions();
            //     Graph.CommunityNodes.generateCommunityGraph(Graph.graph, prevCommunityNum, Graph.CommunityNodes.withLinks);
            //     Graph.selectCommunity(prevCommunityNum);
            // });
        },

        filterByCommunity : function(graph, communityNum, withLinks){
            console.log("Graph.CommunityNodes.filterByCommunity");

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

    },

    SingleNode : {

        currentNode : null,

        generateNodeGraph : function(graph, nodeNum, communityNum){
            console.log("Graph.SingleNode.generateNodeGraph");

            Graph.force.stop();
            $("#graph svg").remove();

            Graph.currentMode = MODE_SINGLENODE;
            Graph.backtrackStack.push({ mode : MODE_SINGLENODE,
                                        nodeNum : nodeNum,
                                        communityNum : communityNum
                                      });

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
                var filteredGraph = Graph.SingleNode.filterByNode(graph, nodeNum, communityNum);

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
                    .on("click", Graph.SingleNode.nodeClick);

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

        nodeClick : function(elem){
            console.log("Graph.SingleNode.nodeClick");

            Graph.SingleNode.generateNodeGraph(Graph.graph, elem.name, elem.group);
            Graph.selectCommunity(0);
            Graph.changeOptions();
        },

        filterByNode : function(graph, nodeNum, communityNum){
            console.log("Graph.SingleNode.filterByNode");

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
    },

    mouseover : function(elem){
        if(elem.name >= 0){
            d3.select(this).select("text").transition()
              .style("opacity", "1");
        }
    },

    mouseout : function(elem){
        if(elem.name >= 0){
            d3.select(this).select("text").transition()
              .style("opacity", "0");
        }
    },

    click : function(elem){
        
    },

    changeOptions : function(){
        console.log("Graph.changeOptions");

        $("div#options").empty();

        if(Graph.backtrackStack.length > 1){
            console.log("Graph.changeOptions: if(Graph.backtrackStack.length > 0)");

            var currScreen = Graph.backtrackStack.pop();
            var prevScreen = Graph.backtrackStack.pop();
            Graph.backtrackStack.push(prevScreen);
            Graph.backtrackStack.push(currScreen);

            console.log(prevScreen);

            if(prevScreen.mode == MODE_COMMUNITIES){
                $("div#options").append("<button class='goBack'>Go back to viewing all communities</button>");
                $("div#options button.goBack").bind("click", function(){
                    Graph.Communities.generateCommunities(Graph.graph);
                    Graph.selectCommunity(0);
                    Graph.backtrackStack.pop();
                    Graph.backtrackStack.pop();
                    Graph.changeOptions();
                });
            }
            else if(prevScreen.mode == MODE_COMMUNITYNODES){
                $("div#options").append("<button class='goBack'>Go back to viewing community " + prevScreen.communityNum + "</button>");
                $("div#options button.goBack").bind("click", function(){
                    Graph.CommunityNodes.generateCommunityGraph(Graph.graph, prevScreen.communityNum, Graph.CommunityNodes.withLinks);
                    Graph.selectCommunity(prevScreen.communityNum);
                    Graph.backtrackStack.pop();
                    Graph.backtrackStack.pop();
                    Graph.changeOptions();
                });
            }
            else if(prevScreen.mode == MODE_SINGLENODE){
                $("div#options").append("<button class='goBack'>Go back to viewing connections of node " + prevScreen.nodeNum + "</button>");
                $("div#options button.goBack").bind("click", function(){
                    Graph.SingleNode.generateNodeGraph(Graph.graph, prevScreen.nodeNum, prevScreen.communityNum);
                    Graph.selectCommunity(0);
                    Graph.backtrackStack.pop();
                    Graph.backtrackStack.pop();
                    Graph.changeOptions();
                });
            }
        }

        if(Graph.currentMode == MODE_COMMUNITYNODES){
            console.log("Graph.changeOptions: if(Graph.currentNode == MODE_COMMUNITYNODES) (withLinks == " + Graph.CommunityNodes.withLinks + ")");
            if(Graph.CommunityNodes.withLinks){
                $("div#options").append("<button class='viewCommunityNodes'>View users in this community only</button>");
                $("button.viewCommunityNodes").bind("click", function(){
                    Graph.CommunityNodes.generateCommunityGraph(Graph.graph, Graph.CommunityNodes.currentCommunity, false);
                    Graph.backtrackStack.pop();
                    Graph.changeOptions();
                });
            }
            else{
                $("div#options").append("<button class='viewCommunityNodes'>View users connected to and in this community</button>");
                $("button.viewCommunityNodes").bind("click", function(){
                    Graph.CommunityNodes.generateCommunityGraph(Graph.graph, Graph.CommunityNodes.currentCommunity, true);
                    Graph.backtrackStack.pop();
                    Graph.changeOptions();
                });
            }
        }

        if(Graph.currentMode != MODE_COMMUNITIES){
            Graph.appendViewAllCommunities();
        }
    },

    selectCommunity : function(communityNum){
        console.log("Graph.selectCommunity");

        $("div.community").removeClass("active");

        if(communityNum > 0){
            $("div.community[data-cnum=" + communityNum + "]").addClass("active");
        }

        Graph.CommunityNodes.currentCommunity = communityNum;
    },

    hideAllExtraOptions : function(){
        console.log("Graph.hideAllExtraOptions");

        $("div.communityOptions").remove();
    },

    appendViewAllCommunities : function(){
        console.log("Graph.appendViewAllCommunities");

        $("div#options").append("<button class='viewAllButton'>View all communities</button>");
        $("div#options button.viewAllButton").bind("click", function(){
            Graph.Communities.generateCommunities(Graph.graph);
            Graph.selectCommunity(0);
            Graph.changeOptions();
        });
    }
}