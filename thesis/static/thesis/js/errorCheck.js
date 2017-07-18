var ErrorChecking = {
	initializeErrorCheck : function(){
		ErrorChecking.disableCommunityGeneration();

		$("#selectAlgorithm").bind("change", function(){
			ErrorChecking.checkIfValid();
		});

		$("#selectParameter").bind("change", function(){
			ErrorChecking.checkIfValid();
		});


	},

	checkIfValid : function(){
		if($("#selectAlgorithm").val() > 0
			&& $("#selectParameter").val() >0){

			if($("#selectAlgorithm").val() == ALGO_KMEANS){
				if($("#selectK").val() != ""){
					ErrorChecking.enableCommunityGeneration();
				}
				else{
					ErrorChecking.disableCommunityGeneration();
				}
			}
			else{
				ErrorChecking.enableCommunityGeneration();
			}
		}
	},

	enableCommunityGeneration : function(){
		$("button.generateCommunities").removeAttr("disabled");
	},

	disableCommunityGeneration : function(){
		$("button.generateCommunities").attr("disabled", true);
	}
}

