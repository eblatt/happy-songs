var margin = {top: 20, right: 20, bottom: 20, left: 20};
	width = 800 - margin.left - margin.right,
	height = 500 - margin.top - margin.bottom,
	formatPercent = d3.format(".1%");

var svg = d3.select("#map").append("svg")
	.attr("width", width + margin.left + margin.right)
	.attr("height", height + margin.top + margin.bottom)
	.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var projection = d3.geo.mercator()
  .scale(70)
  .center([0,20])
  .translate([width / 2, height / 2]);

tooltip = d3.select("body").append("div")
	.attr("class", "tooltip")
	.style("opacity", 0);


queue()
	.defer(d3.csv, "2017_happiness.csv")
	.defer(d3.json, "https://raw.githubusercontent.com/holtzy/D3-graph-gallery/master/DATA/world.geojson")
	.defer(d3.csv, "map_new.csv")
	.await(ready);
	

var legendText = ["", "2", "", "4", "", "6", "", "8"];
var legendColors = ["#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02"];


function ready(error, data, us, songs) {

		var color = d3.scale.threshold()
		.domain([2,3,4,5,6,7,8,9])
		.range(["#fff7bc", "#fee391", "#fec44f", "#fe9929", "#ec7014", "#cc4c02", "#993404", "#662506", "#662666", "#5A421F"]);




		console.log(songs)
		var myMap = new Map();
		data.forEach(function(d) {
			myMap.set(d.country_name, d.score)

			});
		var songMap = new Map();
		songs.forEach(function(d){
			songMap.set(d.country, d.track)
		});
		var artistMap = new Map();
		songs.forEach(function(d){
			artistMap.set(d.country, d.artist)
		});
		var speechMap = new Map();
		songs.forEach(function(d){
			speechMap.set(d.country, d.avg_speech)
		});


	var path = d3.geo.path()
		         .projection(projection);

	svg.append("g")
       .selectAll("path")
       .data(us.features)
       .enter()
       .append("path")
      // draw each country
       .attr("d", d3.geo.path()
       .projection(projection)
        );


	var countyShapes = svg.selectAll(".country")
    	.data(us.features)
    	.enter()
		.append("path")
		.attr("class", "country")
		.attr("d", path);

	countyShapes
		.on("mouseover", function(d) {
			tooltip.transition()
			.duration(250)
			.style("opacity", 1);
			tooltip.html(
			"<p><strong>" + d.properties.name + "</strong></p>" +
			"<table><tbody><tr><td class='wide'>Happiness Score:</td><td>" + myMap.get(d.properties.name) + "</td></tr>" +
			"<tr><td>Popular Song:</td><td>" + songMap.get(d.properties.name) + ", " + artistMap.get(d.properties.name) + "</td></tr>" +
			"<tr><td>Average Speechiness:</td><td>" + speechMap.get(d.properties.name) + "</td></tr></tbody></table>"
			)
			.style("left", (d3.event.pageX + 15) + "px")
			.style("top", (d3.event.pageY - 28) + "px");
		})
		.on("mouseout", function(d) {
			tooltip.transition()
			.duration(250)
			.style("opacity", 0);
		});


	countyShapes.style("fill", function(d) {
		var score = myMap.get(d.properties.name) || 0;
        //console.log(d.properties.name)
        //console.log(Math.floor(score));
        return color(score);
		});



	var legend = svg.append("g")
		.attr("id", "legend");

	var legenditem = legend.selectAll(".legenditem")
		.data(d3.range(8))
		.enter()
		.append("g")
			.attr("class", "legenditem")
			.attr("transform", function(d, i) { return "translate(" + i * 31 + ",0)"; });

	legenditem.append("rect")
		.attr("x", width - 240)
		.attr("y", -7)
		.attr("width", 30)
		.attr("height", 6)
		.attr("class", "rect")
		.style("fill", function(d, i) { return legendColors[i]; });

	legenditem.append("text")
		.attr("x", width - 240)
		.attr("y", -10)
		.style("text-anchor", "middle")
		.text(function(d, i) { return legendText[i]; });


}

d3.select(self.frameElement).style("height", "685px");