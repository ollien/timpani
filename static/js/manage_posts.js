document.addEventListener("DOMContentLoaded",function(e){function t(e,t){e.abort(),t.classList.remove("working"),t.disabled=!1}var n=document.getElementById("delete-modal"),o=new Modal(n);o.positiveButton=o.element.querySelector("button.positive");var i=document.querySelectorAll("a.button.delete"),s=document.querySelector("span.delete-post-title");o.element.addEventListener("positive-pressed",function(e){e.preventDefault();var n=o.element.getAttribute("post-id"),i=new XMLHttpRequest;i.open("POST","/delete_post/"+n),i.addEventListener("load",function(e){var t=JSON.parse(i.responseText);if(0===t.error){o.positiveButton.classList.remove("working"),o.positiveButton.disabled=!1,o.hide();var s=document.querySelector('li[post-id="'+n+'"]');s.addEventListener("transitionend",function(e){this.remove()}),s.classList.add("deleting")}else 1===t.error&&(window.location="/login")}),o.positiveButton.disabled=!0,o.positiveButton.classList.add("working"),this.addEventListener("neutral-pressed",function(e){t(i,o.positiveButton)}),i.send()}),Array.prototype.slice.call(i).forEach(function(e){e.addEventListener("click",function(t){var i=e.parentNode.parentNode,r=i.querySelector("a.post-title").textContent;n.setAttribute("post-id",i.getAttribute("post-id")),s.textContent=r,o.show()})})});