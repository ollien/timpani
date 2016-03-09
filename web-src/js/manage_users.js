/*jshint eqnull: true, eqeqeq: true */

document.addEventListener("DOMContentLoaded", function(event) {
	var addUserModalElement = document.getElementById("add-user-modal");
	var addUserModal = new Modal(addUserModalElement);
	addUserModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var addUserButton = document.getElementById("add-user-button");
	var usersList = document.getElementById("users-list");
	//Inputs for add user modal
	var usernameInput = document.getElementById("username-input");
	var fullNameInput = document.getElementById("full-name-input");
	var passwordInput = document.getElementById("password-input");
	var confirmPasswordInput = document.getElementById("confirm-password-input");
	var canChangeSettingsCheckbox = document.getElementById("can-change-settings-checkbox");
	var canWritePostsCheckbox = document.getElementById("can-write-posts-checkbox");


	addUserButton.addEventListener("click", function(event) {
		addUserModal.show();
	});

	addUserModal.element.addEventListener("positive-pressed", function(event) {
		event.preventDefault();
		addUserModal.positiveButton.classList.add("working");
		var formData = new FormData();
		formData.append(usernameInput.getAttribute("name"), usernameInput.value);
		formData.append(fullNameInput.getAttribute("name"), fullNameInput.value);
		formData.append(passwordInput.getAttribute("name"), passwordInput.value);
		if (canChangeSettingsCheckbox.checked) {
			formData.append(canChangeSettingsCheckbox.getAttribute("name"), "on");
		}
		if (canWritePostsCheckbox.chceked) { 
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
				usernameSpan.classList.add("usenrame");
				usernameSpan.textContent = usernameInput.value;
				li.appendChild(usernameSpan);
				//TODO: Animate this
				usersList.appendChild(li);
				addUserModal.hide();
			}
			else if (res.error === 1) {
				window.location = "/login";
			}
			else if (res.error === 2){
				//TODO: Display error
			}
		});
		request.send(formData);
		
	});

	addUserModal.element.addEventListener("hide", function(event){
			usernameInput.value = "";
			fullNameInput.value = "";
			passwordInput = "";
			confirmPasswordInput = "";
			canChangeSettingsCheckbox = "";
			canWritePostsCheckbox = "";
	});

});
