var socket = io.connect('http://localhost:5001', {'forceNew':true});


socket.on('desde_servidor',function(data){
	render_data(data);
});


function render_data(data)
{
	document.getElementById('div_dato').innerHTML = data;
}




