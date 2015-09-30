window.onload = function() {
	Node = function() {
		this.atQueue = 0;
		this.outQueues = [0, 0, 0, 0];
	}
	Node.prototype.toString = function() {
		return "{ Node - @NESW:" + this.atQueue + "/" + this.outQueues[0] + "/" + this.outQueues[1] + "/" + this.outQueues[2] + "/" + this.outQueues[3] + " }";
	}


	Grid = function(settings) {
		this.settings = settings
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

		this.draw = function() {
			var cs = this.settings.cellSize;
			var rs = new paper.Size(cs, cs);
			console.log("grid size: " + this.width + "x" + this.height + ", cell size: " + rs);

			drawCell = function(v, minV, maxV, x, y) {
				tl = new paper.Point(x * cs, y * cs);
				r = new paper.Shape.Rectangle(tl, rs);
				r.fillColor = 'black'; // non-road color

				if (v >= 0) {
					uv = v * (1.0 / (maxV - minV));
					r.fillColor = new paper.Color(uv, 1.0 - uv, 0.0); //map v to green-red range
				}
			}

			s = this.settings;
			for (y = 0; y < this.height; ++y) {
				for (x = 0; x < this.width; ++x) {
					cc = new paper.Point(x * 3 + 1, y * 3 + 1);
					cell = this.grid[y][x];
					// console.log("[" + x + ", " + y + "]: " + cell);

					drawCell(cell.atQueue, 0, s.maxAtJunction, cc.x, cc.y);
					drawCell(cell.outQueues[0], 0, s.maxInStreet, cc.x, cc.y - 1);
					drawCell(cell.outQueues[1], 0, s.maxInStreet, cc.x + 1, cc.y);
					drawCell(cell.outQueues[2], 0, s.maxInStreet, cc.x, cc.y + 1);
					drawCell(cell.outQueues[3], 0, s.maxInStreet, cc.x - 1, cc.y);

					drawCell(-1, 0, 0, cc.x - 1, cc.y - 1);
					drawCell(-1, 0, 0, cc.x + 1, cc.y - 1);
					drawCell(-1, 0, 0, cc.x - 1, cc.y + 1);
					drawCell(-1, 0, 0, cc.x + 1, cc.y + 1);
				}
			}

			//draw legend (green=0 cars, red=max cars)

			paper.view.draw();
		}
	}


	getRandomInt = function(min, max) {
		return Math.floor(Math.random() * (max - min)) + min;
	}

	main = function(settings) {
		grid = new Grid(settings);
		grid.createDummy(settings.gridSize, settings.gridSize);
		// console.log('grid: ' + grid);
		grid.draw();
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
};
