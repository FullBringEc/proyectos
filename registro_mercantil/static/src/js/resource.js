
openerp.registro_mercantil = function (instance)
{   
	
	var instance = openerp;
	var _t = instance.web._t,
	_lt = instance.web._lt;
	var QWeb = instance.web.qweb;  
    /*instance.web.client_actions.add('tiff.ui', 'instance.web_tiff_widget.TiffWidget');*/
    instance.web.form.FieldBinaryTiff = instance.web.form.FieldBinary.extend({

        template: 'FieldBinaryTiff',
        placeholder: "/web/static/src/img/placeholder.png",
        numRender : 0,
        init: function(field_manager, node) {
            var self = this;
            this._super(field_manager, node);
            this.binary_value = false;
            this.useFileAPI = !!window.FileReader;
            this.max_upload_size = 50 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                this.fileupload_id = _.uniqueId('oe_fileupload');
                $(window).on(this.fileupload_id, function() {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
        render_value: function(){
            
            var self = this;
            self.$el.find('.divC').css('width',self.options.size[0])
            if(self.numRender == 0){
                self.numRender=1;
                $btnAtras = self.$el.find('.buttonback');
                $btnAtras.click(function(){
                    onclickAtras()
                });
                $btnAdelante = self.$el.find('.buttonnext');
                $btnAdelante.click(function(){
                    onclickAdelante()
                    console.log("adelante")
                });


                $btnDiseno = self.$el.find('.btnDiseno');
                $btnDiseno.click(function(){
                    onclickDiseno()
                })

                $btnUndo = self.$el.find('.button-undo');
                $btnUndo.click(function(){
                    onclickUndo()
                })

                $btnRepeat = self.$el.find('.button-repeat');
                $btnRepeat.click(function(){
                    onclickRepeat()
                })
                $btnSave = self.$el.find('.button-save');
                $btnSave.click(function(){
                    onclickSave()
                })
                $exportar_pdf = self.$el.find('.exportar_pdf');
                $exportar_pdf.click(function(){
                    var doc = null;
                    cursor = 0;
                    function load_imagen(index){
                        if(index > (lenTiff-1)){
                                return true
                            }
                        imagen = tiffs[index].getTif()
                        var img = new Image();
                        img.onload = function() {

                            var w = img.naturalWidth/10;   // this will be 300
                            var h = img.naturalHeight/10;
                            console.log(doc)
                            if (doc == null){
                                doc = new jsPDF('p', 'px', [w, h]);
                            }else{
                                doc.addPage(w,h)
                            }
                            // w = 2000//tiffs[i].width
                            // h = 2000//tiffs[i].height
                            // console.log(w +" - "+ h)
                            
                            doc.addImage(this.src, 'png', 0, 0, w,h);
                            
                            // console.log("imagen")
                            if(index >= (lenTiff-1)){
                                console.log(index +" " + (lenTiff-1))

                                doc.save('Test.pdf');
                            }
                            load_imagen(index+1)
                            
                        }
                        //console.log(this.getTif())
                        // image.src = "data:image/png;base64,"+this.getTif();
                        img.src = "data:image/png;base64,"+imagen
                    }
                    load_imagen(0)
                   
                    
                    
                })




                
                // $btnMultitif = self.$el.find('.multitiff');
                // $btnMultitif.click(function(){
                //     instance.web.blockUI();
                //     var c = instance.webclient.crashmanager;
                //     //alert(tiffs[cursorTiff])
                //     self.session.get_file({
                //         url: '/web/binary/multitiff',
                //         data: {
                //             data: JSON.stringify({
                //                 model: tiffs[cursorTiff].getTif().toDataURL()
                //             })},
                //         complete: instance.web.unblockUI,
                //         error: c.rpc_error.bind(c)
                //     });


                // })
            }
            var lenTiff = 0;
            var cursorTiff =  0;
            var tiffs = [];
            tipo = this.options.tipo
            id = parseInt(JSON.stringify(this.view.datarecord.id))
            $canv = $('.imagenCanvas')
            $ctx = $canv[0].getContext("2d");
            // alert(id)
            // lienzo = new CanvasState($('#figurasCanvas')[0],$('#borradorCanvas')[0]);
            console.log(tipo+" - "+id)
            if(id){
                new openerp.web.Model('rbs.documento.'+tipo).call('read',[[id],['compania_nombres','fecha_inscripcion', 'contenedor_id']])
                        .then(function(result){
                            console.log(result)
                            $('#tipo').html(tipo)
                            $('#propietario').html(result[0].compania_nombres)
                            $('#fecha').html(result[0].fecha_inscripcion)
                            new openerp.web.Model('rbs.imagenes').query(['imagen']).filter([['contenedor_id','=',result[0].contenedor_id[0]]]).context(null).all()
                            .then(function(result){  

                                lenTiff =  result.length;
                                for (var i=0; i<result.length; i++){
                                    tiffs.push(new tifClass(result[i].imagen,i,result[i].id));
                                }
                                
                                on_change();
                            })
                        })
                }
            // console.log($ctx)
            function tifClass(TIfforiginal, index, id){
                this.saved= true
                this.TIfforiginal = TIfforiginal;
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
                    return this.TIfforiginal;
                }

                this.getTif = function (){ 
                    if(this.versiones.length == 0){
                        return this.TIfforiginal;
                        
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
                    // console.log(width+" "+height)

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
                        // console.log(url)
                 
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


                this.guardarImagen = function(){
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
                            // console.log(c)
                            new openerp.web.Model('rbs.imagenes').call('actualizarImagen',[[self.idBD],c])
                                .then(function(result){
                                    // console.log(result)
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
                try{
                    var image = new Image();
                    image.onload = function() {
                        var width = image.naturalWidth;   // this will be 300
                        var height = image.naturalHeight; // this will be 400



                        // $(".pagina_actual").val(cursorTiff+1)      
                        // $(".pagina_final").val(lenTiff)
                        // lienzo.shapes=tiffs[cursorTiff].getShapes()
                        $canv[0].width = width;
                        $canv[0].height = height;
                        $ctx.drawImage(image, 0, 0, width, height);

                        // lienzo.valid=false
                        // lienzo.setSize(width,height);
                    };
                    // console.log(tiffs[0])
                    image.src = "data:image/png;base64,"+tiffs[cursorTiff].getTif();
                    // console.log("paso por aqui"+self.options.size[0])
                    $canv.css("width", "" + (self.options.size[0]*(9/10)) + "px")

                }catch(e){
                    // console.log(e)
                }
                
                
            }
                        

            /*
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
                
            }*/
            //var canvasEditable = fx.canvas();
            onclickAdelante = function(){
                if(cursorTiff!=lenTiff-1){
                    if(tiffs[cursorTiff].isSaved()){
                        cursorTiff++;
                        on_change()
                    }else{
                        alert("Para cambiar de imagen primero almacene la actual")
                    }
                }
            }
            onclickAtras = function(){
                if(cursorTiff!=0){
                    if(tiffs[cursorTiff].isSaved()){
                        cursorTiff--;on_change();
                    }else{
                        alert("Para cambiar de imagen primero almacene la actual")
                    }
                }
            }
            onclickUndo = function(){
                tiffs[cursorTiff].setTifUndo();
                on_change()
            }
            onclickRepeat = function(){
                tiffs[cursorTiff].setTifRepeat();
                on_change()
            }
            onclickSave = function(){
                tiffs[cursorTiff].save();
                //onchange()
            }
        },
        

        on_file_uploaded_and_valid: function(size, name, content_type, file_base64) {
            this.internal_set_value(file_base64);
            this.binary_value = true;
            this.render_value();
            this.set_filename(name);
        },
        on_clear: function() {
            new openerp.web.Model('rbs.documento.'+this.options.tipo).call('borrar_contenedor',[[parseInt(JSON.stringify(this.view.datarecord.id))]])
                        .then(function(result){
                            console.log(result)
                            
                        })
            this._super.apply(this, arguments);

            this.render_value();
            this.set_filename('');
        },
        set_value: function(value_){
            console.log(value_)
            // console.log(this.get_value())
            var changed = value_ !== this.get_value();
            this._super.apply(this, arguments);
            // By default, on binary images read, the server returns the binary size
            // This is possible that two images have the exact same size
            // Therefore we trigger the change in case the image value hasn't changed
            // So the image is re-rendered correctly
            if (!changed){
                this.trigger("change:value", this, {
                    oldValue: value_,
                    newValue: value_

                });

            }
        }
});

instance.web.form.FieldUrlTiff = instance.web.form.FieldChar.extend({
    template: 'FieldUrlTiff',
    initialize_content: function() {
        this._super();
        var $button = this.$el.find('button');
        $button.click(this.on_button_clicked);
        this.setupFocus($button);
    },
    render_value: function() {
        var show_value = this.format_value(this.get('value'), '');
        
        
        if (!this.get("effective_readonly")) {
            this.$el.find('input').val(show_value);
        } else {
            if (this.password) {
                show_value = new Array(show_value.length + 1).join('*');
            }
            this.$(".oe_form_char_content").text(show_value);
            this.$el.find('iframe')
                    .attr('src',this.get('value'))
                    .css("width", "" + this.options.size[0] + "px")
                    .css("height", "" + this.options.size[1] + "px")

        }




            
    },
    on_button_clicked: function() {
        if (!this.get('value') || !this.is_syntax_valid()) {
            this.do_warn(_t("E-mail Error"), _t("Can't send email to invalid e-mail address"));
        } else {
            location.href = 'mailto:' + this.get('value');
        }
    }
});
    instance.web.form.widgets.add('FieldUrlTiff', 'instance.web.form.FieldUrlTiff');
    instance.web.form.widgets.add('FieldBinaryTiff', 'instance.web.form.FieldBinaryTiff');
}

