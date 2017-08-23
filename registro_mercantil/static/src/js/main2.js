function TifWIdget(tipo,id){
    Tiff.initialize({TOTAL_MEMORY: 16777216 * 50});
    var t0 = performance.now();
    var s = new openerp.init();
    url = s.session.url('/registro_mercantil/BinaryTiff/tiff', {
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
    var $canv;
    var canv;
    var texture;
    xhr.onload = function (e) {
            var tiff;    
            var buffer = xhr.response;
            console.log((buffer))
            tiff = new Tiff({buffer: buffer});
            lenTiff =  tiff.countDirectory();
            var t1 = performance.now();
            console.log("Call to doSomething took " + (t1 - t0) + " milliseconds.")
            for (var i = 0, len = tiff.countDirectory(); i < len; ++i) {
                tiffs.push(new tifClass(tiff,i));
            }
            onchange();
                
    }


    xhr.send();
    function tifClass(origen, index){ 
        this.saved= true
        this.canvasEdit;
        this.origen = origen; 
        this.index = index;
        this.versiones = [];
        this.verActual = -1;
        this.texture;
        this.canv = null;
        this.getTexture = function(){
            if(this.versiones[this.verActual][1] == null)
            {
                this.versiones[this.verActual][1] = this.getCanvasEdit().texture(this.getTif());
            }
            return this.versiones[this.verActual][1]
        }
        //this.setTexture = function(texture){
            //this.texture = texture;
        //    this.versiones[this.verActual][1] = texture;
        //}
        this.getTif = function (){ 
            if(this.versiones.length == 0){
                this.origen.setDirectory(index);
                //this.canv = this.origen.toCanvas();
                this.setTif(this.origen.toCanvas())
                return this.getTif();
            }else{
                return this.versiones[this.verActual][0]
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
        this.setTif = function (canvas,texture,canvasEdit){ 
            //this.canv = canvas
            if(this.verActual == -1){
                this.versiones.push([canvas,texture,canvasEdit])
                this.verActual++;
            }else{
                l = this.versiones.length
                this.versiones.splice(this.verActual+1,l-(this.verActual+1));
                this.versiones.push([canvas,texture,canvasEdit])
                this.verActual++;
                this.saved = false
            }
            
        }
        this.getCanvasEdit = function(){
            if(this.versiones[this.verActual][2] == null)
            {
                this.versiones[this.verActual][2] = fx.canvas();
            }
            return this.versiones[this.verActual][2]

        }
        this.isSaved = function(){
            return this.saved;
        }
        this.save = function(){
            this.saved = true;
        }
    }
    onclickAdelante = function(){
        if(cursorTiff!=lenTiff-1){
            if(tiffs[cursorTiff].isSaved()){
                cursorTiff++;
                onchange()
            }else{
                alert("Para cambiar de imagen primero almacene la actual")
            }
        }
    }
    onclickAtras = function(){
        if(cursorTiff!=0){
            if(tiffs[cursorTiff].isSaved()){
                cursorTiff--;onchange();
            }else{
                alert("Para cambiar de imagen primero almacene la actual")
            }
        }
    }
    onclickUndo = function(){
        tiffs[cursorTiff].setTifUndo();
        onchange()
    }
    onclickRepeat = function(){
        tiffs[cursorTiff].setTifRepeat();
        onchange()
    }
    onclickSave = function(){
        tiffs[cursorTiff].save();
        //onchange()
    }

    onclickDiseno = function(){
        canvasEditable.draw(texture).ink(0.50).update();
        canv = canvasEditable;
        setAtributos()
        //tiffs[cursorTiff].setTif(canvasEditable)
        texture = canvasEditable.texture(canvasEditable);
        tiffs[cursorTiff].setTif(canvasEditable,texture,canvasEditable)
        //tiffs[cursorTiff].setTexture(texture)
        
    }
    onchange = function(){
        canv = null
        texture = null
        canvasEditable = null
        //canvasEditable = tiffs[cursorTiff].getCanvasEdit();

        canv = tiffs[cursorTiff].getTif();
        canvasEditable = tiffs[cursorTiff].getCanvasEdit();
        texture = tiffs[cursorTiff].getTexture();
        //canvasEditable.draw(texture).ink(0).update();
        setAtributos()
        
    }
    setAtributos = function(){
                $('.canvas').remove();
                canv.className ='canvas';
                $('.panzoom').append(canv);
                $canv = $('.canvas')

                $canv.css("width", "75%");
            }

    // Eventos 
    $btnAtras = $('.button-back');
    $btnAtras.click(function(){
        onclickAtras()
    });
    $btnAdelante = $('.button-next');
    $btnAdelante.click(function(){
        onclickAdelante()
    })
    $btnDiseno = $('.btnDisenoPrueba');
    $btnDiseno.click(function(){
        onclickDiseno()
    })
    $btnDiseno2 = $('.btnDisenoPrueba2');
    $btnDiseno2.click(function(){
        canvasEditable.draw(texture).ink(0.50).update();
        canv = canvasEditable;
        setAtributos()
        //tiffs[cursorTiff].setTif(canvasEditable)
        texture = canvasEditable.texture(canvasEditable);
        tiffs[cursorTiff].setTif(canvasEditable,texture,canvasEditable)
    })

    $btnUndo = $('.button-undo');
    $btnUndo.click(function(){
        onclickUndo()
    })

    $btnRepeat = $('.button-repeat');
    $btnRepeat.click(function(){
        onclickRepeat()
    })
    $btnSave = $('.button-save');
    $btnSave.click(function(){
        onclickSave()
    })
    $btnMultitif = $('.multitiff');
    $btnMultitif.click(function(){
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
    // function tifClass(origen, index){ 
    //     this.saved= true
    //     this.origen = origen; 
    //     this.index = index;
    //     this.versiones = [];
    //     this.verActual = -1;
        
    //     this.getTif = function (){ 
    //             return this.versiones[this.verActual];
    //     }
    //     this.getTifUndo = function (){ 
    //         if(this.verActual<=0){
    //             console.log("no ha habido ningun cambio");

    //         }else{
    //             this.verActual--;   
    //             this.saved = false;
    //             return this.getTif();
    //         }
    //     }
    //     this.getTifRepeat = function (){ 
    //         if(this.verActual==this.versiones.length-1){
    //             console.log("no ha habido ningun cambio");
    //         }else{
    //             this.verActual++; 
    //             this.saved = false; 
    //             return this.getTif();
    //         }
    //     }
    //     this.setTif = function (cambio){ 
    //         if(this.verActual == -1){
    //             this.versiones.push(cambio);
    //             this.verActual++;
    //         }else{
    //             l = this.versiones.length;
    //             this.versiones.splice(this.verActual+1,l-(this.verActual+1));
    //             this.versiones.push(cambio)
    //             this.verActual++;
    //             this.saved = false;
    //         }
            
    //     }
        
    //     this.isSaved = function(){
    //         return this.saved;
    //     }
    //     this.save = function(){
    //         this.saved = true;
    //     }
    //     this.setTif(origen);
        
    // }
    // a = new tifClass("",2)
    // a.setTif("asd")
    // a.getTifUndo()
    // a.getTifUndo()
    // a.getTifRepeat()
    // a.getTifRepeat()
    // console.log(a.getTif());

    //for(i = 0; i<1000; i++)
    // {   

        //$('.panzoom').replaceWith("<iframe src='\\web_tiff_widget\\static\\src\\img\\pdf.pdf'  frameborder='0'></iframe>");
        //$('.panzoom').append("<canvas class=\"divImage\" style=\"background-color: yellow;width:718px; height:700px;\"></canvas>");
        


        ///// CODIGO PARA BUSCAR EN LA BASE DE DATOS
// var s = new openerp.init();
// records = new s.web.Model('rbs.documento.mercantil.'+tipo).call('read',[[id],['filedata']],context=null);
// records.then(cargar2,function(err){
//                                 console.log("------error")
//                                 console.log(err);
//                             });
        ///// METODO ALTERNATIVO PARA BUSCAR ENB LA BASE DE DATOS USANDO DOMAIN
//var domain = [['state', '=', 'open'],['pos_session_id', '=', self.pos_session.id]]
//var records = new instance.web.Model(model.model).query(fields).filter(domain).context(context).all()
}


    
