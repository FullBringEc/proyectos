//Objetos importantes de canvas
var canvas = document.getElementById('game')
ctx = canvas.getContext("2d");
//Crear el; objeto de la nave
var nave = {
	x:100,
	y:canvas.height - 100,
	width:50,
	height:50,
	contador:0
}
var juego = {
	estado: 'iniciando'
};
var textoRespuesta = {
	contador:-1,
	titulo:'',
	subtitulo:''
}

var teclado = {};
var disparos = [];
var disparosEnemigos = [];
var enemigos = [];
//DEfinir variables para l;as imagenes
var fondo,imgNave,imgEnemigo,imgDisparo,imgDisparoEnemigo;
var imagenes = ['monstruo.png','nave.png','laserEnemigo.png','laser.png','fondo.jpg']
var soundShoot, soundInvaderShoot, soundDeadSpace, soundDeadInvader, SounEndGame;
var preloader;
//Definicion de funciones
function loadMedia(){
	preloader = new PreloadJS();
	preloader.onProgress = progresoCarga;
	cargar();
	// var imagenes = 
	// fondo = new Image();
	// fondo.src = "image.jpg";
	// fondo.onload = function(){
	// 	var intervalo = window.setInterval(frameLoop,1000/55);
	// }

}
function cargar(){
	while(imagenes.length > 0){
		var imagen = imagenes.shift();
		preloader.loadFile(imagen)
	}
}
function progresoCarga(){
	console.log(parseInt(preloader.progress*100)+"%")
	if(preloader.progress == 1){
		var intervalo = window.setInterval(frameLoop,1000/55);
		fondo = new Image();
		fondo.src = "fondo.jpg";
		imgNave = new Image();
		imgNave.src = "nave.png";
		imgEnemigo = new Image();
		imgEnemigo.src = "monstruo.png";
		imgDisparo = new Image();
		imgDisparo.src = "laserEnemigo.png";
		imgDisparoEnemigo = new Image();
		imgDisparoEnemigo.src = "laser.png";

		soundShoot = document.createElement('audio')
		document.body.appendChild(soundShoot);
		soundShoot.setAttribute('src','laserSpace.wav')

		soundInvaderShoot = document.createElement('audio')
		document.body.appendChild(soundInvaderShoot);
		soundInvaderShoot.setAttribute('src','laserAlien.wav')

		soundDeadSpace = document.createElement('audio')
		document.body.appendChild(soundDeadSpace);
		soundDeadSpace.setAttribute('src','deadSpaceShip.wav')

		soundDeadInvader = document.createElement('audio')
		document.body.appendChild(soundDeadInvader);
		soundDeadInvader.setAttribute('src','deadInvader.wav')

		SounEndGame = document.createElement('audio')
		document.body.appendChild(SounEndGame);
		SounEndGame.setAttribute('src','endGame.wav')
	}
}
function dibujarEnemigos(){
	for(var i in enemigos){
		var enemigo = enemigos[i]
		if(enemigo.estado == 'vivo') ctx.fillStyle = 'red';
		if(enemigo.estado == 'muerto') ctx.fillStyle = 'black';
		ctx.drawImage(imgEnemigo, enemigo.x,enemigo.y,enemigo.width,enemigo.height);
	}
}
function dibujarFondo(){
	ctx.drawImage(fondo,0,0,canvas.width,canvas.height);
}
function dibujarNave(){
	ctx.drawImage(imgNave,nave.x, nave.y,nave.width,nave.height);
}
function agregarEventosTeclado(){
	agregarEventos(document,"keydown",function(e){
		teclado[e.keyCode] = true;
		console.log(e.keyCode);
	})
	agregarEventos(document,"keyup",function(e){
		teclado[e.keyCode] = false;
	})
	function agregarEventos(elemento, nombreEvento, funcion){
		if(elemento.addEventListener){
			//navegadores de verdad
			elemento.addEventListener(nombreEvento,funcion,false);
		}else if(elemento.attachEvent){
			//internet Explorer
			elemento.attachEvent(nombreEvento,funcion);
		}
	}
}
function moverNave(){
	if(teclado[37] == true){
		//movimiente a la izquierda

		nave.x -=6;

		if(nave.x<10) nave.x = 0;
	}
	if(teclado[39] == true){
		//movimiente a la derecha
		var limite = canvas.width - nave.width;
		nave.x +=6;
		if(nave.x>limite) nave.x = limite;
	}
	if(teclado[32] == true){
		if(!teclado.fire){
			fire();
			teclado.fire = true;
		}

	}else{
		teclado.fire = false;
	}
	if(nave.estado == 'hit'){
		nave.contador++;
		if(nave.contador >= 20){
			nave.contador = 0;
			nave.estado = 'muerto';
			juego.estado = 'perdido';
			textoRespuesta.titulo = 'Game Over';
			textoRespuesta.subtitulo = 'Presiona la tecla R para continuar';
			textoRespuesta.contador = 0;
		}
	}
	
}

function dibujarDiparosEnemigos(){
	for(var i in disparosEnemigos){
		var disparo = disparosEnemigos[i];
		ctx.save();
		ctx.fillStyle = 'yellow';
		ctx.drawImage(imgDisparoEnemigo,disparo.x,disparo.y,disparo.width,disparo.height);
		ctx.restore();
		
	}
}
function moverDisparosEnemigos(){
	for (var i in disparosEnemigos) {
		var disparo = disparosEnemigos[i];
		disparo.y +=3;
	}
	disparosEnemigos = disparosEnemigos.filter(function(disparo){
		return disparo.y < canvas.height;
	})
}
function aleatorio(inferior, superior){
	var posibilidades = superior - inferior;
	var a = Math.random()* posibilidades;
	a = Math.floor(a);
	return parseInt(inferior) + a;

}
function actualizaEnemigos(){
	function agregarDisparosEnemigos(enemigo){
		return {
			x:enemigo.x,
			y:enemigo.y,
			width:10,
			height:33,
			contador:0

		}
	}
	if(juego.estado == 'iniciando'){
		for (var i = 0; i < 10; i++) {
			enemigos.push({
				x:10 + (i*50),
				y:10,
				height:40,
				width:40,
				estado:'vivo',
				contador:0
			});
		}
		juego.estado = 'jugando'
	}
	
	for(var i in enemigos){
		var enemigo = enemigos[i];
		if(!enemigo) continue;
		if (enemigo && enemigo.estado == 'vivo') {
			enemigo.contador++;
			enemigo.x += Math.sin(enemigo.contador * Math.PI/90) *5;

			if(aleatorio(0,enemigos.length *10) == 4){
				soundInvaderShoot.pause();
				soundInvaderShoot.currenTime = 0;
				soundInvaderShoot.play();
				disparosEnemigos.push(agregarDisparosEnemigos(enemigo))		
				
			}
			
		}
		if(enemigo && enemigo.estado == 'hit'){
			enemigo.contador++;
			if(enemigo.contador >= 20){
				enemigo.estado = 'muerto';
				enemigo.contador = 0;
			}
		}
	}
	enemigos = enemigos.filter(function(enemigo){
		if(enemigo && enemigo.estado != 'muerto')return true;
		return false;
	})
}
function moverDisparos(){
	for (var i in disparos) {
		var disparo = disparos[i];
		disparo.y -= 2;
	}
	disparos = disparos.filter(function(disparo){
		return disparo.y > 0;
	});
}
function fire(){
	soundShoot.pause();
	soundShoot.currenTime = 0;
	soundShoot.play();
	disparos.push({
		x:nave.x + 20,
		y:nave.y + 10,
		width:10,
		height:30
	})
}
function dibujarDisparos(){
	for (var i in disparos) {
		var disparo = disparos[i];
		ctx.drawImage(imgDisparo,disparo.x,disparo.y,disparo.width,disparo.height);

	}
}
function dibujaTexto(){
	if(textoRespuesta.contador == -1) return;
	var alpha = textoRespuesta.contador/70.0;
	if(alpha>1){
		for(var i in enemigos){
			delete enemigos[i];
		}
	}
	ctx.save();
	ctx.globalAlpha = alpha;
	if(juego.estado == 'perdido'){
		ctx.fillStyle = 'red';
		ctx.font = 'Bold 40pt Arial';
		ctx.fillText(textoRespuesta.titulo,140,200)
		ctx.font = '14pt Arial';
		ctx.fillText(textoRespuesta.subtitulo,190,250)

	}
	if(juego.estado == 'victoria'){
		ctx.fillStyle = 'red';
		ctx.font = 'Bold 40pt Arial';
		ctx.fillText(textoRespuesta.titulo,140,200)
		ctx.font = '14pt Arial';
		ctx.fillText(textoRespuesta.subtitulo,190,250)

	}
}
function actualizarEstadoJuego(){
	if(juego.estado == 'jugando' && enemigos.length ==0){
		//alert("asd")
		juego.estado = 'victoria';
		textoRespuesta.titulo = 'Derrotaste a los enemigos';
		textoRespuesta.subtitulo = 'Presiona la tecla R para reiniciar';
		textoRespuesta.contador = 0;
	}
	if(textoRespuesta.contador>=0){
		textoRespuesta.contador++;
	}
	if((juego.estado == 'perdido' || juego.estado == 'victoria') && teclado[82]){
		juego.estado = 'iniciando';
		nave.estado = 'vivo';
		textoRespuesta.contador=-1;
	}
}
function hit(a, b){
	var hit = false;
	if(b.x  + b.width >= a.x && b.x < a.x + a.width){
		if (b.y + b.height>= a.y && b.y < a.y + a.height) {
			hit = true;
		}	
	}
	
	if ((b.x <= a.x)&& (b.x + b.width >= a.x + a.width)) {
		if(b.y <= a.y && b.y+b.height >= a.y + a.height){
			hit = true;
		}
	}

	if (a.x <= b.x && a.x + a.width >= b.x + b.width) {
		if(a.y <= b.y && a.y+a.height >= b.y + b.height){
			hit = true;
		}
	}

	return hit;
}
function verificarContacto(){
	for(var i in disparos){
		var disparo = disparos[i];
		for(j in enemigos){
			var enemigo = enemigos[j];
			if(hit(disparo,enemigo)){
				soundDeadInvader.pause();
				soundDeadInvader.currenTime = 0;
				soundDeadInvader.play();
				enemigo.estado = 'hit';
				enemigo.contador = 0;
				
			}

		}
	}
	if(nave.estado == 'hit' || nave.estado == 'muerto') return;
	for (var i in disparosEnemigos) {
		var disparo = disparosEnemigos[i];
		if(hit(disparo,nave)){
			soundDeadSpace.currenTime = 0;
			soundDeadSpace.play();
			nave.estado = 'hit';
			console.log("contacto")
		}
	}
}
function frameLoop(){
	actualizarEstadoJuego();
	moverNave();
	moverDisparos();
	moverDisparosEnemigos();
	dibujarFondo();
	verificarContacto();
	actualizaEnemigos();
	dibujarEnemigos();
	dibujarDiparosEnemigos();
	dibujarDisparos();
	dibujaTexto();
	dibujarNave();
}

window.addEventListener('load',init)
function init(){
	agregarEventosTeclado();
	loadMedia();	
}
