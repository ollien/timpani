/*jshint eqnull: true */

document.addEventListener('DOMContentLoaded', function (event) {
		var editorDiv = document.getElementById('editor');
		var editor = new Quill(editorDiv);
		var codeEditor = ace.edit('code-editor');
		var postBodyInput = document.getElementById('post-body');
		var validityInput = document.getElementById('post-validity');
		var tagsInput = document.getElementById('tags-input');
		var placeholderTagsInput = document.getElementById('placeholder-tags-input');
		var tagsInputPlugin = insignia(tagsInput);
		var form = document.getElementById('post-form');
		var linkButton = document.getElementById('add-link');
		var imageButton = document.getElementById('add-image');
		var quoteButton = document.getElementById('add-quote');
		var codeButton = document.getElementById('add-code');
		var alignLeftButton = document.getElementById('align-left');
		var alignCenterButton = document.getElementById('align-center');
		var alignRightButton = document.getElementById('align-right');
		var alignJustifyButton = document.getElementById('align-justify');
		
		var linkModal = {
				element: document.getElementById('link-modal'),
				input: document.getElementById('modal-link'),
				init: function () {
						//We needt o access some objects within this obect upon initialization, so we use this function to do that.
						this.modal = new Modal(this.element);
						this.errorDiv = this.element.querySelector('div.modal-error');
						this.positiveButton = this.element.querySelector('button.positive');
						delete this.init;
						return this;
				}
		}.init();
		
		var imageModal = {
				element: document.getElementById('image-modal'),
				linkInput: document.getElementById('image-url'),
				fileInput: document.getElementById('image-upload'),
				uploadRequest: null,
				//This will be defined when an image is being uploaded. This is a global variable so it can be cancelled.
				init: function () {
						//We need to access some objects within this object upon initializaton, so we use this function to do that.
						this.modal = new Modal(this.element);
						this.positiveButton = this.element.querySelector('button.positive');
						this.errorDiv = this.element.querySelector('div.modal-error');
						delete this.init;
						return this;
				}
		}.init();
		
		var codeModal = {
				element: document.getElementById('code-modal'),
				selectLanguage: document.getElementById('select-language'),
				init: function () {
						//We need to access some objects within this object upon initializatoin, so we use this function to do that.
						this.modal = new Modal(this.element, { keyboard: false });
						this.positiveButton = this.element.querySelector('button.positive');
						delete this.init;
						return this;
				}
		}.init();
		
		editor.addModule('toolbar', { container: 'div#toolbar' });
		editor.addFormat('quote', { 'class': 'quote' });
		editor.addFormat('code', { 'class': 'language-' });
		codeEditor.getSession().setUseWorker(false);
		
		editor.on('selection-change', function (range) {
				if (range == null) {
						editorDiv.classList.remove('focused');
						quoteButton.disabled = true;
						codeButton.disabled = false;
				} 
				
				else {
						editorDiv.classList.add('focused');
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
		
		editor.on('text-change', function () {
				var range = editor.getSelection();
				if (range == null || range.end - range.start === 0) {
						quoteButton.disabled = true;
						codeButton.disabled = false;
				} 
				
				else {
						quoteButton.disabled = false;
						codeButton.disabled = true;
				}
		});
		
		linkButton.addEventListener('click', function (event) {
				linkModal.modal.show();
				linkModal.input.focus();
		});
		
		imageButton.addEventListener('click', function (event) {
				imageModal.modal.show();
		});
		
		codeButton.addEventListener('click', function (event) {
				codeModal.modal.show();
		});
		
		alignLeftButton.addEventListener('click', function (event) {
				editor.focus();
				var selection = editor.getSelection();
				if (selection != null) {
						editor.formatLine(selection.start, selection.end, 'align', 'left');
				}
		});
		
		alignCenterButton.addEventListener('click', function (event) {
				editor.focus();
				var selection = editor.getSelection();
				if (selection != null) {
						editor.formatLine(selection.start, selection.end, 'align', 'center');
				}
		});
		
		alignRightButton.addEventListener('click', function (event) {
				editor.focus();
				var selection = editor.getSelection();
				if (selection != null) {
						editor.formatLine(selection.start, selection.end, 'align', 'right');
				}
		});
		
		alignJustifyButton.addEventListener('click', function (event) {
				editor.focus();
				var selection = editor.getSelection();
				if (selection != null) {
						editor.formatText(selection.start, selection.end + 1, 'align', 'justify');
				}
		});
		
		linkModal.element.addEventListener('show', function (event) {
				linkModal.input.value = '';
				linkModal.errorDiv.classList.remove('active');
		});
		
		linkModal.element.addEventListener('positive-pressed', function (event) {
				if (linkModal.input.value.trim().length === 0) {
						linkModal.errorDiv.classList.add('active');
						event.preventDefault();
				} 
				
				else {
						editor.focus();
						var selection = editor.getSelection();
						editor.setSelection(null);
						var link = linkModal.input.value.trim();
						if (!link.match(/^.+:\/\//)) {
								link = '//' + link;
						}

						//This basically indicates that we don't actually have a selection.
						if (selection.end - selection.start === 0) {
								editor.insertText(selection.start, linkModal.input.value, 'link', link);
						} 
		
						else {
								editor.formatText(selection.start, selection.end, 'link', link);
						}
				}
		});
		
		linkModal.element.addEventListener('hide', function (event) {
				linkModal.positiveButton.blur();
		});
		
		imageModal.element.addEventListener('show', function (event) {
				imageModal.linkInput.disabled = false;
				imageModal.linkInput.value = '';
				imageModal.fileInput.disabled = false;
				imageModal.fileInput.value = null;
				imageModal.positiveButton.classList.remove('uploading');
				imageModal.positiveButton.disabled = false;
				imageModal.errorDiv.classList.remove('active');
		});
		
		imageModal.linkInput.addEventListener('input', function (event) {
				imageModal.fileInput.disabled = true;
		});
		
		imageModal.fileInput.addEventListener('change', function (event) {
				imageModal.linkInput.disabled = true;
		});
		
		imageModal.element.addEventListener('positive-pressed', function (event) {
				if (!imageModal.linkInput.disabled && imageModal.linkInput.value.length > 0) {
						editor.focus();
						var selection = editor.getSelection();
						editor.insertEmbed(selection.end, 'image', imageModal.linkInput.value);
				} 
				
				else if (!imageModal.fileInput.disabled && imageModal.fileInput.value.length > 0) {
						event.preventDefault();
						//We're gonna need to do this on our own.
						imageModal.uploadRequest = new XMLHttpRequest();
						var formData = new FormData();
						formData.append('image', imageModal.fileInput.files[0]);
						imageModal.uploadRequest.open('POST', '/upload_image');
						
						imageModal.uploadRequest.onload = function () {
								var data = JSON.parse(imageModal.uploadRequest.responseText);

								if (data.error === 0) {
										editor.focus();
										var selection = editor.getSelection();
										editor.insertEmbed(selection.end, 'image', data.url);
										imageModal.modal.hide();
								} 
								
								else if (data.error === 2) {
										imageModal.errorDiv.textContent = 'Image must be a JPG, PNG, or GIF.';
										imageModal.errorDiv.classList.add('active');
										imageModal.positiveButton.classList.remove('uploading');
										imageModal.positiveButton.disabled = false;
								}
								imageModal.uploadRequest = null;
						};

						imageModal.uploadRequest.send(formData);
						imageModal.positiveButton.classList.add('uploading');
						imageModal.positiveButton.disabled = true;
				}
		});
		
		imageModal.element.addEventListener('hide', function (event) {
				imageModal.positiveButton.blur();
				if (imageModal.uploadRequest != null) {
						imageModal.uploadRequest.abort();
				}
		});
		
		codeModal.element.addEventListener('show', function (event) {
				editor.setSelection(null);
				codeModal.selectLanguage.selectedIndex = '0';
				codeEditor.setValue('');
				codeEditor.focus();
		});
		
		codeModal.selectLanguage.addEventListener('change', function (event) {
				codeEditor.getSession().setMode('ace/mode/' + codeModal.selectLanguage.value);
		});
		
		codeModal.element.addEventListener('positive-pressed', function (event) {
				editor.focus();
				var selection = editor.getSelection();
				editor.setSelection(null);
				//Workaround to get blank lines to display
				var input = codeEditor.getValue().split('\n');
				for (var i = 0; i < input.length; i++) {
						if (input[i].length === 0) {
								input[i] = '  ';
						}
				}
				input = input.join('\n');
				editor.insertText(selection.end, input, 'code', codeModal.selectLanguage.value);
		});

		codeModal.element.addEventListener('hide', function (event) {
				codeModal.positiveButton.blur();
				codeEditor.getSession().setMode('ace/mode/plain_text');
		});

		tagsInput.addEventListener('focus', function (event) {
				var div = document.getElementById('tag-input-div');
				div.classList.add('focused');
		});

		tagsInput.addEventListener('blur', function (event) {
				var div = document.getElementById('tag-input-div');
				div.classList.remove('focused');
		});

		form.addEventListener('submit', function (event) {
				if (editor.getText().trim().length === 0) {
						validityInput.setCustomValidity('Please fill out a post body.');
						event.preventDefault();
				} 
				
				else {
						postBodyInput.value = editor.getHTML();
						placeholderTagsInput.value = tagsInputPlugin.value();
				}
		});
});
