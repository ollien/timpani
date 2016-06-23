function canLoadInsignia(){return null!=window.navigator&&!(navigator.userAgent.indexOf("MSIE")>-1&&navigator.userAgent.indexOf("MSIE 11")===-1&&navigator.userAgent.indexOf("Opera")===-1)}var INSIGNIA_OPTIONS={validate:function(e,t){return e.indexOf("#")===-1}};document.addEventListener("DOMContentLoaded",function(e){var t=document.getElementById("editor"),n=new Quill(t),i=ace.edit("code-editor"),l=document.getElementById("post-body"),d=document.getElementById("post-validity"),a=document.getElementById("tags-input"),o=document.getElementById("placeholder-tags-input"),u=canLoadInsignia()?insignia(a,INSIGNIA_OPTIONS):null,s=document.getElementById("post-form"),r=document.getElementById("add-link"),c=document.getElementById("add-image"),v=document.getElementById("add-quote"),m=document.getElementById("add-code"),g=document.getElementById("align-left"),p=document.getElementById("align-center"),f=document.getElementById("align-right"),I=document.getElementById("align-justify"),E=document.getElementById("link-modal");linkModal=new Modal(E),linkModal.input=document.getElementById("modal-link"),linkModal.errorDiv=linkModal.element.querySelector("div.modal-error"),linkModal.positiveButton=linkModal.element.querySelector("button.positive");var L=document.getElementById("image-modal"),k=new Modal(L);k.linkInput=document.getElementById("image-url"),k.fileInput=document.getElementById("image-upload"),k.uploadRequest=null,k.positiveButton=k.element.querySelector("button.positive"),k.errorDiv=k.element.querySelector("div.modal-error");var y=document.getElementById("code-modal"),b=new Modal(y,{keyboard:!1});b.selectLanguage=document.getElementById("select-language"),b.positiveButton=b.element.querySelector("button-positive"),d.setCustomValidity("Please fill out a post body."),n.addModule("toolbar",{container:"div#toolbar"}),n.addFormat("quote",{"class":"quote"}),n.addFormat("code",{"class":"language-"}),i.getSession().setUseWorker(!1),n.on("selection-change",function(e){null==e?(t.classList.remove("focused"),v.disabled=!0,m.disabled=!1):(t.classList.add("focused"),e.end-e.start>0?(v.disabled=!1,m.disabled=!0):(v.disabled=!0,m.disabled=!1))}),n.on("text-change",function(){var e=n.getSelection();null==e||e.end-e.start===0?(v.disabled=!0,m.disabled=!1):(v.disabled=!1,m.disabled=!0),n.getLength()<=1?d.setCustomValidity("Please fill out a post body."):d.setCustomValidity("")}),r.addEventListener("click",function(e){linkModal.show(),linkModal.input.focus()}),c.addEventListener("click",function(e){k.show()}),m.addEventListener("click",function(e){b.show()}),g.addEventListener("click",function(e){n.focus();var t=n.getSelection();null!=t&&n.formatLine(t.start,t.end,"align","left")}),p.addEventListener("click",function(e){n.focus();var t=n.getSelection();null!=t&&n.formatLine(t.start,t.end,"align","center")}),f.addEventListener("click",function(e){n.focus();var t=n.getSelection();null!=t&&n.formatLine(t.start,t.end,"align","right")}),I.addEventListener("click",function(e){n.focus();var t=n.getSelection();null!=t&&n.formatText(t.start,t.end+1,"align","justify")}),linkModal.element.addEventListener("show",function(e){linkModal.input.value="",linkModal.errorDiv.classList.remove("active")}),linkModal.element.addEventListener("positive-pressed",function(e){if(0===linkModal.input.value.trim().length)linkModal.errorDiv.classList.add("active"),e.preventDefault();else{n.focus();var t=n.getSelection();n.setSelection(null);var i=linkModal.input.value.trim();i.match(/^.+:\/\//)||(i="//"+i),t.end-t.start===0?n.insertText(t.start,linkModal.input.value,"link",i):n.formatText(t.start,t.end,"link",i)}}),linkModal.element.addEventListener("hide",function(e){linkModal.positiveButton.blur()}),k.element.addEventListener("show",function(e){k.linkInput.disabled=!1,k.linkInput.value="",k.fileInput.disabled=!1,k.fileInput.value=null,k.positiveButton.classList.remove("uploading"),k.positiveButton.disabled=!1,k.errorDiv.classList.remove("active")}),k.linkInput.addEventListener("input",function(e){k.fileInput.disabled=0!==k.linkInput.value.length}),k.fileInput.addEventListener("change",function(e){k.linkInput.disabled=!0}),k.element.addEventListener("positive-pressed",function(e){if(!k.linkInput.disabled&&k.linkInput.value.length>0){n.focus();var t=n.getSelection();n.insertEmbed(t.end,"image",k.linkInput.value)}else if(!k.fileInput.disabled&&k.fileInput.value.length>0){e.preventDefault(),k.uploadRequest=new XMLHttpRequest;var i=new FormData;i.append("image",k.fileInput.files[0]),k.uploadRequest.open("POST","/upload_image"),k.uploadRequest.onload=function(){var e=JSON.parse(k.uploadRequest.responseText);if(0===e.error){n.focus();var t=n.getSelection();n.insertEmbed(t.end,"image",e.url),k.hide()}else 2===e.error&&(k.errorDiv.textContent="Image must be a JPG, PNG, or GIF.",k.errorDiv.classList.add("active"),k.positiveButton.classList.remove("uploading"),k.positiveButton.disabled=!1);k.uploadRequest=null},k.uploadRequest.send(i),k.positiveButton.classList.add("uploading"),k.positiveButton.disabled=!0}}),k.element.addEventListener("hide",function(e){k.positiveButton.blur(),null!=k.uploadRequest&&k.uploadRequest.abort()}),b.element.addEventListener("show",function(e){n.setSelection(null),b.selectLanguage.selectedIndex="0",i.setValue(""),i.focus()}),b.selectLanguage.addEventListener("change",function(e){i.getSession().setMode("ace/mode/"+b.selectLanguage.value)}),b.element.addEventListener("positive-pressed",function(e){n.focus();var t=n.getSelection();n.setSelection(null);for(var l=i.getValue().split("\n"),d=0;d<l.length;d++)0===l[d].length&&(l[d]="  ");l=l.join("\n"),n.insertText(t.end,l,"code",b.selectLanguage.value)}),b.element.addEventListener("hide",function(e){b.positiveButton.blur(),i.getSession().setMode("ace/mode/plain_text")}),a.addEventListener("focus",function(e){var t=document.getElementById("tag-input-div");t.classList.add("focused")}),a.addEventListener("blur",function(e){var t=document.getElementById("tag-input-div");t.classList.remove("focused")}),s.addEventListener("submit",function(e){l.value=n.getHTML(),canLoadInsignia()?o.value=u.value():o.value=a.value})});