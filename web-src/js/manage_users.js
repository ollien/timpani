/*jshint eqnull: true, eqeqeq: true */

var PASSWORDS_DO_NOT_MATCH = "Passwords do not match.";

function addInfoButtonListener(button) {
	button.addEventListener("click", function(event){
		userInfoModal.show();
		var userId = this.parentNode.getAttribute("user_id");
		var request = new XMLHttpRequest();
		request.open("GET", "/get_user_info/" + userId);
		request.addEventListener("load", function(event){
			var res = JSON.parse(request.responseText);
			if (res.error === 0) {
				usernameDisplay.textContent = res.info.username;
				fullNameDisplay.textContent = res.info.full_name;
				if (res.info.permissions.length === 0) {
					noPermissions.style.display = "";
					permissionDisplayList.style.display = "none";
				}
				else {
					noPermissions.style.display = "none";
					permissionDisplayList.style.display = "";
					canChangeSettingsDisplay.style.display = res.info.permissions.indexOf("can_write_posts") > -1 ? "" : "none";
					canWritePostsDisplay.style.display = res.info.permissions.indexOf("can_change_settings") > -1 ? "" : "none";
				}
			}
			else if (res.error === 1){
				window.location = "/login";	
			}
		});
		request.send();
	});
}

document.addEventListener("DOMContentLoaded", function(event) {
	var addUserModalElement = document.getElementById("add-user-modal");
	var userInfoModalElement = document.getElementById("user-info-modal");
	var addUserModal = new Modal(addUserModalElement);
	addUserModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var userInfoModal = new Modal(userInfoModalElement);
	userInfoModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var addUserButton = document.getElementById("add-user-button");
	var usersList = document.getElementById("users-list");
	var createUserForm = document.getElementById("create-user-form");
	var fakeCreateSubmitButton = createUserForm.querySelector("button");
	var userInfoButtons = Array.prototype.slice.call(document.querySelectorAll(".user-info-button"));
	//Inputs for add user modal
	var usernameInput = document.getElementById("username-input");
	var fullNameInput = document.getElementById("full-name-input");
	var passwordInput = document.getElementById("password-input");
	var confirmPasswordInput = document.getElementById("confirm-password-input");
	var canChangeSettingsCheckbox = document.getElementById("can-change-settings-checkbox");
	var canWritePostsCheckbox = document.getElementById("can-write-posts-checkbox");
	//Spans for user info modal
	var usernameDisplay = document.getElementById("username-display");
	var fullNameDisplay = document.getElementById("full-name-display");
	var permissionDisplayList = document.getElementById("permission-info");
	var canChangeSettingsDisplay = document.getElementById("can-change-settings");
	var canWritePostsDisplay = document.getElementById("can-write-posts");
	var noPermissions = document.getElementById("no-permissions");


	addUserButton.addEventListener("click", function(event) {
		addUserModal.show();
	});

	createUserForm.addEventListener("submit", function(event) {
		addUserModal.positiveButton.classList.add("working");
		event.preventDefault();
		createUserForm.checkValidity();
		var formData = new FormData();
		formData.append(usernameInput.getAttribute("name"), usernameInput.value);
		formData.append(fullNameInput.getAttribute("name"), fullNameInput.value);
		formData.append(passwordInput.getAttribute("name"), passwordInput.value);
		if (canChangeSettingsCheckbox.checked) {
			formData.append(canChangeSettingsCheckbox.getAttribute("name"), "on");
		}
		if (canWritePostsCheckbox.checked) {
			formData.append(canWritePostsCheckbox.getAttribute("name"), "on");
		}
		var request = new XMLHttpRequest();
		request.open("POST", "/create_user");
		request.addEventListener("load", function(event) {
			var res = JSON.parse(request.responseText);
			addUserModal.positiveButton.classList.remove("working");
			if (res.error === 0) {
				var user_id = res.user_id;
				var li = document.createElement("li");
				li.setAttribute("user_id", user_id);
				li.classList.add("user");
				var usernameSpan = document.createElement("span");
				usernameSpan.classList.add("username");
				usernameSpan.textContent = usernameInput.value + "\n";
				li.appendChild(usernameSpan);
				var infoButton = document.createElement("span");
				infoButton.classList.add("user-info-button");
				infoButton.classList.add("fa");
				infoButton.classList.add("fa-info-circle");
				console.log(userInfoButtons);
				userInfoButtons.push(infoButton);
				addInfoButtonListener(infoButton);
				li.appendChild(infoButton);
				li.style.opacity = 0;
				usersList.appendChild(li);
				//Fixes race condition where element wouldn't fade
				//Needs to be set to a variable so jshint doesn't complain about an expression.
				var opacity = window.getComputedStyle(li).opacity;
				li.style.opacity = 1;
				addUserModal.hide();
			}
			else if (res.error === 1) {
				window.location = "/login";
			}
			else if (res.error === 2){
				usernameInput.setCustomValidity("Username already in use!");
				fakeCreateSubmitButton.click();
			}
		});
		request.send(formData);
	});
	
	usernameInput.addEventListener("input", function(event){
		this.setCustomValidity("");	
	});

	passwordInput.addEventListener("input", function(event){
		this.setCustomValidity("");
		if (this.value !== confirmPasswordInput.value) {
			this.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	confirmPasswordInput.addEventListener("input", function(event){
		passwordInput.setCustomValidity("");
		if (passwordInput.value !== this.value){
			passwordInput.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	addUserModal.element.addEventListener("positive-pressed", function(event) {
		event.preventDefault();
		//Through I would normally use createUserForm.submit(), this doesn't fire the "submit" event.
		fakeCreateSubmitButton.click();
	});

	addUserModal.element.addEventListener("hide", function(event){
		createUserForm.reset();
		passwordInput.setCustomValidity("");
		confirmPasswordInput.setCustomValidity("");
		usernameInput.setCustomValidity("");
	});

	userInfoButtons.forEach(addInfoButtonListener);
});
