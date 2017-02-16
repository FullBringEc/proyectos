        
$(function(){
    $el = $('body')
            
        $btnAtras = $el.find('.btnAtras');
        $btnAtras.click(function(){
            onclickAtras()
        });
        $btnAdelante = $el.find('.btnAdelante');
        $btnAdelante.click(function(){
            onclickAdelante()
        })
        $btnDiseno = $el.find('.btnDiseno');
        $btnDiseno.click(function(){
            onclickDiseno()
        })

    url = 'http://localhost:8069/registro_mercantil/BinaryTiff/tiff?model=rbs.documento.mercantil.acta&id=1&field=filedata&t=1478619739158'
    Tiff.initialize({TOTAL_MEMORY: 16777216 * 50});
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
        tiff = new Tiff({buffer: buffer});
        lenTiff =  tiff.countDirectory();
        for (var i = 0, len = tiff.countDirectory(); i < len; ++i) {
            tiffs.push(new tifClass(tiff,i));
        }
        onchange();
        
    }
    var canvasEditable = null;
    onclickAdelante = function(){if(cursorTiff!=lenTiff-1){cursorTiff++;onchange()}}
    onclickAtras = function(){if(cursorTiff!=0){cursorTiff--;onchange();}}
    onclickDiseno = function(){
        alert(canv.index)
        //if (texture == null){
            //texture = canvasEditable.texture(canv);
        //}
            canvasEditable.draw(texture).ink(.2).update();
            //canv = null
            //texture = null
            canv = canvasEditable;
            setAtributos()
            tiffs[cursorTiff].setTif(canvasEditable)
            texture = canvasEditable.texture(canvasEditable);
            tiffs[cursorTiff].setTexture(texture)
            //texture = canvasEditable.texture(canvasEditable);

        //canvasEditable = null
        //canvasEditable = fx.canvas();
    }
        onchange = function(){
        canv = null
        texture = null
        canvasEditable = null
        canvasEditable = tiffs[cursorTiff].getCanvasEdit();
        canv = tiffs[cursorTiff].getTif();
        texture = tiffs[cursorTiff].getTexture();
        setAtributos()
        
    }
    function tifClass(origen, index){ 
        this.canvasEdit;
        this.origen = origen; 
        this.index = index;
        this.versiones = [];
        this.verActual = -1;
        this.texture;
        this.getTexture = function(){
            if(this.texture == null)
            {
                this.texture = this.canvasEdit.texture(this.getTif());
            }
            return this.texture;
        }
        this.setTexture = function(texture){
            this.texture = texture;
        }
        this.canv = null;
        this.getTiff = function (){ 
            if(this.versiones.length == 0){
                this.origen.setDirectory(index);
                return this.origen.toCanvas();
            }else{
                return this.versiones[this.verActual]
            }
        }
        this.getCanvasEdit = function(){
            if(this.canvasEdit == null){
                this.canvasEdit = fx.canvas();
                return this.canvasEdit; 
            }else{
                return this.canvasEdit; 
            }

        }
        this.getTif = function (){ 
            if(this.canv == null){
                this.origen.setDirectory(index);
                this.canv = this.origen.toCanvas();
                this.canv.index = this.index;
                return this.canv;
            }else{
                return this.canv;
            }
        }
        this.setTif = function (canvas){ 
                this.canv = canvas
                this.canv.index = this.index;
        }
        this.setTiff = function (canvas){ 
            //if(this.verActual == -1){
                this.versiones.push(canvas)
                this.verActual++;
            /*}else{
               l = this.versiones.length
                this.versiones.splice(this.verActual+1,l-(this.verActual+1));
                this.versiones.push(canvas)
                this.verActual++;
            }*/
        }
    }
    xhr.send();
    setAtributos = function(){
        canv.className ='canvasTiff';
        $el = $('.canvasdisenado')
        $el.find('> canvas').remove();
        $el.append(canv);
        $canv= self.$el.find('.canvasTiff')


        $canv.css("width", "500px");
        $canv.css("height", "500px");
        $($canv).click(function(e) {
            if(self.view.get("actual_mode") == "view") {
                var $button = $(".oe_form_button_edit");
                $button.openerpBounce();
                self.stopPropagation();
            }
        });
        
        
        $canv.load(function() {
            if (! self.options.size)
                return;
            $canv.css("width", "" + self.options.size[0] + "px");
            $canv.css("height", "" + self.options.size[1] + "px");
        });
        $canv.on('error', function() {
            $canv.attr('src', self.placeholder);
            instance.webclient.notification.warn(_t("Tiff"), _t("No se puede visualizar el TIFF seleccionado"));
        });
    }

    
})