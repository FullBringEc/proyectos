Tiff.initialize({TOTAL_MEMORY: 16777216 * 50});
self.addEventListener('message', function(milliseconds) {
	self.postMessage("inicio el proceso");
}, false);