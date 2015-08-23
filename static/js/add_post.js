document.addEventListener("DOMContentLoaded", function(event){
	var editorContainer = document.querySelector("textarea#post-body")
	var containerStyle = getComputedStyle(editorContainer)
	var editor = CKEDITOR.replace("post-body", {width: containerStyle.width, height: containerStyle.height})
	//editor.resize("80%", "20%")
	hljs.initHighlightingOnLoad()
})
