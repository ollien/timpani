/*jshint eqnull: true */
document.addEventListener("DOMContentLoaded", function (event) {
	var code = document.querySelectorAll("[class*=\"language-\"]");
	Array.prototype.slice.call(code).forEach(function (element) {
		Prism.highlightElement(element);
	});
});
