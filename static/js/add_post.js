document.addEventListener("DOMContentLoaded", function(event){
	var editorContainer = document.querySelector("textarea#post-body")
	var containerStyle = getComputedStyle(editorContainer)
	var editor = CKEDITOR.replace("post-body", {width: containerStyle.width, height: containerStyle.height})
	//editor.resize("80%", "20%")
	hljs.initHighlightingOnLoad()
	var tagsInput = document.getElementById("tags-input")
	var placeholderTagsInput = document.getElementById("placeholder-tags-input")
	var tagsInputPlugin = insignia(tagsInput);
	var form = document.getElementById("post-form") 

	tagsInput.addEventListener("focus", function(event){
		var div = document.getElementById("tag-input-div")
		div.style.border = "1px solid #129FEA"
	});

	tagsInput.addEventListener("blur", function(event){
		var div = document.getElementById("tag-input-div")
		div.style.border = "1px solid #ccc"
	});

	form.addEventListener("submit", function(event){
		placeholderTagsInput.value = tagsInputPlugin.value()
	})

})
