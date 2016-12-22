var $canv;
var $ctx;          
var lienzo;      // Es el espacio donde se crearan los objetos seleccionables
var controlZoom; // Este objeto contiene las funciones de zoom y movimiento del canvas // se lo inicializa en el archivo jquery.panzoom.js
function TifWIdget(tipo,id){
    Tiff.initialize({TOTAL_MEMORY: 16777216 * 50});
    var s = new openerp.init();
    url = s.session.url('/web_tiff_widget/BinaryTiff/tiff', {
                                        model: "rbs.documento.mercantil."+tipo,
                                        id: id,
                                        field: "filedata",
                                        t: (new Date().getTime()),});
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url);
    xhr.responseType = 'arraybuffer';

    var lenTiff = 0;
    var cursorTiff =  0;
    var tiffs = [];
    $canv = $('#imagenCanvas')
    $ctx = $canv[0].getContext("2d");
    lienzo = new CanvasState($canv[0]);
    xhr.onload = function (e) {
        console.log(xhr.response);
            PDFJS.getDocument(xhr.response).then(function(pdf) {
              // Using promise to fetch the page
              var canvas = document.createElement('canvas');
              var context = canvas.getContext('2d');
              for (var i = 1; i < pdf.numPages; i++) {
                pdf.getPage(i).then(function(page) {
                    console.log(page);
                    var scale = 10;
                    var viewport = page.getViewport(scale);

                    //
                    // Prepare canvas using PDF page dimensions
                    //
                    
                    
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;

                    //
                    // Render PDF page into canvas context
                    //
                    var renderContext = {
                      canvasContext: context,
                      viewport: viewport
                    };
                    page.render(renderContext);
                    tiffs[i] = new tifClass(context.getImageData(0, 0, canvas.width, canvas.height),i);
                    if(i == 1){
                        on_change();
                    }
                  });
              }
              
            });
            /*var tiff;    
            var buffer = xhr.response;
            //console.log((buffer))
            tiff = new Tiff({buffer: buffer});
            lenTiff =  tiff.countDirectory();
            for (var i = 0, len = tiff.countDirectory(); i < len; ++i) {
                tiffs.push(new tifClass(tiff,i));
            }
            on_change();*/
                
    }


    xhr.send();
    
    function tifClass(TIfforiginal, index){ 
        this.saved= true
        this.TIfforiginal = TIfforiginal;
        this.canvasOriginal
        this.index = index;
        this.versiones = [];
        this.verActual = 0;
        this.texture;
        this.canv = null;

        this.versiones.push(TIfforiginal);
        this.getTif = function (){ 
            if(this.versiones.length == 0){
                this.TIfforiginal.setDirectory(index);
                this.canvasOriginal = this.TIfforiginal.toCanvas();
                this.setTif(this.canvasOriginal.toDataURL("image/png"))
                return this.getTif();
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
        
        this.isSaved = function(){
            return this.saved;
        }
        this.save = function(){
            this.saved = true;
        }
        var accion
    }
    on_change = function(){
        //console.log($canv)
        // var image = new Image();
        // image.onload = function() {
        //     var width = image.naturalWidth; // this will be 300
        //     var height = image.naturalHeight; // this will be 400
        //     $canv.attr('width',width);
        //     $canv.attr('height',height);
        //     $ctx.drawImage(image, 0, 0, width, height);
        //     //$canv.css("width", "75%");
        // };
        lienzo.setFondo(tiffs[cursorTiff].getTif());

        asd = new ShapeText(10,40,"bold 24px verdana",null,'rgba(12, 25, 212, .5)')
        lienzo.addShape(asd); 
        lienzo.addShape(new Shape(40,40,50,50));
        //image.src = tiffs[cursorTiff].getTif();
    }
     

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
    $('.btnDisenoPrueba').click(function(){
        app.filters.invert()
    })
    var contraste = 0 ;
    $('.contraste').on("input change", function() {
        valor = this.value - contraste;
        //console.log("contraste :"+ valor)
        if(valor!=0){
            app.filters.contrast(valor)    
        }
        
        contraste = this.value;
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


    
