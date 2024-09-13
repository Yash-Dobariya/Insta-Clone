var socket = io.connect('http://' + document.domain + ':' + location.port);

var yourUserId = 1;
var yourStatus = true;
socket.emit('status_update', { user_id: yourUserId, status: yourStatus });
