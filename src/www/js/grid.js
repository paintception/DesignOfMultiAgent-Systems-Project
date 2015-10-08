/*
 * speed:
 * - create legend object once, redraw every time, or does this happen automatically?
 * - paper.view.draw(), paper.view.update() ... how does this work?
 */
Grid = function(simulation) {
	// //enforce proper instantiation, we don't want 'window' as this...
	// if (!(this instanceof Grid)) return new Grid();

	this.simulation = simulation;
	this.parameters = {};
	this.grid = [];
	this.width = 0;
	this.height = 0;

	this.setParameters = function(parameters) {
		this.parameters = parameters;
	};

	this.setGridData = function(w, h, gridData) {
		this.width = w;
		this.height = h;
		this.grid = gridData;
	};

	this.draw = function(maxCellSize) {
		var cs;
		{
			var csz = paper.view.viewSize;
			//grid sizes * 3 because we need 3*3 room per junction
			var canvasXMax = csz.width / (this.width * 3);
			var canvasYMax = csz.height / (this.height * 3);
			cs = Math.min(canvasXMax, canvasYMax, maxCellSize);
		}
		console.log("grid.draw(): grid size: " + this.width + "x" + this.height + ", cell size: " + cs);

		//Remove everything from last draw, reusing objects or creating multiple layers or canvases would really be better
		paper.project.activeLayer.removeChildren();

		var p = this.parameters;
		var jc = p.junction_capacity, sc = p.street_capacity;
		var w = this.width, h = this.height;
		for (var y = 0; y < h; ++y) {
			for (var x = 0; x < w; ++x) {
				var cx = x * 3 + 1, cy = y * 3 + 1;
				var cell = this.grid[y][x];

				this._drawCell(cell.main, 0, jc, cx, cy, cs, 'junction');
				this._drawCell(cell.streets[0], 0, sc, cx, cy - 1, cs, 'vstreet');
				this._drawCell(cell.streets[1], 0, sc, cx + 1, cy, cs, 'hstreet');
				this._drawCell(cell.streets[2], 0, sc, cx, cy + 1, cs, 'vstreet');
				this._drawCell(cell.streets[3], 0, sc, cx - 1, cy, cs, 'hstreet');

				this._drawCell(-1, 0, 0, cx - 1, cy - 1, cs);
				this._drawCell(-1, 0, 0, cx + 1, cy - 1, cs);
				this._drawCell(-1, 0, 0, cx - 1, cy + 1, cs);
				this._drawCell(-1, 0, 0, cx + 1, cy + 1, cs);
			}
		}

		drawLegend.call(this);

		paper.view.draw();
	};


	/* PRIVATE FUNCTIONS */

	//Note: _drawCell requires this context so we use python prefix style instead of a var here
	this._drawCell = function(v, minV, maxV, x, y, cellSize, cellType) {
		if (v == null) v = []; //TEMP: convert nulls (border streets) to empty streets
		if (v != -1) v = v.length; //take the length of the array (which is filled with agent IDs)

		cellType = cellType || 'none';
		var cx = x * cellSize, cy = y * cellSize;

		var settings = this.simulation.getSettings();
		var lowOffset = settings.colorizeLowOffset, grayscale = settings.grayscale;

		/* cell background */
		var rectColor = 'black'; //non-road color
		if (v >= 0) {
			rectColor = mapToColor(v, minV, maxV, lowOffset, grayscale);
		}
		var rectParams = {
			topLeft: [cx, cy],
			size: [cellSize, cellSize],
			fillColor: rectColor
		};
		var rect = new paper.Shape.Rectangle(rectParams);

		/* white stripes */
		var stripeParams = {
			strokeWidth: 1,
			strokeColor: 'white',
			dashArray: [3, 1]
		};
		var stripe; //not sure how paper.js does drawing or keeps its references, but without this 'predeclaration' here, drawing breaks.
		if (cellType == 'junction') {
			stripeParams.topLeft = [cx, cy];
			stripeParams.size = [cellSize, cellSize];
			stripeParams.strokeWidth = 2;
			stripe = new paper.Shape.Rectangle(stripeParams);
		} else if (cellType == 'hstreet') {
			stripeParams.from = [cx, cy + cellSize / 2];
			stripeParams.to = [cx + cellSize, cy + cellSize / 2];
			stripe = new paper.Path.Line(stripeParams);
		} else if (cellType == 'vstreet') {
			stripeParams.from = [cx + cellSize / 2, cy];
			stripeParams.to = [cx + cellSize / 2, cy + cellSize];
			stripe = new paper.Path.Line(stripeParams);
		} else {
			// var numDots = 10, greyLevel = 0.25;
			// var dp = { fillColor: new paper.Color(greyLevel), radius: 1 };
			// for (i = 0; i < numDots; ++i) {
			// 	dp.center = [cx + getRandomInt(1, cellSize - 2), cy + getRandomInt(1, cellSize - 2)];
			// 	stripe = new paper.Shape.Circle(dp);
			// }
		}
	};

	var drawLegend = function() {
		var edgeDist = 7, barWidth = 150, barHeight = 20;
		var x = edgeDist, y = paper.view.viewSize.height - edgeDist - barHeight;
		var settings = this.simulation.getSettings();
		var lowOffset = settings.colorizeLowOffset, grayscale = settings.grayscale;

		var bar = new paper.Shape.Rectangle({
			topLeft: [x, y],
			size: [barWidth, barHeight],
			strokeWidth: 1,
			strokeColor: 'black'
		});
		bar.fillColor = {
			gradient: { //Note: the gradient behaves strangely, adding a third stop somehow fixes that
				stops: [mapToColor(0, 0, 10, lowOffset, grayscale), mapToColor(10, 0, 10, lowOffset, grayscale), 'blue']
			},
			origin: [0, 0], destination: [barWidth, 0]
		};
		return bar;
	};

	var mapToColor = function(v, minV, maxV, lowOffset, grayscale) {
		var colorScale = v * (1.0 / (maxV - minV));
		colorScale = colorScale * (1.0 - lowOffset) + lowOffset;
		var rectColor;
		if (!grayscale) {
			rectColor = new paper.Color(colorScale, 1.0 - colorScale, 0.0); //map v to green-red range
		} else {
			rectColor = new paper.Color(colorScale, colorScale, colorScale); //map v to black-white range
		}

		return rectColor;
	};
};
