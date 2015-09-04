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
	var modalInput = linkModalElement.querySelector("input#modal-link")	

	editor.addModule("toolbar", {container: "div#toolbar"})

	linkButton.addEventListener("click", function(event){
		//Once the input is focused, we will lose our selection. We need to get it now.
		linkModal.show()
		modalInput.focus()
	})

	linkModal.element.addEventListener("positive-pressed", function(event){
		if (modalInput.value.length === 0) {
			modalInput.setCustomValidity("Please enter a link")	
			event.preventDefault()
		}
		else {
			editor.focus()
			var selection = editor.getSelection()
			editor.setSelection(null)
			//This basically indicates that we don't actually have a selection.
			if (selection.end - selection.start === 0){
				console.log(modalInput.value)
				console.log(selection.start)
				console.log(modalInput.value)
				editor.insertText(selection.start, modalInput.value, "link", modalInput.value)	
			}
		}
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
