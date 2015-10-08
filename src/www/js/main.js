/*
 * TODO in order of listing:
 * - TABS: for graphs and possibly agents (https://jqueryui.com/tabs/)
 * - grayscale toggle
 * - add text to legend
 * - editable parameters (create fields for them)
 * - play/pause + set speed
 * - draw grid without the non-existing streets at the edges
 * - api: GET agents + view them
 * - api: POST sim/new with parameters object to be able to restart
 * - make drawing more efficient? (don't recreate objects?)
 * - initial load speed (it's allright now, after the setInterval fix?)
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

	main = function(settings) {
		var canvas = document.getElementById('grid-canvas');
		paper.setup(canvas);

		console.log('main: creating simulation');
		sim = new Simulation(settings);
		sim.run();
	}


	/* ENTRY POINT */
	main({
		'maxCellSize': 1000,
		'grayscale': true,
		'colorizeLowOffset': 0.2,
		'fps': 2
	});
});
