
openerp.web_tiff_widget = function (instance)
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
            this.max_upload_size = 25 * 1024 * 1024; // 25Mo
            if (!this.useFileAPI) {
                this.fileupload_id = _.uniqueId('oe_fileupload');
                $(window).on(this.fileupload_id, function() {
                    var args = [].slice.call(arguments).slice(1);
                    self.on_file_uploaded.apply(self, args);
                });
            }
        },
        render_value: function() {
            
            var self = this;
            var url;
            Tiff.initialize({TOTAL_MEMORY: 16777216 * 50});
            if (this.get('value') && !instance.web.form.is_bin_size(this.get('value'))) {
                url = 'data:image/tiff;base64,' + this.get('value');
            } else if (this.get('value')) {
                var id = JSON.stringify(this.view.datarecord.id || null);
                var field = this.name;
                if (this.options.preview_image)
                    field = this.options.preview_image;
                alert(id + " - "+ field + " - "+ (new Date().getTime()))
                url = this.session.url('/web_tiff_widget/BinaryTiff/tiff', {
                                            model: this.view.dataset.model,
                                            id: id,
                                            field: field,
                                            t: (new Date().getTime()),
                });
            } else {
                url = this.placeholder;
            }

                this.cargarEditorTiff(self,url);
            
            
        },
        cargarEditorTiff: function(self,url){
            
            if(self.numRender == 0){
                self.numRender=1;
                $btnAtras = self.$el.find('.buttonback');
                $btnAtras.click(function(){
                    onclickAtras()
                });
                $btnAdelante = self.$el.find('.buttonnext');
                $btnAdelante.click(function(){
                    onclickAdelante()
                })
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
                $btnMultitif = self.$el.find('.multitiff');
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
            }
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
            //var canvasEditable = fx.canvas();
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
                canvasEditable.draw(texture).ink(0).update();
                setAtributos()
                
            }
            


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
                /*this.getTiff = function (){ 
                    if(this.versiones.length == 0){
                        this.origen.setDirectory(index);
                        return this.origen.toCanvas();
                    }else{
                        return this.versiones[this.verActual]
                    }
                }
                this.setTiff = function (canvas){ 
                    if(this.verActual == -1){
                        this.versiones.push(canvas)
                        this.verActual++;
                    }else{
                        l = this.versiones.length
                        this.versiones.splice(this.verActual+1,l-(this.verActual+1));
                        this.versiones.push(canvas)
                        this.verActual++;
                    }
                }*/
            }
            xhr.send();
            setAtributos = function(){
                
                self.$el.find('.canvas').remove();
                canv.className ='canvas';
                self.$el.find('.divgeneral .divC').append(canv);
                $canv= self.$el.find('.canvas')

                self.$el.find('.divgeneral').css("width", "" + self.options.size[0] + "px");
                self.$el.find('.divgeneral').css("height", "" + self.options.size[1] + "px");


                //self.$el.find('.div-canvas').css("text-align","center")
                
                $canv.css("height", "100%");
                //$canv.css("height", "100%");
                //$canv.css("height", "" + self.options.size[1] + "px");
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

            
        },
        

        on_file_uploaded_and_valid: function(size, name, content_type, file_base64) {
            this.internal_set_value(file_base64);
            this.binary_value = true;
            this.render_value();
            this.set_filename(name);
        },
        on_clear: function() {
            this._super.apply(this, arguments);
            this.render_value();
            this.set_filename('');
        },
        set_value: function(value_){
            
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

