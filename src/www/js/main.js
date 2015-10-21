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
	/* 'PUBLIC' UTILITY FUNCTIONS (polluting global namespace...) */

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

	var agentsTable = null;


	/* LOCAL FUNCTIONS */

	var setupInterface = function() {
		$('#tabs').tabs({'active': 0});

		var parens = function(data, type, full, meta) {
			return "(" + data + ")";
		};

		agentsTable = $('#agents').DataTable({
			// paging: false,
			'iDisplayLength': 25,
			select: 'single',
			ajax: {
				url: '/sim/agents',
				dataSrc: ''
			}, columns: [
				{data: 'name'},
				{ data: 'position', 'render': parens},
				{data: 'start', 'render': parens},
				{data: 'destination', 'render': parens},
				{data: 'path'},
				{data: 'start_time'},
				{data: 'stuck_time'},
				{data: 'total_path_distance'}
			]
		});
		agentsTable.on('select', function(e, dt, type, indexes) {
			if (type === 'row') {
				var name = dt.rows(indexes).data().pluck('name')[0];
				var wt = dt.rows(indexes).data().pluck('waiting_times')[0]; //waiting_times list
				var wtDump = ["<i>Waiting times for agent " + name + ":</i>"];
				for (var tl_time in wt) { //loop over travel logs (start_time => [(x,y,w), (x,y,w), ...])
					var tl_log = wt[tl_time];
					var dayLog = "Travel started at " + tl_time + ": ";

					var dayLogItems = [];
					for (var wp in tl_log) { //(x,y,w) waypoints + waiting times during travel
						var item = tl_log[wp];
						dayLogItems.push("(" + item[0] + "," + item[1] + ")[<b>" + item[2] + "</b>]");
					}
					wtDump.push(dayLog + dayLogItems.join(" -> "));
				}
				console.log(wtDump.join("<br>\n"));
				$('#agent-details').html(wtDump.join("<br>\n"));
			}
		});
	};

	//TODO: implement
	var getSimParamsFromDOM = function(baseParams) {
		var params = baseParams;
		// TODO
		// params.value1 = $('param-cfg param1').value();
		return params;
	};

	var setupListeners = function(simulation) {
		var sim = simulation;
		$('#ctl-new').on('click', function(ev) {
			sim.startNew(getSimParamsFromDOM(sim.getParameters()));
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

		setupInterface();

		console.log('main: creating simulation');
		var sim = new Simulation(settings, agentsTable);

		setupListeners(sim);

		sim.setPaused(!settings.autoplay);
	};


	/* ENTRY POINT */
	main({
		'maxCellSize': 1000,
		'grayscale': true,
		'colorizeLowOffset': 0.2,
		'autoplay': false,
		'fps': 2
	});
});
