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
	var imageButton = document.getElementById("add-image")
	var alignLeftButton = document.getElementById("align-left")
	var alignCenterButton = document.getElementById("align-center")
	var alignRightButton = document.getElementById("align-right")
	var alignJustifyButton = document.getElementById("align-justify")

	var linkModal = {
		element: document.getElementById("link-modal"),
		input: document.getElementById("modal-link"),
		init: function() { //We needt o access some objects within this obect upon initialization, so we use this function to do that.
			this.modal = new Modal(this.element)
			this.errorDiv = this.element.querySelector("div.modal-error")
			delete this.init
			return this
		}
	}.init()

	var imageModal = {
		element: document.getElementById("image-modal"),
		linkInput: document.getElementById("image-url"),
		fileInput: document.getElementById("image-upload"),
		uploadRequest: null, //This will be defined when an image is being uploaded. This is a global variable so it can be cancelled.
		init: function(){ //We need to access some objects within this object upon initializaton, so we use this function to do that.
			this.modal = new Modal(this.element)
			this.positiveButton = this.element.querySelector("button.positive") //We need to do some styling with this button, so it's better to find it now rather than later.
			delete this.init
			return this
		},
	}.init()
	

	editor.addModule("toolbar", {container: "div#toolbar"})
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

	imageButton.addEventListener("click", function(event){
		imageModal.show()	
	})

	alignLeftButton.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "left")	
		}
	})

	alignCenterButton.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "center")	
		}
	})

	alignRightButton.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatLine(selection.start, selection.end, "align", "right")	
		}
	})

	alignJustifyButton.addEventListener("click", function(event){
		editor.focus()
		var selection = editor.getSelection()
		if (selection != null){
			editor.formatText(selection.start, selection.end+1, "align", "justify")	
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

	imageModalLinkInput.addEventListener("input", function(event){
		imageModalFileInput.disabled = true	
	})

	imageModalFileInput.addEventListener("change", function(event){
		imageModalLinkInput.disabled = true	
	})

	imageModal.element.addEventListener("positive-pressed", function(event){
		if (!imageModalLinkInput.disabled && imageModalLinkInput.value.length > 0) { 
			editor.focus()
			var selection = editor.getSelection()
			editor.insertEmbed(selection.end, "image", imageModalLinkInput.value)
		}
		else if (!imageModalFileInput.disabled && imageModalFileInput.value.length > 0) {
			event.preventDefault() //We're gonna need to do this on our own.
			var imageUploadRequest = new XMLHttpRequest()
			var formData = new FormData();
			formData.append("image", imageModalFileInput.files[0])
			imageUploadRequest.open("POST", "/upload_image")

			imageUploadRequest.onload =  function(){
				var data = JSON.parse(imageUploadRequest.responseText);
				if (data.error == 0) {
					editor.focus()
					var selection = editor.getSelection()
					editor.insertEmbed(selection.end, "image", data.url)
					imageModal.hide()	
				}
				imageUploadRequest = null
				//TODO: implement error handling
			}

			imageUploadRequest.send(formData)
			imageModalPositiveButton.classList.add("uploading")
			imageModalPositiveButton.disabled = true;
		}
	})

	imageModal.element.addEventListener("hide", function(event){
		imageModalLinkInput.disabled = false
		imageModalLinkInput.value = ""
		imageModalFileInput.disabled = false
		imageModalFileInput.value = null
		imageModalPositiveButton.classList.remove("uploading")
		imageModalPositiveButton.disabled = false;
		if (imageUploadRequest != null) {
			imageUploadRequest.abort()	
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

