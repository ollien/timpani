var PASSWORDS_DO_NOT_MATCH="Passwords do not match.";document.addEventListener("DOMContentLoaded",function(e){var t=document.getElementById("add-user-modal"),n=new Modal(t);n.positiveButton=n.element.querySelector("button.positive");var i=document.getElementById("add-user-button"),d=document.getElementById("users-list"),s=document.getElementById("create-user-form"),a=s.querySelector("button"),o=document.getElementById("username-input"),u=document.getElementById("full-name-input"),r=document.getElementById("password-input"),l=document.getElementById("confirm-password-input"),c=document.getElementById("can-change-settings-checkbox"),m=document.getElementById("can-write-posts-checkbox");i.addEventListener("click",function(e){n.show()}),s.addEventListener("submit",function(e){n.positiveButton.classList.add("working"),e.preventDefault(),s.checkValidity();var t=new FormData;t.append(o.getAttribute("name"),o.value),t.append(u.getAttribute("name"),u.value),t.append(r.getAttribute("name"),r.value),c.checked&&t.append(c.getAttribute("name"),"on"),m.checked&&t.append(m.getAttribute("name"),"on");var i=new XMLHttpRequest;i.open("POST","/create_user"),i.addEventListener("load",function(e){var t=JSON.parse(i.responseText);if(n.positiveButton.classList.remove("working"),0===t.error){var s=t.user_id,u=document.createElement("li");u.setAttribute("user_id",s),u.classList.add("user");var r=document.createElement("span");r.classList.add("username"),r.textContent=o.value,u.appendChild(r),u.classList.add("fading"),d.appendChild(u),u.classList.remove("fading"),n.hide()}else 1===t.error?window.location="/login":2===t.error&&(o.setCustomValidity("Username already in use!"),a.click())}),i.send(t)}),o.addEventListener("input",function(e){this.setCustomValidity("")}),r.addEventListener("input",function(e){this.setCustomValidity(""),this.value!==l.value&&this.setCustomValidity(PASSWORDS_DO_NOT_MATCH)}),l.addEventListener("input",function(e){r.setCustomValidity(""),r.value!==this.value&&r.setCustomValidity(PASSWORDS_DO_NOT_MATCH)}),n.element.addEventListener("positive-pressed",function(e){e.preventDefault(),a.click()}),n.element.addEventListener("hide",function(e){s.reset(),r.setCustomValidity(""),l.setCustomValidity(""),o.setCustomValidity("")})});