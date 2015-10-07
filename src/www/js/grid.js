//window.onload = function() {
$(document).ready(function() {
	Node = function() {
		this.atQueue = 0;
		this.outQueues = [0, 0, 0, 0];
	}
	Node.prototype.toString = function() {
		return "{ Node - @NESW:" + this.atQueue + "/" + this.outQueues[0] + "/" + this.outQueues[1] + "/" + this.outQueues[2] + "/" + this.outQueues[3] + " }";
	}


	Grid = function() {
		this.parameters = {}
		this.grid = [];
		this.width = 0;
		this.height = 0;

		this.createDummy = function(w, h) {
			this.width = w;
			this.height = h;

			this.grid = [];
			for (y = 0; y < h; ++y) {
				row = [];
				for (x = 0; x < w; ++x) {
					n = new Node();

					n.atQueue = this.settings.maxAtJunction;
					// n.atQueue = getRandomInt(0, this.settings.maxAtJunction);
					for (i = 0; i < 4; ++i) n.outQueues[i] = getRandomInt(0, this.settings.maxInStreet);
					// n.atQueue = 0;
					// for (i = 0; i < 4; ++i) n.outQueues[i] = 0;

					row.push(n);
				}
				this.grid.push(row);
			}
		};

		this.setParameters = function(parameters) {
			this.parameters = parameters;
			console.log("grid: set parameters", parameters);
		};

		this.setGridData = function(w, h, gridData) {
			this.width = w;
			this.height = h;
			this.grid = gridData;
			console.log("grid: set grid of " + w + "*" + h, gridData);
		};

		this.draw = function(cellSize) {
			var renderStart = new Date().getTime();
			var cs = cellSize;
			console.log("draw(): grid size: " + this.width + "x" + this.height + ", cell size: " + cs);

			drawCell = function(v, minV, maxV, x, y, cellType) {
				var cellType = cellType || 'none';
				var cx = x * cs, cy = y * cs;

				/* cell background */
				var rectColor = 'black'; //non-road color
				if (v >= 0) {
					colorScale = v * (1.0 / (maxV - minV));
					rectColor = new paper.Color(colorScale, 1.0 - colorScale, 0.0); //map v to green-red range
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
			}

			p = this.parameters;
			for (y = 0; y < this.height; ++y) {
				for (x = 0; x < this.width; ++x) {
					cc = new paper.Point(x * 3 + 1, y * 3 + 1);
					cell = this.grid[y][x];
					// console.log("[" + x + ", " + y + "]: " + cell);

					drawCell(cell.atQueue, 0, p.junction_capacity, cc.x, cc.y, 'junction');
					drawCell(cell.outQueues[0], 0, p.street_capacity, cc.x, cc.y - 1, 'vstreet');
					drawCell(cell.outQueues[1], 0, p.street_capacity, cc.x + 1, cc.y, 'hstreet');
					drawCell(cell.outQueues[2], 0, p.street_capacity, cc.x, cc.y + 1, 'vstreet');
					drawCell(cell.outQueues[3], 0, p.street_capacity, cc.x - 1, cc.y, 'hstreet');

					drawCell(-1, 0, 0, cc.x - 1, cc.y - 1);
					drawCell(-1, 0, 0, cc.x + 1, cc.y - 1);
					drawCell(-1, 0, 0, cc.x - 1, cc.y + 1);
					drawCell(-1, 0, 0, cc.x + 1, cc.y + 1);
				}
			}

			//TODO: draw legend (green=0 cars, red=max cars)

			paper.view.draw();
			var renderTime = new Date().getTime() - renderStart;
			console.log("draw(): drawing completed in " + renderTime + "msec");
		}
	}


	getRandomInt = function(min, max) {
		return Math.floor(Math.random() * (max - min)) + min;
	}

	main = function(settings) {
		grid = new Grid();
		$.getJSON('http://localhost:8001/sim/parameters', function (data) {
			grid.setParameters(data);
		});
		$.getJSON('http://localhost:8001/sim/grid', function (data) {
			grid.setGridData(data.width, data.height, data.grid);
		});
		// grid.draw(settings.cellSize);
	}





	var canvas = document.getElementById('grid-canvas');
	paper.setup(canvas);
	settings = {
		'gridSize': 15,
		'maxAtJunction': 5,
		'maxInStreet': 10,

		'cellSize': 15
	}

	main(settings);
});
//};
