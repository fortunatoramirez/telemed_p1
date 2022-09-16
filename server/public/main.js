var socket = io.connect('http://localhost:5001', {'forceNew':true});
var aviso;
var explodedValues = [0];


socket.on('desde_servidor',function(data){
	render_data(data);
});


function render_data(data)
{

	explodedValues[0] = parseFloat(data);
	drawVisualization();

	document.getElementById('div_dato').innerHTML = data;

	if(data < 2.5)
	{
		aviso = 'NORMAL';
	}
	else
	{
		aviso = 'PELIGRO';
	}

	document.getElementById('div_aviso').innerHTML = aviso;

}



/* GRAFICANDO LOS DATOS */
function drawVisualization() {
    // Create and populate the data table from the values received via websocket
    var data = google.visualization.arrayToDataTable([
        ['Tracker', '1'],
        ['Amplitud', explodedValues[0]]
    ]);
    
    // use a DataView to 0-out all the values in the data set for the initial draw
    var view = new google.visualization.DataView(data);
    view.setColumns([0, {
        type: 'number',
        label: data.getColumnLabel(1),
        calc: function () {return 0;}
    }]);
    
    // Create and draw the plot
    var chart = new google.visualization.BarChart(document.getElementById('visualization'));
    
    var options = {
        title:"Valor de amplitud",
        width: 1200,
        height: 300,
        bar: { groupWidth: "95%" },
        legend: { position: "none" },
        animation: {
            duration: 0
        },
        hAxis: {
            // set these values to make the initial animation smoother
            minValue: 0,
            maxValue: 5
        }
    };
    
    var runOnce = google.visualization.events.addListener(chart, 'ready', function () {
        google.visualization.events.removeListener(runOnce);
        chart.draw(data, options);
    });
    
    chart.draw(view, options);
    
    // you can handle the resizing here - no need to recreate your data and charts from scratch
    /*
    $(window).resize(function() {
        chart.draw(data, options);
    });
    */
}

google.load('visualization', '1', {packages: ['corechart'], callback: drawVisualization});



