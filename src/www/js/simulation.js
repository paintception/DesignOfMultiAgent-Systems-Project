/*
 * Inherits from EventEmitter.
 */
Simulation = function(settings) {
	/* INITIALIZATION */

	this.settings = settings;
	this.isPaused_ = true;
	this.renderTimeoutId = null;

	console.log('simulation: creating grid');
	this.grid = new Grid(this);

	EventEmitter.call(this);

	var self = this;


	/* PUBLIC METHODS */

	//TODO: test
	this.startNew = function(parameters) {
		var data = JSON.stringify({'parameters': parameters});
		console.log("sending new sim with data:", data);
		$.post('http://localhost:8001/sim/new', data, function(response) {
			console.log('POST sim/new response:', response);
		}, 'json');
	};

	this.restart = function(randomizeRoutes) {
		randomizeRoutes = randomizeRoutes || false;
		var data = JSON.stringify({'randomize_routes': randomizeRoutes});
		$.post('http://localhost:8001/sim/restart', data, function(response) {
			console.log('POST sim/restart response:', response);
		}, 'json');
	};

	this.setPaused = function(setPaused) {
		var prevPaused = this.isPaused_;
		if (!setPaused && this.isPaused_) {
			console.log("simulation: unpausing");
			this.isPaused_ = false;

			var self = this;
			var cb = function() {
				renderStep();
				if (!self.isPaused_) {
					self.renderTimeoutId = setTimeout(cb, 1000 / self.settings.fps);
				}
			};
			cb();
		} else if (setPaused && !this.isPaused_) {
			console.log("simulation: pausing");
			this.isPaused_ = true;
			clearTimeout(this.renderTimeoutId);
		}
		if (this.isPaused_ != prevPaused) this.emit('sim:pauseState', {paused: this.isPaused_});
	};

	this.isPaused = function() {
		return this.isPaused_;
	};

	this.singleStep = function() {
		console.log("simulation: single step");
		this.setPaused(true);
		renderStep();
	};

	this.setSetting = function(name, value) {
		if (name in this.settings) {
			var ov = this.settings[name];
			this.settings[name] = value;
			this.emit('sim:settingChanged', {name: name, oldValue: ov, newValue: this.settings[name]});
		}
	};

	this.getSetting = function(name) {
		return this.settings[name];
	};

	this.getSettings = function() {
		return this.settings;
	};

	this.getParameters = function() {
		return this.grid.getParameters();
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

		updateParamsAndGrid(self.grid);

		// renderTime = new Date().getTime() - renderStart;
		// console.log("grid: update took " + renderTime + "msec"); //TODO: fix this timer by wrapping it up inside inner callback
	};

	var updateParamsAndGrid = function(grid) {
		$.getJSON('http://localhost:8001/sim/parameters', function (data) {
			grid.setParameters(data);
			var displayParams = data;
			delete displayParams.routes;
			var repr = "<table>" + Object.keys(data).map(function(x){
				return "<tr><td>" + x + ":</td><td>" + data[x] + "</td></tr>";
			}).join('') + "</table>";
			$('#param-info').html("<b>Simulation parameters</b>: " + repr);

			$.getJSON('http://localhost:8001/sim/grid', function (data) {
				grid.setGridData(data.width, data.height, data.grid);

				var duration = timeIt(function() {
					grid.draw(settings.maxCellSize);
				}, "grid.draw");

				$('#render-info').html("<b>Grid render time</b>: " + duration + " msec");
			});
		}).error(function(err) {
			console.log("getJSON error, server down? -- ", err); //TODO: use this for a connectivity indicator?
		});
	};

	updateParamsAndGrid(this.grid);
};

Simulation.prototype = Object.create(EventEmitter.prototype);
Simulation.prototype.constructor = Simulation;
