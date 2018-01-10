odoo.define('web.pdf_binary', function (require) {
// "use strict";
    
    var core = require('web.core');
    var widget = require('web.form_widgets');
    var FormView = require('web.FormView');
    var QWeb = core.qweb;
    var _lt = core._lt;
    console.log(widget)
	// var instance = openerp;
	// var _t = instance.web._t,
	// _lt = instance.web._lt;
	// var QWeb = instance.web.qweb;  
    /*instance.web.client_actions.add('tiff.ui', 'instance.web_tiff_widget.TiffWidget');*/
    
    var FieldPdfBinary = core.form_widget_registry.get("binary").extend({
        template: 'pdf_binary',
        // placeholder: "/web/static/src/img/placeholder.png",
        numRender : 0,
        init: function(field_manager, node) {
            var self = this;
            this._super(field_manager, node);
            this.binary_value = false;
            this.useFileAPI = !!window.FileReader;
            this.max_upload_size = 25 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                this.fileupload_id = _.uniqueId('o_fileupload');
                $(window).on(this.fileupload_id, function() {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
        render_value: function(){

            var self = this;
            // var $content = $(QWeb.render("pdf_binary_content"));
            // this.$('> img').remove();
            // this.$el.prepend($content);
            // console.log($content)

            self.$el.find('.divC').css('width',self.options.size[0])
            // if(self.numRender == 0){
                // self.numRender=1;
            $btnAtras = self.$el.find('.buttonback');
            $btnAtras.unbind('click');
            $btnAtras.click(function(){
                onclickAtras()
            });
            $btnAdelante = self.$el.find('.buttonnext');
            $btnAdelante.unbind('click');
            $btnAdelante.click(function(){
                onclickAdelante()
                console.log("adelante")
            });

            $pagina_actual = self.$el.find('.pagina_actual');
            $pagina_actual.unbind('keypress');
            $pagina_actual.keypress(function(e){
                if(e.keyCode == 13){
                    nueva_pagina=$(".pagina_actual").val()-1
                    if (nueva_pagina<lenTiff && nueva_pagina>=0){
                        cursorTiff=nueva_pagina;
                        on_change();
                    }
                    else {
                        $(".pagina_actual").val(cursorTiff+1) 
                    }
                }}    
                );


            $btnDiseno = self.$el.find('.btnDiseno');
            $btnDiseno.unbind('click');
            $btnDiseno.click(function(){
                onclickDiseno()
            })
            $exportar_pdf = self.$el.find('.exportar_pdf');
            $exportar_pdf.unbind('click');
            $exportar_pdf.click(function(){
                var doc = null;
                cursor = 0;
                function load_imagen(index){
                    if(index > (lenTiff-1)){
                            return true
                        }
                    tiffs[index].getTif(cb)
                    function cb(imagen){
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
                            doc.addImage(this.src, 'jpeg', 0, 0, w,h);
                            if(index >= (lenTiff-1)){
                                console.log(index +" " + (lenTiff-1))
                                doc.save('Test.pdf');
                            }
                            load_imagen(index+1)
                        }
                        img.src = "data:image/jpeg;base64,"+imagen
                    }
                }
                load_imagen(0)
               
                
                
            })
            var lenTiff = 0;
            var cursorTiff =  0;
            var tiffs = [];
            tipo = this.options.tipo
            id = parseInt(JSON.stringify(this.view.datarecord.id))
            $canv = self.$el.find('.imagenCanvas')
            console.log($canv);
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
                            new openerp.web.Model('rbs.imagenes').query(['id']).filter([['contenedor_id','=',result[0].contenedor_id[0]]]).context(null).all()
                            .then(function(result){  
                                lenTiff =  result.length;
                                for (var i=0; i<result.length; i++){
                                    tiffs.push(new tifClass(i,result[i].id));
                                }
                                on_change();
                            })
                        })
                }
            function tifClass(index, id){
                this.saved= true
                // this.TIfforiginal = TIfforiginal;
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

                
                this.getTif = function(cb){ 
                    
                    new openerp.web.Model('rbs.imagenes').query(['imagen']).filter([['id','=',this.idBD]]).context(null).all()
                    .then(function(result){  
                        cb(result[0].imagen)
                    })
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
                }
                this.unsave = function(){
                    this.saved = false;
                }
                var accion
            }
            on_change = function(){
                try{
                    tiffs[cursorTiff].getTif(reload_image)
                }catch(e){

                }
                
            }
            reload_image = function(img){
                var image = new Image();
                image.onload = function() {
                    var width = image.naturalWidth;   // this will be 300
                    var height = image.naturalHeight; // this will be 400
                    $(".pagina_actual").val(cursorTiff+1)      
                    $(".pagina_final").val(lenTiff)
                    $canv[0].width = width;
                    $canv[0].height = height;
                    $ctx.drawImage(image, 0, 0, width, height);
                };
                image.src = "data:image/png;base64,"+img;
                $canv.css("width", "" + (self.options.size[0]*(9/10)) + "px")
            }
            onclickAdelante = function(){
                if(cursorTiff!=lenTiff-1){
                    cursorTiff++;
                    console.log(cursorTiff,"index")
                    on_change()
                }
            }
            onclickAtras = function(){
                if(cursorTiff!=0){
                        cursorTiff--;
                        on_change();
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

// var FieldUrlTiff = widget.FieldChar.extend({
//     template: 'FieldUrlTiff',
//     initialize_content: function() {
//         this._super();
//         var $button = this.$el.find('button');
//         $button.click(this.on_button_clicked);
//         this.setupFocus($button);
//     },
//     render_value: function() {
//         var show_value = this.format_value(this.get('value'), '');
        
        
//         if (!this.get("effective_readonly")) {
//             this.$el.find('input').val(show_value);
//         } else {
//             if (this.password) {
//                 show_value = new Array(show_value.length + 1).join('*');
//             }
//             this.$(".oe_form_char_content").text(show_value);
//             this.$el.find('iframe')
//                     .attr('src',this.get('value'))
//                     .css("width", "" + this.options.size[0] + "px")
//                     .css("height", "" + this.options.size[1] + "px")

//         }




            
//     },
//     on_button_clicked: function() {
//         if (!this.get('value') || !this.is_syntax_valid()) {
//             this.do_warn(_t("E-mail Error"), _t("Can't send email to invalid e-mail address"));
//         } else {
//             location.href = 'mailto:' + this.get('value');
//         }
//     }
// });
    // instance.web.form.widgets.add('FieldUrlTiff', 'instance.web.form.FieldUrlTiff');
    // instance.web.form.widgets.add('FieldBinaryTiff', 'instance.web.form.FieldBinaryTiff');

    core.form_widget_registry.add('pdf_binary', FieldPdfBinary);
    // core.form_widget_registry.add('FieldBinaryTiff', widget.FieldBinaryImage);

    /*
     * Init jscolor for each editable mode on view form
     */
    // FormView.include({
    //     on_button_edit: function () {
    //         this._super();
    //         jscolor.init(this.$el[0]);
    //     },
    //     on_button_create: function () {
    //         this._super();
    //         jscolor.init(this.$el[0]);
    //     }
    // });

    return {
        FieldPdfBinary: FieldPdfBinary,
        // FieldBinaryTiff: FieldBinaryTiff
    };
})