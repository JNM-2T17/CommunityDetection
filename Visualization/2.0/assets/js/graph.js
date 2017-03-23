var color;
var force;
var svg;
var w = window;
var d = document;
var e = d.documentElement;
var g = d.getElementsByTagName('body')[0];
var width = w.innerWidth || e.clientWidth || g.clientWidth;
var height = w.innerHeight|| e.clientHeight|| g.clientHeight;
var lastClicked = null;

var allCommunityWords = [];
var wordCloudColor;

window.onload=function(){

    var wordFile = document.getElementById("wordFile").value;
    var filename = document.getElementById("filename").value;
    var directed = document.getElementById("directed").value;

    loadWordData(wordFile);

    //Set up the colour scale
    color = d3.scale.category20();

    //Set up the force layout
    force = d3.layout.force()
        .charge(-120)
        .linkDistance(function(d) { 
            return(1/(d.value+1) * 500); 
        })
        .size([width, height]);

    //Append a SVG to the body of the html page. Assign this SVG as an object to svg
    svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    if(directed == "true"){
        svg.append("defs").selectAll("marker")
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
            .style("stroke", "rgb(50,50,50)")
            .style("opacity", "0.6");
    }
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
            .style("marker-end",  "url(#suit)")
            .style("stroke-width", function (d) {
                return 1;
            // return Math.sqrt(d.value);
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
            .on("click", click);

        // node.on('click', datum => {
        //     alert("hi");
        //     alert(datum);
        //     console.log(datum); // the datum for the clicked circle
        // });

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

};

function mouseover() {
    d3.select(this).select("text").transition()
      .style("opacity", "1");
}

function mouseout() {
    d3.select(this).select("text").transition()
      .style("opacity", "0");
}

function click(elem) {
    if(elem["group"] != lastClicked){
        generateWordCloud(elem["group"], 50);
        lastClicked = elem["group"];
    }
}


// Set-up the export button
$(document).ready(function(){
    $("#saveButton").click(function(){
        console.log("saveButton");
        var svgString = getSVGString(svg.node());
        svgString2Image( svgString, 2*width, 2*height, 'png', save ); // passes Blob and filesize String to the callback

        function save( dataBlob, filesize ){
            saveAs( dataBlob, 'D3 vis exported to PNG.png' ); // FileSaver.js function
        }
    });
});


// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
function getSVGString( svgNode ) {
    svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
    var cssStyleText = getCSSStyles( svgNode );
    appendCSS( cssStyleText, svgNode );

    var serializer = new XMLSerializer();
    var svgString = serializer.serializeToString(svgNode);
    svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
    svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

    return svgString;

    function getCSSStyles( parentElement ) {
        var selectorTextArr = [];

        // Add Parent element Id and Classes to the list
        selectorTextArr.push( '#'+parentElement.id );
        for (var c = 0; c < parentElement.classList.length; c++)
                if ( !contains('.'+parentElement.classList[c], selectorTextArr) )
                    selectorTextArr.push( '.'+parentElement.classList[c] );

        // Add Children element Ids and Classes to the list
        var nodes = parentElement.getElementsByTagName("*");
        for (var i = 0; i < nodes.length; i++) {
            var id = nodes[i].id;
            if ( !contains('#'+id, selectorTextArr) )
                selectorTextArr.push( '#'+id );

            var classes = nodes[i].classList;
            for (var c = 0; c < classes.length; c++)
                if ( !contains('.'+classes[c], selectorTextArr) )
                    selectorTextArr.push( '.'+classes[c] );
        }

        // Extract CSS Rules
        var extractedCSSText = "";
        for (var i = 0; i < document.styleSheets.length; i++) {
            var s = document.styleSheets[i];
            
            try {
                if(!s.cssRules) continue;
            } catch( e ) {
                    if(e.name !== 'SecurityError') throw e; // for Firefox
                    continue;
                }

            var cssRules = s.cssRules;
            for (var r = 0; r < cssRules.length; r++) {
                if ( contains( cssRules[r].selectorText, selectorTextArr ) )
                    extractedCSSText += cssRules[r].cssText;
            }
        }
        

        return extractedCSSText;

        function contains(str,arr) {
            return arr.indexOf( str ) === -1 ? false : true;
        }

    }

    function appendCSS( cssText, element ) {
        var styleElement = document.createElement("style");
        styleElement.setAttribute("type","text/css"); 
        styleElement.innerHTML = cssText;
        var refNode = element.hasChildNodes() ? element.children[0] : null;
        element.insertBefore( styleElement, refNode );
    }
}


function svgString2Image( svgString, width, height, format, callback ) {
    var format = format ? format : 'png';

    var imgsrc = 'data:image/svg+xml;base64,'+ btoa( unescape( encodeURIComponent( svgString ) ) ); // Convert SVG string to data URL

    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");

    canvas.width = width;
    canvas.height = height;

    var image = new Image();
    image.onload = function() {
        context.clearRect ( 0, 0, width, height );
        context.drawImage(image, 0, 0, width, height);

        // canvas.toBlob( function(blob) {
        //     var filesize = Math.round( blob.length/1024 ) + ' KB';
        //     if ( callback ) callback( blob, filesize );
        // });

        var imgPreview = document.createElement("div");
            imgPreview.appendChild(image);
            document.querySelector("body").appendChild(imgPreview);

        $("svg").remove();
        
    };

    image.src = imgsrc;
}