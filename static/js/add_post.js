document.addEventListener("DOMContentLoaded", function(event){
	var editorContainer = document.querySelector("textarea#post-body")
	console.log(editorContainer)
	var containerStyle = getComputedStyle(editorContainer)
	console.log(containerStyle)
	var editor = CKEDITOR.replace("post-body", {height: containerStyle.height})
	//editor.resize("80%", "20%")
	hljs.initHighlightingOnLoad()
})
