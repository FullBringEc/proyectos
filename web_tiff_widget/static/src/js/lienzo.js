// By Simon Sarris
// www.simonsarris.com
// sarris@acm.org
//
// Last update December 2011
//
// Free to use and distribute at will
// So long as you are nice to people, etc

// Constructor for Shape objects to hold data for all drawn objects.
// For now they will just be defined as rectangles.
function Shape(x, y, w, h, fill) {
  // This is a very simple and unsafe constructor. All we're doing is checking if the values exist.
  // "x || 0" just means "if there is a value for x, use that. Otherwise use 0."
  // But we aren't checking anything else! We could put "Lalala" for the value of x 
  this.x = x || 0;
  this.y = y || 0;
  this.w = w || 1;
  this.h = h || 1;
  this.fill = fill || '#AAAAAA';
  this.type = 'rectangulo'
}

// Draws this shape to a given context
Shape.prototype.draw = function(ctx) {
  ctx.fillStyle = this.fill;
  ctx.fillRect(this.x, this.y, this.w, this.h);
}

// Determine if a point is inside the shape's bounds
Shape.prototype.contains = function(mx, my) {
  // All we have to do is make sure the Mouse X,Y fall in the area between
  // the shape's X and (X + Width) and its Y and (Y + Height)
  return  (this.x <= mx) && (this.x + this.w >= mx) &&
          (this.y <= my) && (this.y + this.h >= my);
}
var ctxAuxiliar = document.createElement("canvas").getContext("2d");
function ShapeText (x, y,font,text,fill) {
  this.font = font || "bold 24px verdana";
  this.text = text || "escribir...";

  ctxAuxiliar.font = font || "bold 24px verdana";
  d = ctxAuxiliar.measureText(text);
  w = d.width;
  h = font.split(" ")[1].substr(0,2);
  
  this.x = x || 0;
  this.y = y || 0;
  this.w = w || 1;
  this.h = h || 1;
  this.fill = fill || '#AAAAAA';
  this.type = 'texto'

}
ShapeText.prototype = new Shape;
ShapeText.prototype.draw = function(ctx) {
  ctx.fillStyle = this.fill;
  ctx.font = this.font;
  ctx.textBaseline = "top"
  d = ctxAuxiliar.measureText(this.text);
  this.w = d.width;
  this.h = parseInt(this.font.split(" ")[1].substr(0,2));
  ctx.fillText(this.text,this.x, this.y);
}
function ShapeBorrador (x, y, w, h, fill){
  this.x = x || 0;
  this.y = y || 0;
  this.w = w || 1;
  this.h = h || 1;
  this.fill = fill || '#FFFFFF';
  this.type = 'borrador'
}
ShapeBorrador.prototype = new Shape;


function CanvasState(canvas) {
  // **** First some setup! ****
  
  this.canvas = canvas;
  this.width = canvas.naturalWidth;
  this.height = canvas.naturalHeight;
  this.ctx = canvas.getContext('2d');
  // Esto complica un poco las cosas pero arregla los problemas de coordenadas
  // del ratón cuando hay un borde o relleno. Vea getMouse para más detalles
  var stylePaddingLeft, stylePaddingTop, styleBorderLeft, styleBorderTop;
  if (document.defaultView && document.defaultView.getComputedStyle) {
    this.stylePaddingLeft = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingLeft'], 10)      || 0;
    this.stylePaddingTop  = parseInt(document.defaultView.getComputedStyle(canvas, null)['paddingTop'], 10)       || 0;
    this.styleBorderLeft  = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderLeftWidth'], 10)  || 0;
    this.styleBorderTop   = parseInt(document.defaultView.getComputedStyle(canvas, null)['borderTopWidth'], 10)   || 0;
  }
  //Algunas páginas tienen barras de posición fija (como la barra de stumbleupon) 
  //en la parte superior o izquierda de la página
  //Arruinarán las coordenadas del ratón y esto arreglará
  var html = document.body.parentNode;
  this.htmlTop = html.offsetTop;
  this.htmlLeft = html.offsetLeft;

  // **** Keep track of state! ****
  
  this.valid = false;     //Cuando se establece en false, el lienzo volverá a dibujar todo
  this.fondo = false; //Imagen a colocar en el fondo
  this.shapes = [];       //La colección de cosas a dibujar
  this.dragging = false;  //Seguimiento de cuando estamos arrastrando
  //El objeto seleccionado actual. En el futuro podríamos convertir esto en una matriz para la selección múltiple
  this.selection = null;
  this.borrador = null;
  this.funcionborrar = true;
  this.dragoffx = 0;      //Ver eventos de mousedown y mousemove para explicación
  this.dragoffy = 0;
  
  // **** Then events! ****
  
  // This is an example of a closure!
  // Right here "this" means the CanvasState. But we are making events on the Canvas itself,
  // and when the events are fired on the canvas the variable "this" is going to mean the canvas!
  // Since we still want to use this particular CanvasState in the events we have to save a reference to it.
  // This is our reference!
  /*Traduccion*/
  // **** ¡Entonces eventos! ****
  // Este es un ejemplo de un cierre!
  // Aqui "this" significa el CanvasState. Pero estamos haciendo eventos en la propia lona,
  // y cuando los eventos son disparados en el lienzo la variable "this" va a significar el lienzo!
  // Debido a que todavía queremos usar este CanvasState en particular en los eventos tenemos que guardar una referencia a él.
  // Esta es nuestra referencia!
  var myState = this;
  
  //corrige un problema cuando un doble clic hace que el texto se seleccione en el lienzo
  canvas.addEventListener('selectstart', function(e) { e.preventDefault(); return false; }, false);
  // Arriba, abajo y mover son para arrastrar 
window.onkeydown = function(e) { 
    return !(e.keyCode == 32);
}; 
  document.addEventListener('keyup',function(e){
    e.stopPropagation();
    e.preventDefault();
    if(myState.selection != null){
      if(myState.selection.type =='texto'){
        if(soloLetras(e)){
          myState.selection.text = myState.selection.text+String.fromCharCode(e.which).toString();  
          myState.valid = false;  
        }
        if(e.keyCode == '8'){

          var t = myState.selection.text
          myState.selection.text =t.substring(0,t.length-2); 
          myState.valid = false;
        }
        
      }
    }
    //funcion para que solo acepte letras
    function soloLetras(e) {
      key = e.keyCode || e.which;
      tecla = String.fromCharCode(key).toString();
      letras = " áéíóúabcdefghijklmnñopqrstuvwxyzÁÉÍÓÚABCDEFGHIJKLMNÑOPQRSTUVWXYZ123456789";//Se define todo el abecedario que se quiere que se muestre.
      especiales = [8, 37, 39, 46, 6]; //Es la validación del KeyCodes, que teclas recibe el campo de texto.

      tecla_especial = false
      for(var i in especiales) {
          if(key == especiales[i]) {
              tecla_especial = true;
              break;
          }
      }

      if(letras.indexOf(tecla) == -1 && !tecla_especial){
        //alert('Tecla no aceptada');
          return false;
        }
        return true;
  }

  },false);
  document.addEventListener('mousedown', function(e) {
    if (event.button!=0)return
    myState.selection = null;
      myState.valid = false;
    }, true);
  canvas.addEventListener('mousedown', function(e) {
    if (event.button!=0)return
    var mouse = myState.getMouse(e);
    var mx = mouse.x;
    var my = mouse.y;
    var shapes = myState.shapes;
    var l = shapes.length;
    for (var i = l-1; i >= 0; i--) {
      if (shapes[i].contains(mx, my)) {
        if(shapes[i].type != 'borrador'){
          var mySel = shapes[i];
          // Mantener un registro del lugar en el que hicimos clic
          // Para que podamos moverlo sin problemas (ver mousemove)
          myState.dragoffx = mx - mySel.x;
          myState.dragoffy = my - mySel.y;
          myState.dragging = true;
          myState.selection = mySel;
          myState.valid = false;
          //controlZoom.bloquearMovimiento(true);
          return;
        }
        
      }
    }
    // Si no han retornado significa que no hemos podido seleccionar nada.
    // Si hubo un objeto seleccionado, lo deseleccionamos
    //controlZoom.bloquearMovimiento(false);
    if (myState.selection) {
      myState.selection = null;
      myState.valid = false; // Necesidad de borrar el borde de selección antiguo
    }

    if (myState.borrador==null && myState.funcionborrar) {
      //controlZoom.bloquearMovimiento(true);
      myState.borrador = {};
      myState.borrador.x = mx;
      myState.borrador.y = my;
      myState.valid = false; // Necesidad de borrar el borde de selección antiguo
    }


  }, true);
  canvas.addEventListener('mousemove', function(e) {
    
    if (myState.dragging){
      var mouse = myState.getMouse(e);
      //No queremos arrastrar el objeto por su esquina superior izquierda, queremos arrastrarlo
      // de donde hicimos clic. Por eso ahorramos el offset y lo usamos aquí
      myState.selection.x = mouse.x - myState.dragoffx;
      myState.selection.y = mouse.y - myState.dragoffy;   
      myState.valid = false; // Algo está arrastrando así que debemos redibujar
    }

    if (myState.borrador != null && myState.funcionborrar){
      var mouse = myState.getMouse(e);
      //console.log(myState.borrador.x + ' : ' + myState.getMouse(e).x)
      myState.borrador.w = mouse.x - myState.borrador.x;
      myState.borrador.h = mouse.y - myState.borrador.y;
      //console.log(myState.borrador.w + ' : ' + myState.borrador.h)
      myState.valid = false;
    }



  }, true);
  canvas.addEventListener('mouseup', function(e) {
    if (event.button!=0)return
    //console.log("mouse arriba")
    myState.dragging = false;
    if(myState.borrador!=null){
      //controlZoom.bloquearMovimiento(false);
      var x = myState.borrador.x;
      var y = myState.borrador.y;
      var w = myState.borrador.w;
      var h = myState.borrador.h;
      //console.log(x+' - '+y+' - '+w+' - '+h);
      if(w<0){
        myState.borrador.x = x+w; myState.borrador.w = w*-1;
      }
      if(h<0){
        myState.borrador.y = y+h; myState.borrador.h = h*-1;
      }
      myState.addShape(new ShapeBorrador(myState.borrador.x,myState.borrador.y,myState.borrador.w,myState.borrador.h))
      myState.borrador = null;
    }

  }, true);
  // doble clic para crear nuevas formas
  canvas.addEventListener('dblclick', function(e) {
    var mouse = myState.getMouse(e);
    //console.log(mouse)
    myState.addShape(new Shape(mouse.x - 10, mouse.y - 10, 20, 20, 'rgba(0,255,0,.6)'));
  }, true);
  
  // **** Opciones! ****
  
  this.selectionColor = '#CC0000';
  this.selectionWidth = 2;  
  this.interval = 50;
  setInterval(function() { myState.draw(); }, myState.interval);
}

CanvasState.prototype.addShape = function(shape) {
  this.shapes.push(shape);
  this.valid = false;
}

CanvasState.prototype.clear = function() {
  this.ctx.clearRect(0, 0, this.width, this.height);
}

//Mientras el draw es llamado tan a menudo como la variable INTERVAL exige,
//Sólo hace algo si el lienzo se invalida por nuestro código
CanvasState.prototype.draw = function() {
  // Si nuestro estado no es válido, vuelve a dibujar y validar!
  if (!this.valid) {
    var ctx = this.ctx;
    var shapes = this.shapes;
    this.clear();
    
    // ** Añadir cosas que desea dibujar en el fondo todo el tiempo aquí
    if(this.fondo){
      this.canvas.setAttribute("width", this.width);
      this.canvas.setAttribute("height", this.height);
      ctx.drawImage(this.fondo, 0, 0, this.width, this.height);
    }
    
    //Dibuja todas las formas
    var l = shapes.length;
    for (var i = 0; i < l; i++) {
      var shape = shapes[i];
      // We can skip the drawing of elements that have moved off the screen:
      if (shape.x > this.width || shape.y > this.height ||
          shape.x + shape.w < 0 || shape.y + shape.h < 0) continue;
      shapes[i].draw(ctx);
    }
    
    // dibujar la selección
    // en este momento esto es sólo un golpe a lo largo del borde de la forma seleccionada
    if (this.selection != null) {
      ctx.strokeStyle = this.selectionColor;
      ctx.lineWidth = this.selectionWidth;
      var mySel = this.selection;
      ctx.strokeRect(mySel.x,mySel.y,mySel.w,mySel.h);
    }

    if (this.borrador != null) {
      ctx.strokeStyle = this.selectionColor;
      ctx.lineWidth = this.selectionWidth;
      var mySel = this.borrador;
      ctx.strokeRect(mySel.x,mySel.y,mySel.w,mySel.h);
    }
    
    // ** Añadir cosas que desea dibujar en la parte superior todo el tiempo aquí **
    
    this.valid = true;
  }
}
CanvasState.prototype.setFondo = function(srcFondo){
  s = this; //s representa el objeto CanvasState 
  var fondo = new Image();
    fondo.onload = function() {
      
      s.width = fondo.naturalWidth; 
      s.height = fondo.naturalHeight;
      //s.valid = false;
      s.fondo = fondo
      s.valid = false;
    }
    fondo.src = srcFondo;
}
CanvasState.prototype.setShapes = function(shapes, srcFondo) {
  // Cambiar los objetos que se muestran
  
  this.shapes = shapes;
  if(srcFondo){
    this.setFondo(srcFondo)
  }else{
    this.fondo = false;
    this.valid = false;
  }
  


  
  
  
}
CanvasState.prototype.getShapes = function() {
  // Cambiar los objetos que se muestran
  return this.shapes;
}


// Crea un objeto con 'x' y 'y' definidas, establecidas en la posición del ratón en relación con el lienzo del estado
// Si quieres ser super-correcto esto puede ser complicado, tenemos que preocuparnos por el relleno y las fronteras
CanvasState.prototype.getMouse = function(e) {
  var element = this.canvas, offsetX = 0, offsetY = 0, mx, my;
  
  // Calcular el desplazamiento total
  if (element.offsetParent !== undefined) {
    do {
      offsetX += element.offsetLeft; //distancia en x desde el padre hasta el elemento, por razones como bordes
      offsetY += element.offsetTop; //distancia en y desde el padre hasta el elemento
    } while ((element = element.offsetParent));
    // este while hace que recorra todos los elementos padres uno a uno y 
    //cuando se llegue al mayor la condicion se vuelde indefinida y sale del bucle,
    //todo esto para sumar las distacias de todos los bordes
  }

  // Añadir relleno y anchos de estilo de borde para compensar
  // También agregue los desplazamientos <html> en caso de que haya una posición: barra fija
  offsetX += this.stylePaddingLeft + this.styleBorderLeft + this.htmlLeft;
  offsetY += this.stylePaddingTop + this.styleBorderTop  + this.htmlTop;

  mx = e.clientX;
  my = e.clientY;




   /*XY = myState.getMouse(e);
ancho = myState.width;
alto =  myState.height;
var bbox = canvas.getBoundingClientRect();
mouse.x = (ancho*XY.x-bbox.left)/bbox.width;
mouse.y = (alto*XY.y-bbox.left)/ bbox.height;*/



  var rect = this.canvas.getBoundingClientRect();
  //console.log((offsetX) +'-'+(offsetY))  ;

  mx = this.width * (mx - rect.left)/(rect.width);
  my = this.height * (my - rect.top)/(rect.height) ;
  // Devolvemos un objeto javascript simple (un hash) con 'x' y 'y' definidos
  
  // Devolvemos un objeto javascript simple (un hash) con 'x' y 'y' definidos
  return {x: mx, y: my};
}

//  Si no quieres usar <body onLoad = 'init ()'>
// Puede descomentar esta referencia init () y colocar la referencia del script dentro de la etiqueta body
// init();
// s = false;
// function init() {
//   s = new CanvasState(document.getElementById('canvas1'));
  
//   asd = new ShapeText(10,40,"bold 24px verdana",null,'rgba(12, 25, 212, .5)')
//   s.addShape(asd); 
  
//   s.addShape(new Shape(40,40,50,50)); // The default is gray
//   s.addShape(new Shape(60,140,40,60, 'lightskyblue'));
//   // Lets make some partially transparent
//   s.addShape(new Shape(80,150,60,30, 'rgba(127, 255, 212, .5)'));
//   s.addShape(new Shape(125,80,30,80, 'rgba(245, 222, 179, .7)'));
//   s.setFondo('https://ratticatte.files.wordpress.com/2008/05/imagen-original3.jpg');
// }

// Now go make something amazing!
