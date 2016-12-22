  // (function() {
  //         var $section = $('section').first();

  //         $section.find('.panzoom').panzoom({
  //           $zoomIn: $section.find(".zoom-in"),
  //           $zoomOut: $section.find(".zoom-out"),
  //           $zoomRange: $section.find(".zoom-range"),
  //           $reset: $section.find(".reset")
  //         });
  //       })();

    (function() {
          var $section = $('section').first();

          $section.find('.panzoom').panzoom({
            $zoomIn: $section.find(".zoom-in"),
            $zoomOut: $section.find(".zoom-out"),
            $zoomRange: $section.find(".zoom-range"),
            $reset: $section.find(".reset")
          });
        })();
  
(function() {
  var $section = $('#focal');
  var $panzoom = $section.find('.panzoom').panzoom();
  $panzoom.parent().on('mousewheel.focal', function( e ) {
    e.preventDefault();
    var delta = e.delta || e.originalEvent.wheelDelta;
    var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;
    $panzoom.panzoom('zoom', zoomOut, {
      animate: false,
      focal: e
    });
  });
})();
  