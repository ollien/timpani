var PASSWORDS_DO_NOT_MATCH="Passwords do not match.";document.addEventListener("DOMContentLoaded",function(e){function t(e){e.addEventListener("click",function(e){d.show();var t=this.parentNode.getAttribute("user_id"),n=new XMLHttpRequest;n.open("GET","/get_user_info/"+t),n.addEventListener("load",function(e){var t=JSON.parse(n.responseText);0===t.error?(w.textContent=t.info.username,L.textContent=t.info.full_name,0===t.info.permissions.length?(I.style.display="",B.style.display="none"):(I.style.display="none",B.style.display="",C.style.display=t.info.permissions.indexOf("can_write_posts")>-1?"":"none",_.style.display=t.info.permissions.indexOf("can_change_settings")>-1?"":"none")):1===t.error&&(window.location="/login")}),n.send()})}var n=document.getElementById("add-user-modal"),s=document.getElementById("user-info-modal"),o=document.getElementById("change-password-modal");console.log(o),console.log(o instanceof HTMLElement);var i=new Modal(n);i.positiveButton=i.element.querySelector("button.positive");var d=new Modal(s);d.positiveButton=i.element.querySelector("button.positive");var a=new Modal(o),l=document.getElementById("add-user-button"),r=document.getElementById("users-list"),u=document.getElementById("create-user-form"),c=u.querySelector("button"),m=Array.prototype.slice.call(document.querySelectorAll(".user-info-button")),p=document.getElementById("change-password-button"),y=document.getElementById("username-input"),v=document.getElementById("full-name-input"),g=document.getElementById("password-input"),f=document.getElementById("confirm-password-input"),E=document.getElementById("can-change-settings-checkbox"),h=document.getElementById("can-write-posts-checkbox"),w=document.getElementById("username-display"),L=document.getElementById("full-name-display"),B=document.getElementById("permission-info"),C=document.getElementById("can-change-settings"),_=document.getElementById("can-write-posts"),I=document.getElementById("no-permissions");l.addEventListener("click",function(e){i.show()}),u.addEventListener("submit",function(e){i.positiveButton.classList.add("working"),e.preventDefault(),u.checkValidity();var n=new FormData;n.append(y.getAttribute("name"),y.value),n.append(v.getAttribute("name"),v.value),n.append(g.getAttribute("name"),g.value),E.checked&&n.append(E.getAttribute("name"),"on"),h.checked&&n.append(h.getAttribute("name"),"on");var s=new XMLHttpRequest;s.open("POST","/create_user"),s.addEventListener("load",function(e){var n=JSON.parse(s.responseText);if(i.positiveButton.classList.remove("working"),0===n.error){var o=n.user_id,d=document.createElement("li");d.setAttribute("user_id",o),d.classList.add("user");var a=document.createElement("span");a.classList.add("username"),a.textContent=y.value,d.appendChild(a);var l=document.createElement("span");l.classList.add("user-info-button"),l.classList.add("fa"),l.classList.add("fa-info-circle"),console.log(m),m.push(l),t(l),d.appendChild(l),d.style.opacity=0,r.appendChild(d);window.getComputedStyle(d).opacity;d.style.opacity=1,i.hide()}else 1===n.error?window.location="/login":2===n.error&&(y.setCustomValidity("Username already in use!"),c.click())}),s.send(n)}),y.addEventListener("input",function(e){this.setCustomValidity("")}),g.addEventListener("input",function(e){this.setCustomValidity(""),this.value!==f.value&&this.setCustomValidity(PASSWORDS_DO_NOT_MATCH)}),f.addEventListener("input",function(e){g.setCustomValidity(""),g.value!==this.value&&g.setCustomValidity(PASSWORDS_DO_NOT_MATCH)}),i.element.addEventListener("positive-pressed",function(e){e.preventDefault(),c.click()}),i.element.addEventListener("hide",function(e){u.reset(),g.setCustomValidity(""),f.setCustomValidity(""),y.setCustomValidity("")}),m.forEach(t),p.addEventListener("click",function(e){a.show()}),a.element.addEventListener("positive-pressed",function(e){})});