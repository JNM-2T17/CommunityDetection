colors = ["red", "green", "blue"];
size = 100;

/*
Gets pixels to offset for the community of a given node
@param communities: Object containing community information
@param node: Object containing node information
@return Array containing x offset at index 0 and y offset at index 1
*/
function getCommunityOffset(communities, node){
	final = [(node.communityNum - 1) * 1.6, 0];
	return final;
}

/*
Gets color of the given node's community 
@param node: Object containing node information
@return Array containing x offset at index 0 and y offset at index 1
*/
function getCommunityColor(node){
	return colors[node.communityNum % colors.length];
}

/*
Gets Fixes positions of nodes on the graph
@param fileName: Name of JSON file containing the graph
@param containerID: ID of container of graph in the HTML file
*/
function setGraph(fileName, containerID){
	sigma.parsers.json(fileName,

		{container: "network-graph",
		 renderer: {
			container: document.getElementById(containerID),
			type: "canvas"
		 },
		 settings: {
			labelThreshold: 1
		 }
		},

		function(s) { // This function is passed an instance of Sigma s

			var communityCounts = new Object();

			// For each node
			s.graph.nodes().forEach(function(node, i, a) {
				// Determine community of node and update count
				if(node.communityNum in communityCounts){
					communityCounts[node.communityNum]["count"]++;
				}
				else{
					// Initialize community values if node is the first node from the community encountered
					communityCounts[node.communityNum] = new Object()
					communityCounts[node.communityNum]["count"] = 1;
					communityCounts[node.communityNum]["level"] = 1;
					communityCounts[node.communityNum]["totalCircled"] = 0;
				}

				communityNodeNum = communityCounts[node.communityNum]["count"] // n wherein the current node is the nth node in its community
				circleLevel = communityCounts[node.communityNum]["level"]; // integer representing the level in the circle wherein 1 is the innermost circle of the community
				totalCircled = communityCounts[node.communityNum]["totalCircled"]; // total number of nodes already in complete circles in the community
				circleNodeNum = communityNodeNum - totalCircled; // n wherein the current node is the nth node in its displayed circle in the community
				circleSize = 0.2 * circleLevel; // size of the current circle
				circleLimit = Math.pow(2, circleLevel) + 3; // maximum number of nodes in the displayed circle
				angle = 360 / circleLimit * circleNodeNum * Math.PI / 180; // value of the angle separating each node in the circle

				// Set node values
				node.x = circleSize * Math.cos(angle);
				node.y = circleSize * Math.sin(angle);
				node.color = getCommunityColor(node);
				node.size = size;

				// Check if we have to move on to the next circle
				if(circleNodeNum >= circleLimit){
					totalCircled += circleLimit;
					circleLevel++;
				}

				// Update community values
				communityCounts[node.communityNum]["level"] = circleLevel;
				communityCounts[node.communityNum]["totalCircled"] = totalCircled;
			});

			// Offset all communities
			s.graph.nodes().forEach(function(node, i, a) {
				node.x = node.x + getCommunityOffset(communityCounts, node)[0];
				node.y = node.y + getCommunityOffset(communityCounts, node)[1];
			});

			// Call refresh to render the new graph
			s.refresh();
		});
}
