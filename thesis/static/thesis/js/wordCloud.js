var MAX_TRIES;
var CLOUDTYPE_TWEETS = 0;
var CLOUDTYPE_PROFILE = 1;

var WordCloud = {
	wordsWidth : 280,
	wordsHeight : 450,
	communities : null,
	communityNum : null,
	maxCount : null,
	generateWordCloud : function(communities, communityNum, maxCount, type){
		WordCloud.communities = communities;
		WordCloud.communityNum = communityNum;
		WordCloud.maxCount = maxCount;

		// var fill = d3.scale.category20();

		// for small screens (and slow cpu's) limit retries
		MAX_TRIES = (WordCloud.wordsWidth > 400) ? 6 : 3;

		// draw initial cloud wilthout filters
		WordCloud.generateCloud(type);
	},
	generateCloud : function (type, retryCycle) {
	    var skillsToDraw = WordCloud.transformToCloudLayoutObjects(WordCloud.communities[WordCloud.communityNum].slice(0,WordCloud.maxCount), retryCycle);
	    d3.layout.cloud()
	        .size([WordCloud.wordsWidth, WordCloud.wordsHeight])
	        .words(skillsToDraw)
	        .rotate(function() {
	            return ~(Math.random() * 2) * 90;
	        })
	        .font("Bebas Neue")
	        .fontSize(function(d) {
	            return d.size;
	        })
	        .on("end", function(fittedSkills) {
	            // check if all words fit and are included
	            if (fittedSkills.length == skillsToDraw.length) {
	                WordCloud.drawCloud(fittedSkills, type); // finished
	            }
	            else if (!retryCycle || retryCycle < MAX_TRIES) {
	                // words are missing due to the random placement and limited room space
	                // console.debug('retrying');
	                // try again and start counting retries
	                WordCloud.generateCloud(type, (retryCycle || 1) + 1);
	            }
	            else {
	                // retries maxed and failed to fit all the words
	                // console.debug('gave up :(');
	                // just draw what we have
	                WordCloud.drawCloud(fittedSkills, type);
	            }
	        })
	        .start();
	},
	// convert skill objects into cloud layout objects
	transformToCloudLayoutObjects : function(list, retryCycle) {
        return _.map(list, function(community) {
            return {
                text: community.text,
                size: community.size
            };
        });
    },
    drawCloud : function(words, type) {
    	var divClass = "community-wordcloud";
    	if(type == CLOUDTYPE_PROFILE){
    		divClass = "community-profilecloud";
    	}
    	
        d3.select(".community[data-cNum='" + WordCloud.communityNum + "'] ." + divClass).append("svg")
            .attr("width", WordCloud.wordsWidth)
            .attr("height", WordCloud.wordsHeight)
            .append("g")
            .attr("transform", "translate(" + ~~(WordCloud.wordsWidth / 2) + "," + ~~(WordCloud.wordsHeight / 2) + ")")
            .selectAll("text")
            .data(words)
            .enter().append("text")
            .style("font-size", function(d) {
                return d.size + "px";
            })
            .style("-webkit-touch-callout", "none")
            .style("-webkit-user-select", "none")
            .style("-khtml-user-select", "none")
            .style("-moz-user-select", "none")
            .style("-ms-user-select", "none")
            .style("user-select", "none")
            .style("cursor", "default")
            .style("font-family", "Bebas Neue")
            .style("fill", "rgb(60,60,60)")
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
            .text(function(d) {
                return d.text;
            });

        if(type == CLOUDTYPE_TWEETS){
        	// set the viewbox to content bounding box (zooming in on the content, effectively trimming whitespace)
	        $(".community-wordcloud svg").each(function(){
	        	var wordSVG = this;
	        	var bbox = wordSVG.getBBox();
		        var viewBox = [bbox.x, bbox.y, bbox.width, bbox.height].join(" ");
		        wordSVG.setAttribute("viewBox", viewBox);
	        });
        }
        else if(type == CLOUDTYPE_PROFILE){
        	console.log("type is profile")
        	// set the viewbox to content bounding box (zooming in on the content, effectively trimming whitespace)
	        $(".community-profilecloud svg").each(function(){
	        	var wordSVG = this;
	        	var bbox = wordSVG.getBBox();
		        var viewBox = [bbox.x, bbox.y, bbox.width, bbox.height].join(" ");
		        wordSVG.setAttribute("viewBox", viewBox);
	        });
        }
    }
}

/**
 * 1. Determine font size based on years of experience relative to the skills with the least and most years of experience.
 * 2. Further increase / decrease font size based on relevancy (linux 20y is could less relevant than java 3y, so relevancy 
 *    .2 vs 1.5 could work for example).
 */
// function toFontSize(relevancy, retryCycle) {
//     // translate years scale to font size scale and apply relevancy factor
//     // var lineairSize = (((years - minyears) / (maxyears - minyears)) * (maxfont - minfont) * relevancy) + minfont;
//     var lineairSize = relevancy / maxrelevancy * (maxfont - minfont) + minfont;
//     // make the difference between small sizes and bigger sizes more pronounced for effect
//     var polarizedSize = Math.pow(lineairSize / 8, 3);
//     // reduce the size as the retry cycles ramp up (due to too many words in too small space)
//     var reduceSize = polarizedSize * ((MAX_TRIES - retryCycle) / MAX_TRIES);
//     return ~~reduceSize;
// }