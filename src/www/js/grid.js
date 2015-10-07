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

	Grid = function() {
		// //enforce proper instantiation, we don't want 'window' as this...
		// if (!(this instanceof Grid)) return new Grid();

		this.parameters = {}
		this.grid = [];
		this.width = 0;
		this.height = 0;

		this.setParameters = function(parameters) {
			this.parameters = parameters;
			// console.log("grid: set parameters", parameters);
		};

		this.setGridData = function(w, h, gridData) {
			this.width = w;
			this.height = h;
			this.grid = gridData;
			// console.log("grid: set grid of " + w + "*" + h, gridData);
		};

		this.draw = function(maxCellSize) {
			var cs;
			{
				csz = paper.view.viewSize;
				//grid sizes * 3 because we need 3*3 room per junction
				canvasXMax = csz.width / (this.width * 3);
				canvasYMax = csz.height / (this.height * 3);
				cs = Math.min(canvasXMax, canvasYMax, maxCellSize);
			}
			console.log("grid.draw(): grid size: " + this.width + "x" + this.height + ", cell size: " + cs);

			var mapToColor = function(v, minV, maxV, lowOffset, grayscale) {
				colorScale = v * (1.0 / (maxV - minV));
				colorScale = colorScale * (1.0 - lowOffset) + lowOffset;
				if (!grayscale) {
					rectColor = new paper.Color(colorScale, 1.0 - colorScale, 0.0); //map v to green-red range
				} else {
					rectColor = new paper.Color(colorScale, colorScale, colorScale); //map v to black-white range
				}

				return rectColor;
			}

			var drawCell = function(v, minV, maxV, x, y, cellType) {
				if (v == null) v = []; //TEMP: convert nulls (border streets) to empty streets
				if (v != -1) v = v.length; //take the length of the array (which is filled with agent IDs)

				var cellType = cellType || 'none';
				var cx = x * cs, cy = y * cs;

				/* cell background */
				var rectColor = 'black'; //non-road color
				if (v >= 0) {
					rectColor = mapToColor(v, minV, maxV, 0.2, false);
				}
				var rectParams = {
					topLeft: [cx, cy],
					size: [cs, cs],
					fillColor: rectColor
				}
				var rect = new paper.Shape.Rectangle(rectParams);

				/* white stripes */
				var stripeParams = {
					strokeWidth: 1,
					strokeColor: 'white',
					dashArray: [3, 1]
				}
				var stripe; //not sure how paper.js does drawing or keeps its references, but without this 'predeclaration' here, drawing breaks.
				if (cellType == 'junction') {
					stripeParams.topLeft = [cx, cy];
					stripeParams.size = [cs, cs];
					stripeParams.strokeWidth = 2;
					stripe = paper.Shape.Rectangle(stripeParams);
				} else if (cellType == 'hstreet') {
					stripeParams.from = [cx, cy + cs / 2];
					stripeParams.to = [cx + cs, cy + cs / 2];
					stripe = new paper.Path.Line(stripeParams);
				} else if (cellType == 'vstreet') {
					stripeParams.from = [cx + cs / 2, cy];
					stripeParams.to = [cx + cs / 2, cy + cs];
					stripe = new paper.Path.Line(stripeParams);
				} else {
					// var numDots = 10, greyLevel = 0.25;
					// var dp = { fillColor: new paper.Color(greyLevel), radius: 1 };
					// for (i = 0; i < numDots; ++i) {
					// 	dp.center = [cx + getRandomInt(1, cs - 2), cy + getRandomInt(1, cs - 2)];
					// 	stripe = new paper.Shape.Circle(dp);
					// }
				}
			};

			var drawLegend = function() {
				var edgeDist = 7, barWidth = 150, barHeight = 20;
				var x = edgeDist, y = paper.view.viewSize.height - edgeDist - barHeight;

				var bar = paper.Shape.Rectangle({
					topLeft: [x, y],
					size: [barWidth, barHeight],
					strokeWidth: 1,
					strokeColor: 'black'
				});
				bar.fillColor = {
					gradient: { //Note: the gradient behaves strangely, adding a third stop somehow fixes that
						stops: [mapToColor(0, 0, 10, 0.2, false), mapToColor(10, 0, 10, 0.2, false), 'blue']
					},
					origin: [0, 0], destination: [barWidth, 0]
				};
				return bar;
			};

			p = this.parameters;
			jc = p.junction_capacity, sc = p.street_capacity;
			w = this.width, h = this.height;
			for (y = 0; y < h; ++y) {
				for (x = 0; x < w; ++x) {
					var cx = x * 3 + 1, cy = y * 3 + 1;
					var cell = this.grid[y][x];

					drawCell(cell.main, 0, jc, cx, cy, 'junction');
					drawCell(cell.streets[0], 0, sc, cx, cy - 1, 'vstreet');
					drawCell(cell.streets[1], 0, sc, cx + 1, cy, 'hstreet');
					drawCell(cell.streets[2], 0, sc, cx, cy + 1, 'vstreet');
					drawCell(cell.streets[3], 0, sc, cx - 1, cy, 'hstreet');

					drawCell(-1, 0, 0, cx - 1, cy - 1);
					drawCell(-1, 0, 0, cx + 1, cy - 1);
					drawCell(-1, 0, 0, cx - 1, cy + 1);
					drawCell(-1, 0, 0, cx + 1, cy + 1);
				}
			}

			var legend = drawLegend();

			paper.view.draw();
		}
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
