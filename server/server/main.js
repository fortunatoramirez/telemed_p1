var express = require('express');
var app = express();
var server = require('http').Server(app);
var io = require('socket.io')(server);

app.use(express.static('public'));

io.on('connection', function(socket){
	socket.on('nuevo_mensaje', function(data){
		console.log(data);
		io.sockets.emit('desde_servidor',data);
	});
});

server.listen(5001, function(){
	console.log('Servidor corriendo en el puerto 5001.');
});
