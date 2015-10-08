/*
 * TODO in order of listing:
 * - play/pause
 * - api: GET time + sim.updateTime() with given or rq
 * - grayscale toggle
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
	}

	timeIt = function(f, logTitle) {
		var renderStart = new Date().getTime();
		f();
		var renderTime = new Date().getTime() - renderStart;
		if (logTitle != undefined) console.log("* execution time of " + logTitle + ": " + renderTime + " msec");
		return renderTime;
	}


	/* LOCAL FUNCTIONS */

	var setupListeners = function(simulation) {
		var sim = simulation;
		$('#ctl-playpause').on('click', function(ev) {
			sim.setPaused(!sim.isPaused());
			$('#ctl-playpause').html(sim.isPaused() ? "Play" : "Pause");
		});
		$('#ctl-step').on('click', function(ev) {
			sim.singleStep();
		});
	};

	var main = function(settings) {
		var canvas = document.getElementById('grid-canvas');
		paper.setup(canvas);

		console.log('main: creating simulation');
		sim = new Simulation(settings);

		setupListeners(sim);

		if (settings.autoplay) sim.setPaused(false);
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
