var LocationPie = {
	charts : [],
	canvases : [],

	generatePieChart : function(locations){
		pieNums = [];
		pieNames = [];

		console.log(locations);

		Object.keys(locations).forEach(function(key) {
		    pieNums.push(locations[key]);
		    pieNames.push(key);
		});

		var pieData = {
		    datasets: [{
		        data: pieNums
		    }],

		    // These labels appear in the legend and in the tooltips when hovering different arcs
		    labels: pieNames
		};

		console.log(pieData);

		return {
		    type: 'horizontalBar',
		    data: pieData,
		    options: {
	            legend: {
		            display: false
		         },
		         tooltips: {
		            enabled: false
		         }
	        }
		};
	},

	displayPieChart : function(commNum, locations){
		var idName = "locPie" + commNum;
		$(".community[data-cNum='" + commNum + "'] .community-locations").html("<canvas id=\"" + idName + "\" width=\"280\" height=\"450\"></canvas>");
		LocationPie.canvases.push($("#" + idName));
		LocationPie.charts.push(new Chart(LocationPie.canvases[LocationPie.canvases.length - 1], LocationPie.generatePieChart(locations)));
	}
}