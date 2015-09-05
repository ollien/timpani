document.addEventListener("DOMContentLoaded", function(event){
	var editorDiv = document.getElementById("editor")
	var editor = new Quill(editorDiv)
	var postBodyInput = document.getElementById("post-body")
	var validityInput = document.getElementById("post-validity")
	var tagsInput = document.getElementById("tags-input")
	var placeholderTagsInput = document.getElementById("placeholder-tags-input")
	var tagsInputPlugin = insignia(tagsInput);
	var form = document.getElementById("post-form") 
	var linkButton = document.getElementById("add-link")
	var linkModalElement = document.getElementById("link-modal")
	var linkModal = new Modal(linkModalElement)
	var linkModalInput = linkModalElement.querySelector("input#modal-link")	
	var linkModalError = linkModalElement.querySelector("div.modal-error")
	var alignLeft = document.getElementById("align-left")
	var alignCenter = document.getElementById("align-center")
	var alignRight = document.getElementById("align-right")
	var alignJustify = document.getElementById("align-justify")

	editor.addModule("toolbar", {container: "div#toolbar"})
	console.log(editor)
	editor.on("selection-change", function(range){
		if (range == null){
			editorDiv.classList.remove("focused")
		}

		else {
			editorDiv.classList.add("focused")
		}
	})


	linkButton.addEventListener("click", function(event){
		//Once the input is focused, we will lose our selection. We need to get it now.
		linkModal.show()
		linkModalInput.focus()
	})

	alignLeft.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "left")	
		}
	})

	alignCenter.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "center")	
		}
	})

	alignRight.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "right")	
		}
	})

	alignJustify.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatText(selection.start, selection.end+1, "align", "justify")	
			console.log(selection)
			console.log("formatted")
		}
	})

	linkModal.element.addEventListener("positive-pressed", function(event){
		if (linkModalInput.value.trim().length === 0) {
			linkModalError.classList.add("active")
			event.preventDefault();
		}
		else {
			editor.focus()
			var selection = editor.getSelection()
			editor.setSelection(null)
			//This basically indicates that we don't actually have a selection.
			if (selection.end - selection.start === 0){
				editor.insertText(selection.start, linkModalInput.value, "link", linkModalInput.value)	
			}
		}
	})

	linkModal.element.addEventListener("hide", function(event){
		linkModalInput.value = ""
		linkModalError.classList.remove("active")
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

