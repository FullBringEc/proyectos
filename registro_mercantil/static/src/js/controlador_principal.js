var $canv;
var $ctx;          
var lienzo;      // Es el espacio donde se crearan los objetos seleccionables
var controlZoom; // Este objeto contiene las funciones de zoom y movimiento del canvas // se lo inicializa en el archivo jquery.panzoom.js
var contenedor_id; // Este objeto contiene las funciones de zoom y movimiento del canvas // se lo inicializa en el archivo jquery.panzoom.js
setTextColor=function(color){
    lienzo.setFuncionActual("Texto");
    if (lienzo.selection.type=='Texto'){  
    // if (lienzo.funcionActual=='Texto'){
        
        lienzo.selection.fill='#'+color
        lienzo.valid=false
    }
}
function TifWIdget(tipo,id){
    Tiff.initialize({TOTAL_MEMORY: 16777216 * 5});
    var s = new openerp.init();
    // url = s.session.url('/registro_mercantil/BinaryTiff/tiff', {
    //                                     model: "rbs.documento."+tipo,
    //                                     id: id,
    //                                     field: "filedata",
    //                                     t: (new Date().getTime()),});

    // console.log(url)
    var lenTiff = 0;
    var cursorTiff =  0;
    var tiffs = [];
    $canv = $('#imagenCanvas')
    $ctx = $canv[0].getContext("2d");
    lienzo = new CanvasState($('#figurasCanvas')[0],$('#borradorCanvas')[0]);

    new openerp.web.Model('rbs.documento.'+tipo).call('read',[[id],['compania_nombres','fecha_inscripcion', 'contenedor_id']])
                .then(function(result){
                    $('#tipo').html(tipo)
                    $('#propietario').html(result[0].compania_nombres)
                    $('#fecha').html(result[0].fecha_inscripcion)
                    contenedor_id = result[0].contenedor_id[0]
                    new openerp.web.Model('rbs.imagenes').query(['imagen']).filter([['contenedor_id','=',contenedor_id]]).context(null).all()
                    .then(function(result){                     
                        lenTiff =  result.length;
                        for (var i=0; i<result.length; i++){
                            // tiffs.push(new tifClass(null,i,result[i].id));
                            // console.log(result[i].imagen);
                            tiffs.push(new tifClass(result[i].imagen,i,result[i].id));
                        }
                        on_change();
                    })
                })

    function tifClass(imagensrc, index, id){
        
        
        if(imagensrc == null){


            var canvasAux = document.createElement("canvas");
            canvasAux.width = 1000;
            canvasAux.height = 1400;
            var ctx = canvasAux.getContext("2d");
            var imgData=ctx.createImageData(1000,1400);
            data = imgData.data;
            for (var i = 0; i < data.length; i += 4) {
              data[i]     = 255;     // red
              data[i + 1] = 255; // green
              data[i + 2] = 255; // blue
              data[i + 3] = 255; // blue
            }
            ctx.putImageData(imgData, 0, 0);

            var url = canvasAux.toDataURL();
            // console.log(url);
            url = url.substr(-url.length+22)

            
            // console.log(url);
            this.imagensrc = url;
        }else{
            this.imagensrc = imagensrc;
        }
        this.saved= true
        // this.imagensrc = imagensrc;
        this.canvasOriginal
        this.width;
        this.height;
        this.index = index;
        this.versiones = [];
        this.verActual = -1;
        this.texture;
        this.canv = null;
        this.shapes = [];
        this.idBD = id;

        this.getShapes = function(){
            return this.shapes;
        }

        this.setShapes = function(s){
            this.shapes = s;
        }

        this.setOriginal = function(){
            this.versiones = [];
            this.verActual = -1;       
            this.shapes = [];
            return this.imagensrc;
        }

        this.getTif = function (){ 
            if(this.versiones.length == 0){
                return this.imagensrc;
                
            }else{

                return this.versiones[this.verActual]
            }
        }
        this.setTifUndo = function (){ 
            if(this.verActual<=0){
                alert("no ha habido ningun cambio")
            }else{
                this.verActual--;   
                this.saved = false 

            }
        }
        this.setTifRepeat = function (){ 
            if(this.verActual==this.versiones.length-1){
                alert("no ha habido ningun cambio")
            }else{
                this.verActual++; 
                this.saved = false   
            }
        }
        this.setTif = function (src){ 
            //this.canv = canvas
            if(this.verActual == -1){
                this.versiones.push(src)
                this.verActual++;
            }else{
                l = this.versiones.length
                this.versiones.splice(this.verActual+1,l-(this.verActual+1));
                this.versiones.push(src)
                this.verActual++;
                this.saved = false
            }
            
        }
        this.descargarImagen = function(){
            self=this
            var canvas = document.createElement('canvas');
            context = canvas.getContext( '2d' )

            var image = new Image();
            image.onload = function() {
            var width = image.naturalWidth;   // this will be 300
            var height = image.naturalHeight; // this will be 400
            canvas.width = width;
            canvas.height = height;
            console.log(width+" "+height)

            context.drawImage(image, 0, 0, width, height);
            for (var i = self.shapes.length - 1; i >= 0; i--) {
                if(self.shapes[i].type!='Texto'){                   
                    self.shapes[i].draw(context);
                }                
            }
            for (var i = self.shapes.length - 1; i >= 0; i--) {
                if(self.shapes[i].type=='Texto'){                   
                    self.shapes[i].draw(context);
                }                
            }

            var link = window.document.createElement( 'a' ),
                url = canvas.toDataURL(),
                filename = 'screenshot.png';
                console.log(url)
         
            link.setAttribute( 'href', url );
            link.setAttribute( 'download', filename );
            link.style.visibility = 'hidden';
            window.document.body.appendChild( link );
            link.click();
            window.document.body.removeChild( link );
            }
            //console.log(this.getTif())
            // image.src = "data:image/png;base64,"+this.getTif();
            image.src = $('#imagenCanvas')[0].toDataURL();
            
        }


        this.guardarImagen = function(posicion){
            var mensaje = confirm("¿Esta seguro que desea guardar?");
            //Detectamos si el usuario acepto el mensaje
            if (mensaje) {
                self=this
                var canvas = document.createElement('canvas');
                context = canvas.getContext( '2d' )

                var image = new Image();
                image.onload = function() {
                    var width = image.naturalWidth;   // this will be 300
                    var height = image.naturalHeight; // this will be 400
                    canvas.width = width;
                    canvas.height = height;

                    context.drawImage(image, 0, 0, width, height);
                    for (var i = self.shapes.length - 1; i >= 0; i--) {
                        if(self.shapes[i].type!='Texto'){                   
                            self.shapes[i].draw(context);
                        }                
                    }
                    for (var i = self.shapes.length - 1; i >= 0; i--) {
                        if(self.shapes[i].type=='Texto'){                   
                            self.shapes[i].draw(context);
                        }                
                    }
                    var cadena=canvas.toDataURL();
                    c = cadena.substr(-cadena.length+22)
                    new openerp.web.Model('rbs.imagenes').call('actualizarImagen',[[self.idBD],c,posicion])
                        .then(function(result){
                            console.log(result)
                            if(result){
                                self.setTif(c)
                                self.save()
                            }
                        })
                } 

                // image.src = "data:image/png;base64,"+this.getTif(); 
                src = $('#imagenCanvas')[0].toDataURL();
                image.src = src

            }
        }

        

        this.isSaved = function(){
            return this.saved;
        }
        this.save = function(){
            this.saved = true;
            // this.setShapes(lienzo.shapes)
        }
        this.unsave = function(){
            this.saved = false;
            // this.setShapes(lienzo.shapes)
        }
        var accion
    }

    on_change = function(){
        //console.log($canv)
        var image = new Image();
        image.onload = function() {
            var width = image.naturalWidth;   // this will be 300
            var height = image.naturalHeight; // this will be 400



            $(".pagina_actual").val(cursorTiff+1)      
            $(".pagina_final").val(lenTiff)
            lienzo.shapes=tiffs[cursorTiff].getShapes()
            $canv[0].width = width;
            $canv[0].height = height;
            $ctx.drawImage(image, 0, 0, width, height);
            lienzo.valid=false
            lienzo.setSize(width,height);
        };
        image.src = "data:image/png;base64,"+tiffs[cursorTiff].getTif();
        
    }

    $(".btnFuentesLetras").change(function(){ 
        lienzo.setFuncionActual("Texto");    
       if (lienzo.selection.type=='Texto'){       
            lienzo.selection.font_family= $(".btnFuentesLetras").val()
            lienzo.valid=false
            tiffs[cursorTiff].unsave();

        }   
    })



    $(".btnTamTexto").change(function(){       
        lienzo.setFuncionActual("Texto");
        if (lienzo.selection.type=='Texto'){             
            lienzo.selection.font_size= $(".btnTamTexto").val()
            lienzo.valid=false
            tiffs[cursorTiff].unsave();
        }   
    })
    $(".btnRotation").click(function(){       
        lienzo.setFuncionActual("Texto");
        if (lienzo.selection.type=='Texto'){             

            lienzo.selection.rotar(45);
            console.log(lienzo.selection.giro); 
            lienzo.valid=false
            tiffs[cursorTiff].unsave();
        }   
    })

    $(".eliminarImagen").click(function(){
            var mensaje = confirm("¿Esta seguro que desea eliminar?");
            if (mensaje) {
                new openerp.web.Model('rbs.imagenes').call('eliminarImagen',[[tiffs[cursorTiff].idBD]])
                .then(function(result){
                    tiffs.splice(cursorTiff,1)     
                    if (cursorTiff==lenTiff){      
                        cursorTiff=cursorTiff-1
                    }
                    lenTiff=lenTiff-1
                    on_change();
                })
            }
    })
    /*
        Cambiar de pagina mediante el teclado
    */
    $(document).keydown(function(e){
        // console.log(e)
        if(e.shiftKey == true){
            if(e.which ==37){
                $('.button-back').click()
            }
            if(e.which ==39){
                $('.button-next').click()
            }
        }
    })
    //funcion para que solo acepte letras


    $(".guardarImagen").click(function(){        
          tiffs[cursorTiff].guardarImagen(cursorTiff);
    })
    $(".nuevaHoja").click(function(){   
        // tiffs.splice(cursorTiff,new tifClass(null,i,null));   
        new openerp.web.Model('rbs.imagenes').call('insertarImagen',[[],contenedor_id,cursorTiff])
        // new openerp.web.Model('rbs.imagenes').call('unlink',[[tiffs[cursorTiff].idBD]])
                .then(function(result){
                    if(typeof result){
                        tiffs.splice(cursorTiff+1,0,new tifClass(null,cursorTiff+1,result));  
                        lenTiff++;
                        $('.button-next').click() 
                    }
                })  
          // tiffs[cursorTiff].guardarImagen(cursorTiff);
    })

    $(".btnAddText").click(function(){        
        lienzo.addShape(new ShapeText(200,200,"Escriba","bold", 54,"verdana",null,'rgba(12, 240, 22, .5)'));  
        tiffs[cursorTiff].unsave();    
    })

    $(".descargarimg").click(function(){
        tiffs[cursorTiff].descargarImagen();

    })

    $(".btnBorrar").click(function(){
        lienzo.setFuncionActual("BorradorXseleccion");
        
        tiffs[cursorTiff].unsave();
    })

    $(".btnBorrarDeslizar").click(function(){
        lienzo.setFuncionActual("BorradorXarrastre");
        tiffs[cursorTiff].unsave();
    })
    
    $(".pagina_actual").keypress(function(e){
    if(e.keyCode == 13){
        nueva_pagina=$(".pagina_actual").val()-1
        if (nueva_pagina<lenTiff && nueva_pagina>=0){
            if(tiffs[cursorTiff].isSaved()){
                cursorTiff=nueva_pagina;
                on_change();
            }else{
                alert("Para cambiar de imagen primero almacene la actual")
            }
        }
        else {
            $(".pagina_actual").val(cursorTiff+1) 
        }
    }}    
    );

    // Eventos 
    $('.button-back').click(function(){
        if(cursorTiff!=0){
            if(tiffs[cursorTiff].isSaved()){
                cursorTiff--;
                on_change();

            }else{
                alert("Para cambiar de imagen primero almacene la actual")
            }
        }
    });
    $('.button-next').click(function(){
        if(cursorTiff!=lenTiff-1){
            if(tiffs[cursorTiff].isSaved()){
                cursorTiff++;
                on_change()

            }else{
                alert("Para cambiar de imagen primero almacene la actual")
            }
        }
    })

    $('.button-original').click(function(){
        tiffs[cursorTiff].setOriginal();
        minContraste = 0
        maxContraste = 100

        inpRanContraste = $('.contraste-range')[0]
        if(inpRanContraste.max != ""){
            maxContraste = inpRanContraste.max
        }
        if(inpRanContraste.min != ""){
            minContraste = inpRanContraste.min
        }

        minBrillo = 0
        maxBrillo = 100

        inpRanBrillo = $('.brightness-range')[0]
        if(inpRanBrillo.max != ""){
            minBrillo = inpRanBrillo.max
        }
        if(inpRanBrillo.min != ""){
            maxBrillo = inpRanBrillo.min
        }

        inpRanContraste.value   = (maxContraste+minContraste)/2
        inpRanBrillo.value      = (minBrillo+maxBrillo)/2

        on_change()
        tiffs[cursorTiff].unsave();
    })

    $('.btnDisenoPrueba').click(function(){
        app.filters.invert()
        tiffs[cursorTiff].unsave();
    })
    var contraste = 0 ;
    $('.contraste-range').on("input change", function() {
        valor = this.value - contraste;
        //console.log("contraste :"+ valor)
        if(valor!=0){
            app.filters.contrast(valor)    
        }
        
        contraste = this.value;
        tiffs[cursorTiff].unsave();
    });
    var brightness = 0 ;
    $('.brightness-range').on("input change", function() {
        valor = this.value - brightness;
        //console.log("contraste :"+ valor)
        if(valor!=0){
            app.filters.brightness(valor)    
        }
        
        brightness = this.value;
        tiffs[cursorTiff].unsave();
    });

    $('.contraste').mousedown(function() {
     //console.log('inicio')
    });

    $('.btnDisenoPrueba2').click(function(){

    })

    $('.button-undo').click(function(){
        tiffs[cursorTiff].setTifUndo();
        onchange()
    })
    $('.sepia').click(function(){
        app.filters.sepia();
        tiffs[cursorTiff].unsave();
    })

    $('.bw').click(function(){
        app.filters.bw();
        tiffs[cursorTiff].unsave();
    })

    $('.invertirColor').click(function(){
        app.filters.invert();
        tiffs[cursorTiff].unsave();
    })

    $('.button-repeat').click(function(){
        tiffs[cursorTiff].setTifRepeat();
        onchange()
    })
    $('.button-save').click(function(){
        tiffs[cursorTiff].save();
    })
    $('.multitiff').click(function(){
        instance.web.blockUI();
        var c = instance.webclient.crashmanager;
        //alert(tiffs[cursorTiff])
        self.session.get_file({
            url: '/web/binary/multitiff',
            data: {
                data: JSON.stringify({
                    model: tiffs[cursorTiff].getTif().toDataURL()
                })},
            complete: instance.web.unblockUI,
            error: c.rpc_error.bind(c)
        });


    })
   

}


    
