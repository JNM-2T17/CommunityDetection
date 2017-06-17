// $(document).ready(function(){
// 	$(".generateCommunities").click(function(){
// 		loadFileData("assets/js/wordCounts.json", "assets/js/vis.json");
// 	});
// });


// function loadFileData(wordFileName, visFileName){
// 	var done = false;

//     d3.json(wordFileName, function(error, jsonfile) {
//         if (error) throw error;

//         allCommunityWords = jsonfile;

//         if(done){
//         	UI.initializeVis(allCommunityWords, graphData, true);
//         }
//         else{
//         	done = true;
//         }
//     });

//     d3.json(visFileName, function(error, jsonfile) {
//         if (error) throw error;

//         graphData = jsonfile;

//         if(done){
//         	UI.initializeVis(allCommunityWords, graphData, true);
//         }
//         else{
//         	done = true;
//         }
//     });
// }

var UI = {
	initializeVis : function(words, graph){
		// General

		$("#evaluation").css("display", "block");
		$("#communities").css("display", "block");

		// Graph

		Graph.generateCommunities(graph);

		// Word Clouds

		var communityColors = d3.scale.category20();

		for(var i = 1; i <= Object.keys(words).length; i++){
			$("#communities").append('\n\
		<div class="community" data-cNum="' + i + '">\n\
			<button class="community-button">\n\
				<div class="community-color" style="background-color: ' + communityColors(i) + '"></div>\n\
				<div class="community-name">Community ' + i + '</div>\n\
			</button>\n\
			<div class="community-wordcloud">\n\
			</div>\n\
		</div>')
		}

		$(".community").each(function(){
			WordCloud.generateWordCloud(words, $(this).attr("data-cNum"), 20);
		});

		$(".community-button").click(function(){
			var communityNum = $(this).parent().attr("data-cNum");

			if($(this).parent().find(".community-wordcloud").css("height") != "0px"){
				$(this).parent().find(".community-wordcloud").animate({
					height: 0
				}, 1000);
			}
			else{
				$(".community[data-cNum!='" + communityNum + "'] svg").each(function(){
					$(this).parent().animate({
						height: 0
					}, 1000);
				});

				$(this).parent().find(".community-wordcloud").animate({
					height: "500px"
				}, 1000);
			}
		});
	}
}