var ALGO_KMEANS = 1;
var ALGO_DHC = 2;

var UI = {
	initializeUI : function(){
		$("#selectAlgorithm").bind("change", function(){
			if($(this).val() == ALGO_KMEANS){
				$(this).after("<input id=\"selectK\" name=\"kval\" placeholder=\"Value of K\" type=\"number\" step=\"1\" min=\"1\" max=\"2500\"/>")
			}
			else{
				$("#selectK").remove();
			}
		});
	},
	
	initializeVis : function(words, graph){
		// General

		$("#evaluation").css("display", "block");
		$("#communities").css("display", "block");

		// Graph

		Graph.Communities.generateCommunities(graph);

		// Word Clouds

		var communityColors = d3.scale.category20();

		for(var i = 1; i <= Object.keys(words).length; i++){
			var sizeLabel = "users";

			if(graph.communities[i-1].size == 1){
				var sizeLabel = "user";
			}

			$("#communities").append('\n\
		<div class="community" data-cNum="' + i + '">\n\
			<button class="community-button">\n\
				<div class="community-color" style="background-color: ' + communityColors(i) + '"></div>\n\
				<div class="community-name">Community ' + i + ' (' + graph.communities[i-1].size + ' ' + sizeLabel + ')</div>\n\
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