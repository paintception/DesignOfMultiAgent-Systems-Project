/*eslint new-cap:0 */

var simulationData = {
    labels : ["Day 1", "Day 2", "Day 3", "Day.."],  // Days of the simulation
    datasets : [
        {
            //PYTHON RESULTS
            label  : "Before Simulation",
            fillColor : "rgba(0,0,255,0.5)",
            strokeColor : "#ACC26D",
            pointColor : "#fff",
            pointStrokeColor : "#9DB86D",
            data : [203, 156, 99, 251, 305]  // Random data
        },
        {
            label : "After Simulation",
            fillColor : "rgba(255,255,0,0.5)",
            strokeColor : "#ACC26D",
            pointColor : "#fff",
            pointStrokeColor : "#9DB86D",
            data : [100, 200, 300, 305, 402]
        }
    ]
};

// get line chart canvas
var simCanvas = document.getElementById('speed_average').getContext('2d');
// draw line chart
new Chart(simCanvas).Line(simulationData);


var fuelData = {
    labels : ["Day 1", "Day 2", "Day 3", "Day.."],
    datasets: [
        {
            label: "My First dataset",
            fillColor: "rgba(220,220,220,0.5)",
            strokeColor: "rgba(220,220,220,0.8)",
            highlightFill: "rgba(220,220,220,0.75)",
            highlightStroke: "rgba(220,220,220,1)",
            data: [65, 59, 80, 81, 56, 55, 40]
        },
        {
            label: "My Second dataset",
            fillColor: "rgba(151,187,205,0.5)",
            strokeColor: "rgba(151,187,205,0.8)",
            highlightFill: "rgba(151,187,205,0.75)",
            highlightStroke: "rgba(151,187,205,1)",
            data: [28, 48, 40, 19, 86, 27, 90]
        }
    ]
};

var fuelCanvas = document.getElementById('fuel_average').getContext('2d');
// draw bar chart
new Chart(fuelCanvas).Bar(fuelData);


var pieDataBefore = [
    {
        value: 65,
        color:"rgba(255,0,0,0.9)"
    },
    {
        value : 35,
        color : "rgba(0,255,0,0.9)"
    }
];

var pieDataAfter = [
    {
        value: 5,
        color:"rgba(255,0,0,0.9)"
    },
    {
        value : 95,
        color : "rgba(0,255,0,0.9)"
    }
];

// pie chart options
var pieOptions = {
     segmentShowStroke : false,
     animateScale : true
};
// get pie chart canvas
var pieGraph1 = document.getElementById("pie").getContext("2d");
var pieGraph2 = document.getElementById("pie2").getContext("2d");
// draw pie chart
new Chart(pieGraph1).Pie(pieDataBefore, pieOptions);
new Chart(pieGraph2).Pie(pieDataAfter, pieOptions);
