function loadWordData(wordFileName){
    // Gets data from JSON file
    d3.json(wordFileName, function(error, jsonfile) {
        if (error) throw error;

        allCommunityWords = jsonfile;

        wordCloudColor = d3.scale.linear()
            .domain([0,1,2,3,4,5,6,10,15,20,100])
            .range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);
    });
}

function generateWordCloud(groupNo, maxCount){
    if(allCommunityWords[groupNo].length > maxCount){
         var frequency_list = allCommunityWords[groupNo].slice(0, maxCount);
    }
    else{
         var frequency_list = allCommunityWords[groupNo];
    }
   

    d3.layout.cloud().size([width, height])
            .words(frequency_list)
            .rotate(0)
            .fontSize(function(d) { return d.size; })
            .on("end", drawWordCloud)
            .start();

    function drawWordCloud(words) {
        $("#wordCloud").empty();
        d3.select("#wordCloud").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(320,200)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("fill", function(d, i) { return wordCloudColor(i); })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
    }
}