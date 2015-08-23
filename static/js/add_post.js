document.addEventListener("DOMContentLoaded", function(event){
	var editorContainer = document.querySelector("div#main-wrapper")
	var containerStyle = getComputedStyle(editorContainer)
	var editor = CKEDITOR.replace("post-body", {width: containerStyle.width, height: containerStyle.height})
	hljs.initHighlightingOnLoad()
})
