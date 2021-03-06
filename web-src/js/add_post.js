/*jshint eqnull: true, eqeqeq: true */

var INSIGNIA_OPTIONS = {
	validate: function(value, tags){
		return value.indexOf("#") === -1;
	}
};

function canLoadInsignia() {
	if (window.navigator == null) {
		return false;
	}

	if (navigator.userAgent.indexOf("MSIE") > -1 && navigator.userAgent.indexOf("MSIE 11") === -1 && navigator.userAgent.indexOf("Opera") === -1) {
		return false;
	}

	return true;
}


document.addEventListener("DOMContentLoaded", function(event) {
	var editorDiv = document.getElementById("editor");
	var editor = new Quill(editorDiv);
	var codeEditor = ace.edit("code-editor");
	var postBodyInput = document.getElementById("post-body");
	var validityInput = document.getElementById("post-validity");
	var tagsInput = document.getElementById("tags-input");
	var placeholderTagsInput = document.getElementById("placeholder-tags-input");
	var tagsInputPlugin = canLoadInsignia() ? insignia(tagsInput, INSIGNIA_OPTIONS) : null;
	var form = document.getElementById("post-form");
	var linkButton = document.getElementById("add-link");
	var imageButton = document.getElementById("add-image");
	var quoteButton = document.getElementById("add-quote");
	var codeButton = document.getElementById("add-code");
	var alignLeftButton = document.getElementById("align-left");
	var alignCenterButton = document.getElementById("align-center");
	var alignRightButton = document.getElementById("align-right");
	var alignJustifyButton = document.getElementById("align-justify");
	var linkModalElement = document.getElementById("link-modal");
	var linkModal = new Modal(linkModalElement);
	linkModal.input = document.getElementById("modal-link");
	linkModal.errorDiv = linkModal.element.querySelector("div.modal-error");
	linkModal.positiveButton = linkModal.element.querySelector("button.positive");

	var imageModalElement = document.getElementById("image-modal");
	var imageModal = new Modal(imageModalElement);
	imageModal.linkInput = document.getElementById("image-url");
	imageModal.fileInput = document.getElementById("image-upload");
	imageModal.uploadRequest = null;
	imageModal.positiveButton = imageModal.element.querySelector("button.positive");
	imageModal.errorDiv = imageModal.element.querySelector("div.modal-error");

	var codeModalElement = document.getElementById("code-modal");
	var codeModal = new Modal(codeModalElement, {keyboard: false});
	codeModal.selectLanguage = document.getElementById("select-language");
	codeModal.positiveButton = codeModal.element.querySelector("button-positive");

	validityInput.setCustomValidity("Please fill out a post body.");
	editor.addModule("toolbar", { container: "div#toolbar" });
	editor.addFormat("quote", { "class": "quote" });
	editor.addFormat("code", { "class": "language-" });
	codeEditor.getSession().setUseWorker(false);

	function setPostValidity() {
		if (editor.getLength() <= 1) {
			validityInput.setCustomValidity("Please fill out a post body.");
		}
		else {
			validityInput.setCustomValidity("");
		}
	}

	//For use with event listeners for when the cancel button is pressed on a pending ajax request
	function cancelRequest(request, button) {
		request.abort();
		button.classList.remove("working");
		button.disabled = false;
	}

	setPostValidity();

	editor.on("selection-change", function(range) {
		if (range == null) {
			editorDiv.classList.remove("focused");
			quoteButton.disabled = true;
			codeButton.disabled = false;
		}
		else {
			editorDiv.classList.add("focused");
			if (range.end - range.start > 0) {
				quoteButton.disabled = false;
				codeButton.disabled = true;
			}
			else {
				quoteButton.disabled = true;
				codeButton.disabled = false;
			}
		}
	});

	editor.on("text-change", function() {
		var range = editor.getSelection();
		if (range == null || range.end - range.start === 0) {
			quoteButton.disabled = true;
			codeButton.disabled = false;
		}
		else {
			quoteButton.disabled = false;
			codeButton.disabled = true;
		}

		setPostValidity();
	});

	linkButton.addEventListener("click", function(event) {
		linkModal.show();
		linkModal.input.focus();
	});

	imageButton.addEventListener("click", function(event) {
		imageModal.show();
	});

	codeButton.addEventListener("click", function(event) {
		codeModal.show();
	});

	alignLeftButton.addEventListener("click", function(event) {
		editor.focus();
		var selection = editor.getSelection();
		if (selection != null) {
			editor.formatLine(selection.start, selection.end, "align", "left");
		}
	});

	alignCenterButton.addEventListener("click", function(event) {
		editor.focus();
		var selection = editor.getSelection();
		if (selection != null) {
			editor.formatLine(selection.start, selection.end, "align", "center");
		}
	});

	alignRightButton.addEventListener("click", function(event) {
		editor.focus();
		var selection = editor.getSelection();
		if (selection != null) {
			editor.formatLine(selection.start, selection.end, "align", "right");
		}
	});

	alignJustifyButton.addEventListener("click", function(event) {
		editor.focus();
		var selection = editor.getSelection();
		if (selection != null) {
			editor.formatText(selection.start, selection.end + 1, "align", "justify");
		}
	});

	linkModal.element.addEventListener("show", function(event) {
		linkModal.input.value = "";
		linkModal.errorDiv.classList.remove("active");
	});

	linkModal.element.addEventListener("positive-pressed", function(event) {
		if (linkModal.input.value.trim().length === 0) {
			linkModal.errorDiv.classList.add("active");
			event.preventDefault();
		}
		else {
			editor.focus();
			var selection = editor.getSelection();
			editor.setSelection(null);
			var link = linkModal.input.value.trim();
			if (!link.match(/^.+:\/\//)) {
				link = "//" + link;
			}

			//This basically indicates that we don"t actually have a selection.
			if (selection.end - selection.start === 0) {
				editor.insertText(selection.start, linkModal.input.value, "link", link);
			}
			else {
				editor.formatText(selection.start, selection.end, "link", link);
			}
		}
	});

	linkModal.element.addEventListener("hide", function(event) {
		linkModal.positiveButton.blur();
	});

	imageModal.element.addEventListener("show", function(event) {
		imageModal.linkInput.disabled = false;
		imageModal.linkInput.value = "";
		imageModal.fileInput.disabled = false;
		imageModal.fileInput.value = null;
		imageModal.positiveButton.classList.remove("working");
		imageModal.positiveButton.disabled = false;
		imageModal.errorDiv.classList.remove("active");
	});

	imageModal.linkInput.addEventListener("input", function(event) {
		imageModal.fileInput.disabled = imageModal.linkInput.value.length !== 0;
	});

	imageModal.fileInput.addEventListener("change", function(event) {
		imageModal.linkInput.disabled = true;
	});

	imageModal.element.addEventListener("positive-pressed", function(event) {
		if (!imageModal.linkInput.disabled && imageModal.linkInput.value.length > 0) {
			editor.focus();
			var selection = editor.getSelection();
			editor.insertEmbed(selection.end, "image", imageModal.linkInput.value);
		}
		else if (!imageModal.fileInput.disabled && imageModal.fileInput.value.length > 0) {
			event.preventDefault();
			//We"re gonna need to do this on our own.
			imageModal.uploadRequest = new XMLHttpRequest();
			var formData = new FormData();
			formData.append("image", imageModal.fileInput.files[0]);
			imageModal.uploadRequest.open("POST", "/upload_image");

			imageModal.uploadRequest.onload = function() {
				var data = JSON.parse(imageModal.uploadRequest.responseText);

				if (data.error === 0) {
					editor.focus();
					var selection = editor.getSelection();
					editor.insertEmbed(selection.end, "image", data.url);
					imageModal.hide();
				}
				else if (data.error === 2) {
					imageModal.errorDiv.textContent = "Image must be a JPG, PNG, or GIF.";
					imageModal.errorDiv.classList.add("active");
					imageModal.positiveButton.classList.remove("working");
					imageModal.positiveButton.disabled = false;
				}
				imageModal.uploadRequest = null;
			};

			this.addEventListener("neutral-pressed", function(event) {
				cancelRequest(imageModal.uploadRequest, imageModal.positiveButton);
			});

			imageModal.uploadRequest.send(formData);
			imageModal.positiveButton.classList.add("working");
			imageModal.positiveButton.disabled = true;
		}
	});

	imageModal.element.addEventListener("hide", function(event) {
		imageModal.positiveButton.blur();
		if (imageModal.uploadRequest != null) {
			imageModal.uploadRequest.abort();
		}
	});

	codeModal.element.addEventListener("show", function(event) {
		editor.setSelection(null);
		codeModal.selectLanguage.selectedIndex = "0";
		codeEditor.setValue("");
		codeEditor.focus();
	});

	codeModal.selectLanguage.addEventListener("change", function(event) {
		codeEditor.getSession().setMode("ace/mode/" + codeModal.selectLanguage.value);
	});

	codeModal.element.addEventListener("positive-pressed", function(event) {
		editor.focus();
		var selection = editor.getSelection();
		editor.setSelection(null);
		//Workaround to get blank lines to display
		var input = codeEditor.getValue().split("\n");
		for (var i = 0; i < input.length; i++) {
			if (input[i].length === 0) {
				input[i] = "  ";
			}
		}
		input = input.join("\n");
		editor.insertText(selection.end, input, "code", codeModal.selectLanguage.value);
	});

	codeModal.element.addEventListener("hide", function(event) {
		codeModal.positiveButton.blur();
		codeEditor.getSession().setMode("ace/mode/plain_text");
	});

	tagsInput.addEventListener("focus", function(event) {
		var div = document.getElementById("tag-input-div");
		div.classList.add("focused");
	});

	tagsInput.addEventListener("blur", function(event) {
		var div = document.getElementById("tag-input-div");
		div.classList.remove("focused");
	});

	form.addEventListener("submit", function(event) {
		postBodyInput.value = editor.getHTML();
		if (canLoadInsignia()) {
			placeholderTagsInput.value = tagsInputPlugin.value();
		}
		else {
			placeholderTagsInput.value = tagsInput.value;
		}
	});
});
