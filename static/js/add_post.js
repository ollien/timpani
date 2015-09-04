document.addEventListener("DOMContentLoaded", function(event){
	var editor = new Quill("div#editor")
	var postBodyInput = document.getElementById("post-body")
	var validityInput = document.getElementById("post-validity")
	var tagsInput = document.getElementById("tags-input")
	var placeholderTagsInput = document.getElementById("placeholder-tags-input")
	var tagsInputPlugin = insignia(tagsInput);
	var form = document.getElementById("post-form") 
	var linkButton = document.getElementById("add-link")
	var linkModalElement = document.getElementById("link-modal")
	var linkModal = new Modal(linkModalElement)

	editor.addModule("toolbar", {container: "div#toolbar"})

	linkButton.addEventListener("click", function(event){
		linkModal.show()
	})

	tagsInput.addEventListener("focus", function(event){
		var div = document.getElementById("tag-input-div")
		div.classList.add("focused")
	});

	tagsInput.addEventListener("blur", function(event){
		var div = document.getElementById("tag-input-div")
		div.classList.remove("focused")
	});

	form.addEventListener("submit", function(event){
		if (editor.getText().trim().length == 0) {
			validityInput.setCustomValidity("Please fill out a post body.")		
			event.preventDefault();
		}
		else {
			postBodyInput.value = editor.getHTML();	
			placeholderTagsInput.value = tagsInputPlugin.value()
		}
	})

})
