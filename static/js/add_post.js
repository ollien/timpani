document.addEventListener("DOMContentLoaded", function(event){
	var editorContainer = document.querySelector("textarea#post-body")
	var containerStyle = getComputedStyle(editorContainer)
	var editor = CKEDITOR.replace("post-body", {width: containerStyle.width, height: containerStyle.height})
	//editor.resize("80%", "20%")
	hljs.initHighlightingOnLoad()
	var tagsInput = document.getElementById("tags-input")
	var placeholderTagsInput = document.getElementById("placeholder-tags-input")
	var tagsInputPlugin = insignia(tagsInput, {deletion: true});
	tagsInput.addEventListener("focus", function(event){
		var div = document.getElementById("tag-input-div")
		div.style.border = "1px solid #129FEA"
	});

	tagsInput.addEventListener("blur", function(event){
		var div = document.getElementById("tag-input-div")
		div.style.border = "1px solid #ccc"
	});

	tagsInput.addEventListener("insignia-evaluated", function(event){
		placeholderTagsInput.value = tagsInputPlugin.value()
		tags = Array.prototype.slice.call(tagsInput.parentNode.querySelectorAll("span.nsg-tag"))
		tags.forEach(function(node){
			var removeButton = node.querySelector(".nsg-tag-remove")	
			//This attribute is set to make sure we don't have multiple listeners
			var attr = removeButton.getAttribute("listener")
			if (attr == null || attr != "set"){
				removeButton.setAttribute("listener", "set")
				removeButton.addEventListener("mouseenter", function(event){
					node.classList.add("faded")
				})
				removeButton.addEventListener("mouseleave", function(event){
					node.classList.remove("faded")
				})
			}
		})
	})

})
