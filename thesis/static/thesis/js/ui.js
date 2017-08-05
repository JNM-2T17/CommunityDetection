var ALGO_KMEANS = 1;
var ALGO_KMEANS_SA = 5;

var UI = {
	initializeUI : function(){
		console.log("UI.initializeUI");

		checkIfKmeans();

		$("#selectAlgorithm").bind("change", function(){
			checkIfKmeans();
		});

		function checkIfKmeans(){
			var dropbox = $("#selectAlgorithm");

			if(dropbox.val() == ALGO_KMEANS
				|| dropbox.val() == ALGO_KMEANS_SA){
				dropbox.after("<input id=\"selectK\" name=\"kval\" placeholder=\"Value of K\" type=\"number\" step=\"1\" min=\"0\" max=\"2500\"/>")
				$("#selectK").bind("change", function(){
					ErrorChecking.checkIfValid();
				});
			}
			else{
				$("#selectK").remove();
			}
		}

		ErrorChecking.initializeErrorCheck();
	},

	initializeVis : function(tweetWords, profileWords, graph, locations){
		console.log("UI.initializeVis");

		// General

		$("#description").css("display", "block");
		$("#evaluation").css("display", "block");
		$("#communities").css("display", "block");

		// Graph

		Graph.Communities.generateCommunities(graph);

		// STATISTICS

		var communityColors = d3.scale.category20();

		for(var i = 1; i <= Object.keys(tweetWords).length; i++){
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
			<div class="community-stats">\n\
				Tweet Word Cloud\n\
				<div class="community-wordcloud">\n\
				</div>\n\
				Profile Word Cloud\n\
				<div class="community-profilecloud">\n\
				</div>\n\
				Users Per Location\n\
				<div class="community-locations">\n\
				</div>\n\
			</div>\n\
		</div>')
		}

		// Tweet Word Clouds
		$(".community").each(function(){
			WordCloud.generateWordCloud(tweetWords, $(this).attr("data-cNum"), 20, CLOUDTYPE_TWEETS);
		});

		// Profile Word Clouds
		$(".community").each(function(){
			WordCloud.generateWordCloud(profileWords, $(this).attr("data-cNum"), 20, CLOUDTYPE_PROFILE);
		});

		// Location Pie Charts
		$(".community").each(function(){
			LocationPie.displayPieChart($(this).attr("data-cNum"), locations[$(this).attr("data-cNum")]);
		});

		$(".community-button").click(function(){
			var communityNum = $(this).parent().attr("data-cNum");

			if(Graph.currentMode == MODE_COMMUNITIES){
				Graph.Communities.centerOnCommunity(communityNum);
			}

			if($(this).parent().find(".community-stats").css("height") != "0px"){
				$(this).parent().find(".community-stats").animate({
					height: 0
				}, 1000);
			}
			else{
				$(".community[data-cNum!='" + communityNum + "'] .community-stats").each(function(){
					$(this).animate({
						height: 0
					}, 1000);
				});

				$(this).parent().find(".community-stats").animate({
					height: "1600px"
				}, 1000);
			}
		});
	}
}