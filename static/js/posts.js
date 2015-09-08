document.addEventListener("DOMContentLoaded", function(event){
	console.log("running")
	var code = document.querySelectorAll("[class*=language-");
	console.log(code)
	Array.prototype.slice.call(code).forEach(function(element){
		console.log(element)
		Prism.highlightElement(element)	
	})
})
