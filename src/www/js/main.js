/*
 * TODO in order of listing:
 * - api: POST max simulation days
 * - start webserver from main (to have cmdline options+output+webUI) -- https://docs.python.org/2/howto/curses.html
 * - api: GET time + sim.updateTime() with given or rq
 * - set speed
 * - TABS: for graphs and possibly agents (https://jqueryui.com/tabs/)
 * - add text to legend
 * - editable parameters (create fields for them)
 * - draw grid without the non-existing streets at the edges
 * - api: GET agents + view them
 * - api: POST sim/new with parameters object to be able to restart
 * - make drawing more efficient? (don't recreate objects?)
 * - initial load speed (it's allright now, after the setInterval fix?)
 * - add explosions
 */
$(document).ready(function() {
	/* 'PUBLIC' UTILITY FUNCTIONS (poluting global namespace...) */

	getRandomInt = function(min, max) {
		return Math.floor(Math.random() * (max - min)) + min;
	};

	timeIt = function(f, logTitle) {
		var renderStart = new Date().getTime();
		f();
		var renderTime = new Date().getTime() - renderStart;
		if (logTitle != undefined) console.log("* execution time of " + logTitle + ": " + renderTime + " msec");
		return renderTime;
	};


	/* LOCAL FUNCTIONS */

	//TODO: implement
	var getSimParamsFromDOM = function() {
		return {'var1': 23, 'var2': true};
	var setupListeners = function(simulation) {
		var sim = simulation;
		$('#ctl-new').on('click', function(ev) {
			sim.startNew(getSimParamsFromDOM());
		});

		$('#ctl-restart').on('click', function(ev) {
			sim.restart(false);
		});

		$('#ctl-playpause').on('click', function(ev) {
			sim.setPaused(!sim.isPaused());
		});
		sim.on('sim:pauseState', function(data) {
			$('#ctl-playpause').html(data.paused ? "Play" : "Pause");
		});

		$('#ctl-step').on('click', function(ev) {
			sim.singleStep();
		});

		$('#ctl-grayscale').on('click', function(ev) {
			sim.setSetting('grayscale', !sim.getSetting('grayscale'));
		});

		sim.on('sim:settingChanged', function(data) {
			switch (data.name) {
			case 'grayscale':
				$('#ctl-grayscale').html(data.newValue ? "Color mode" : "Grayscale mode");
				break;
			}
		});
	};

	var main = function(settings) {
		var canvas = document.getElementById('grid-canvas');
		paper.setup(canvas);

		console.log('main: creating simulation');
		var sim = new Simulation(settings);

		setupListeners(sim);

		sim.setPaused(!settings.autoplay);
	};


	/* ENTRY POINT */
	main({
		'maxCellSize': 1000,
		'grayscale': true,
		'colorizeLowOffset': 0.2,
		'autoplay': false,
		'fps': 1
	});
});
