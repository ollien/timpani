document.addEventListener("DOMContentLoaded",function(e){var t=document.getElementById("add-user-modal"),n=new Modal(t);n.positiveButton=n.element.querySelector("button.positive");var d=document.getElementById("add-user-button"),a=document.getElementById("users-list"),o=document.getElementById("username-input"),r=document.getElementById("full-name-input"),s=document.getElementById("password-input"),i=(document.getElementById("confirm-password-input"),document.getElementById("can-change-settings-checkbox")),u=document.getElementById("can-write-posts-checkbox");d.addEventListener("click",function(e){n.show()}),n.element.addEventListener("positive-pressed",function(e){e.preventDefault(),n.positiveButton.classList.add("working");var t=new FormData;t.append(o.getAttribute("name"),o.value),t.append(r.getAttribute("name"),r.value),t.append(s.getAttribute("name"),s.value),i.checked&&t.append(i.getAttribute("name"),"on"),u.chceked&&t.append(u.getAttribute("name"),"on");var d=new XMLHttpRequest;d.open("POST","/create_user"),d.addEventListener("load",function(e){var t=JSON.parse(d.responseText);if(n.positiveButton.classList.remove("working"),0===t.error){var r=t.user_id,s=document.createElement("li");s.setAttribute("user_id",r),s.classList.add("user");var i=document.createElement("span");i.classList.add("usenrame"),i.textContent=o.value,s.appendChild(i),a.appendChild(s),n.hide()}else 1===t.error?window.location="/login":2===t.error}),d.send(t)})});