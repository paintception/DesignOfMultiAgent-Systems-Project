Simulation = function(settings) {
	/* INITIALIZATION */

	this.settings = settings;

	console.log('simulation: creating grid');
	grid = new Grid(this);


	/* PUBLIC METHODS */

	this.run = function() {
		renderStep(); //first render without delay
		setInterval(renderStep, 1000 / this.settings.fps);
	};

	this.setPaused = function(paused) {
		//TODO: implement
	};

	this.getSettings = function() {
		return this.settings;
	};


	/* PRIVATE METHODS */

	var renderStep = function() {
		// console.log("grid: updating...");
		// renderStart = new Date().getTime();

		var stepStart = new Date().getTime();
		$.getJSON('http://localhost:8001/sim/step', function (data) {
			var stepTime = new Date().getTime() - stepStart;
			$('#sim-info').html("<b>Sim calc time</b>: " + stepTime + " msec");

			$('#time-info').html("<b>Simulation time</b>: " + data.day + ":" + data.step + " (timestamp: " + data.ts + ")");
		});

		updateParamsAndGrid(grid);

		// renderTime = new Date().getTime() - renderStart;
		// console.log("grid: update took " + renderTime + "msec"); //TODO: fix this timer by wrapping it up inside inner callback
	};

	var updateParamsAndGrid = function(grid) {
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
	};
};
