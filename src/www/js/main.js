/*
 * TODO in order of listing:
 * - initial load speed
 * - split Grid into new file, create Simulation object (also separate) with settings
 * - prepare for graphs
 * - grayscale toggle
 * - add text to legend
 * - editable parameters (create fields for them)
 * - play/pause + set speed
 * - draw grid without the non-existing streets at the edges
 * - api: GET agents + view them
 * - api: POST sim/new with parameters object to be able to restart
 * - make drawing more efficient? (don't recreate objects?)
 * - add explosions
 */
$(document).ready(function() {
	getRandomInt = function(min, max) {
		return Math.floor(Math.random() * (max - min)) + min;
	}

	timeIt = function(f, logTitle) {
		var renderStart = new Date().getTime();
		f();
		var renderTime = new Date().getTime() - renderStart;
		if (logTitle != undefined) console.log("* execution time of " + logTitle + ": " + renderTime + " msec");
		return renderTime;
	}

	updateParamsAndGrid = function(grid) {
		$.getJSON('http://localhost:8001/sim/parameters', function (data) {
			grid.setParameters(data);
			repr = "<table>" + Object.keys(data).map(function(x){
				return "<tr><td>" + x + ":</td><td>" + data[x] + "</td></tr>";
			}).join('') + "</table>";
			$('#param-info').html("<b>Simulation parameters</b>: " + repr);

			$.getJSON('http://localhost:8001/sim/grid', function (data) {
				grid.setGridData(data.width, data.height, data.grid);
				duration = timeIt(function() {
					grid.draw(settings.maxCellSize);
				}, "grid.draw");
				$('#render-info').html("<b>Grid render time</b>: " + duration + " msec");
			});
		}).error(function(err) {
			console.log("getJSON error, server down? -- ", err); //TODO: use this for a connectivity indicator?
		});
	}

	main = function(settings) {
		grid = new Grid();
		setInterval(function() {
			// console.log("grid: updating...");
			renderStart = new Date().getTime();

			var stepStart = new Date().getTime();
			$.getJSON('http://localhost:8001/sim/step', function (data) {
				var stepTime = new Date().getTime() - stepStart;
				console.log("grid: step done in " + stepTime + " msec", data);
				$('#time-info').html("<b>Simulation time</b>: " + data.day + ":" + data.step + " (timestamp: " + data.ts + ")");
			});

			updateParamsAndGrid(grid);

			renderTime = new Date().getTime() - renderStart;
			// console.log("grid: update took " + renderTime + "msec"); //TODO: fix this timer by wrapping it up inside inner callback
		}, 1000 / settings.fps);
	}


	//--------------------------------------


	var canvas = document.getElementById('grid-canvas');
	paper.setup(canvas);
	settings = {
		// 'grid_width': 15,
		// 'grid_height': 15,
		// 'junction_capacity': 5,
		// 'street_capacity': 10,

		'maxCellSize': 1000,
		'grayscale': true,
		'colorizeLowOffset': 0.2,
		'fps': 0.2
	}

	main(settings);
});
