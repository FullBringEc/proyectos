accion = function(){
        public = {};
        public.contrast=false;
        public.brightness=false;
        public.bw=false;
        public.sepia=false;
        public.invert=false;
        public.orden = [];
        public.recortes = [];
        public.addAccion = function(funcion, valor){
            if(funcion=="contrast" || 
                funcion=="brightness"){
                addOrden(funcion, valor)
            }else{
                eval("public."+funcion+" = "+valor)  
            }
        };

        public.addAccion = function(texto, x,y){
            if(funcion=="contrast" || 
                funcion=="brightness"){
                addOrden(funcion, valor)
            }else{
                eval("public."+funcion+" = "+valor)  
            }
        };

        public.execute = function(){
            for (i in public.orden) {
                eval("console.log(public."+public.orden[i]+");")
            }
        }

        function addOrden(funcion, valor){
            var index = public.orden.indexOf(funcion);
            if ( index == -1){
                public.orden.push(funcion);
            }
            eval("public."+funcion+" = "+valor)            

        }


        return public;

    }

var cursorTexto=false;
//console.log("asdasd")
$($('.btnAddText').click(function(){
    console.log("asd");
        if(!cursorTexto){
            $canv.css("cursor", "text");
            cursorTexto = true;
        }else{
            $canv.css("cursor", "default");
            cursorTexto = false;
        }
    }))

var app = ( function () {
        getCanvas = function(){
            return $('#imagenCanvas')    
        }
        
        getContext = function(){
            
            context = getCanvas()[0].getContext( '2d' )
            return context;
        }
        // API
        public = {};
        
        public.loadPicture = function () {
            var imageObj = new Image();
            imageObj.src = 'image.jpg';

            imageObj.onload = function () {
                getContext().drawImage( imageObj, 0, 0 );
            }
        };

        public.getImgData = function () {
            return getContext().getImageData( 0, 0, getCanvas()[0].width, getCanvas()[0].height );
        };

        // Filters
        public.filters = {};
         
        public.filters.bw = function () {

            var imageData = app.getImgData(),
                pixels = imageData.data,
                numPixels = imageData.width * imageData.height;
         
            for ( var i = 0; i < numPixels; i++ ) {
                var r = pixels[ i * 4 ];
                var g = pixels[ i * 4 + 1 ];
                var b = pixels[ i * 4 + 2 ];
         
                var grey = ( r + g + b ) / 3;
         
                pixels[ i * 4 ] = grey;
                pixels[ i * 4 + 1 ] = grey;
                pixels[ i * 4 + 2 ] = grey;
            }
         
            getContext().putImageData( imageData, 0, 0 );
        };


        public.filters.invert  = function () {
            var imageData = app.getImgData(),
                pixels = imageData.data,
                numPixels = imageData.width * imageData.height;
         
            for ( var i = 0; i < numPixels; i++ ) {
                var r = pixels[ i * 4 ];
                var g = pixels[ i * 4 + 1 ];
                var b = pixels[ i * 4 + 2 ];
         
                pixels[ i * 4 ] = 255 - r;
                pixels[ i * 4 + 1 ] = 255 - g;
                pixels[ i * 4 + 2 ] = 255 - b;
            }
         
            getContext().putImageData( imageData, 0, 0 );
        };

        public.filters.sepia = function () {
            var imageData = app.getImgData(),
                pixels = imageData.data,
                numPixels = imageData.width * imageData.height;
         
            for ( var i = 0; i < numPixels; i++ ) {
                var r = pixels[ i * 4 ];
                var g = pixels[ i * 4 + 1 ];
                var b = pixels[ i * 4 + 2 ];
         
                pixels[ i * 4 ] = 255 - r;
                pixels[ i * 4 + 1 ] = 255 - g;
                pixels[ i * 4 + 2 ] = 255 - b;
         
                pixels[ i * 4 ] = ( r * .393 ) + ( g *.769 ) + ( b * .189 );
                pixels[ i * 4 + 1 ] = ( r * .349 ) + ( g *.686 ) + ( b * .168 );
                pixels[ i * 4 + 2 ] = ( r * .272 ) + ( g *.534 ) + ( b * .131 );
            }
         
            getContext().putImageData( imageData, 0, 0 );
        };


        public.filters.contrast = function ( contrast , canvas) {
            console.log("api.filters.contrast("+contrast+");")
            var imageData;
            var pixels;
            var numPixels;
            var factor;
            var context;
            if(canvas!=undefined)
            {
                context = canvas[0].getContext( '2d' );
                imageData = context.getImageData( 0, 0, canvas[0].width, canvas[0].height );
                
            }else{
                context = getContext();
                imageData = app.getImgData();
            }
            pixels = imageData.data;
            numPixels = imageData.width * imageData.height;

                
         
            contrast || ( contrast = 100 ); // Default value
         
            factor = ( 259 * ( contrast + 255 ) ) / ( 255 * ( 259 - contrast ) );
         
            for ( var i = 0; i < numPixels; i++ ) {
                var r = pixels[ i * 4 ];
                var g = pixels[ i * 4 + 1 ];
                var b = pixels[ i * 4 + 2 ];
         
                pixels[ i * 4 ] = factor * ( r - 128 ) + 128;
                pixels[ i * 4 + 1 ] = factor * ( g - 128 ) + 128;
                pixels[ i * 4 + 2 ] = factor * ( b - 128 ) + 128;
            }
         
            context.putImageData( imageData, 0, 0 );
        };

        public.filters.brightness  = function (level) {
            var imageData = app.getImgData(),
                pixels = imageData.data,
                //numPixels = imageData.width * imageData.height;
                height = imageData.width,
                width  = imageData.height;
            for (var y = 0; y < height; y++) {
                for (var x = 0; x < width; x++) {
                    pixels[(y * width + x) * 4 + 0] += level;
                    pixels[(y * width + x) * 4 + 1] += level;
                    pixels[(y * width + x) * 4 + 2] += level;
                }
            }
         
            getContext().putImageData( imageData, 0, 0 );
        };
        
        
        public.save = function () {
            var link = window.document.createElement( 'a' ),
                url = getCanvas().toDataURL(),
                filename = 'screenshot.jpg';
                console.log(url)
         
            link.setAttribute( 'href', url );
            link.setAttribute( 'download', filename );
            link.style.visibility = 'hidden';
            window.document.body.appendChild( link );
            link.click();
            window.document.body.removeChild( link );
        };
        return public;
} () );