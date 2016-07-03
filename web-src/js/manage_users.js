/*jshint eqnull: true, eqeqeq: true, expr: true*/

var PASSWORDS_DO_NOT_MATCH = "Passwords do not match.";

document.addEventListener("DOMContentLoaded", function(event) {
	var addUserModalElement = document.getElementById("add-user-modal");
	var userInfoModalElement = document.getElementById("user-info-modal");
	var changePasswordModalElement = document.getElementById("change-password-modal");
	var editPermissionsModalElement = document.getElementById("edit-permissions-modal");
	var addUserModal = new Modal(addUserModalElement);
	addUserModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var userInfoModal = new Modal(userInfoModalElement);
	userInfoModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var changePasswordModal = new Modal(changePasswordModalElement);
	changePasswordModal.positiveButton = changePasswordModal.element.querySelector("button.positive");
	var editPermissionsModal = new Modal(editPermissionsModalElement);
	editPermissionsModal.positiveButton = editPermissionsModal.element.querySelector("button.positive");
	var addUserButton = document.getElementById("add-user-button");
	var usersList = document.getElementById("users-list");
	var createUserForm = document.getElementById("create-user-form");
	var fakeCreateSubmitButton = createUserForm.querySelector("button");
	var userInfoButtons = Array.prototype.slice.call(document.querySelectorAll(".user-info-button"));
	var changePasswordButton = document.getElementById("change-password-button");
	var editPermissionsButton = document.getElementById("edit-permissions-button");
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
	//Stores the current user id. If -1, no user's modal is currently open.
	var currentUserId = -1;
	//Inputs for reset password modal
	var newPasswordInput = document.getElementById("reset-password-input");
	var confirmNewPasswordInput = document.getElementById("confirm-password-reset-input");
	var resetPasswordForm = document.getElementById("change-password-form");
	var fakeResetSubmitButton = resetPasswordForm.querySelector("button");
	//Inputs for edit permissions modal
	var canChangeSettingsEditCheckbox = document.getElementById("can-change-settings-edit-checkbox");
	var canWritePostsEditCheckbox = document.getElementById("can-write-posts-edit-checkbox");

	function addInfoButtonListener(button) {
		button.addEventListener("click", function(event) {
			userInfoModal.show();
			currentUserId = this.parentNode.getAttribute("user_id");
			var request = new XMLHttpRequest();
			request.open("GET", "/get_user_info/" + currentUserId);
			request.addEventListener("load", function(event) {
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
				else if (res.error === 1) {
					window.location = "/login";
				}
			});
			request.send();
		});
	}

	//For use with event listeners for when the cancel button is pressed on a pending ajax request
	function cancelRequest(request, button) {
		request.abort();
		button.classList.remove("working");
		button.disabled = false;
	}

	//Returns the appropriate element to insert before in order to preserve alphabetical order
	//Returns null if there is no element. appendChild should be used in these cases.
	function getInsertBeforeUsername(username) {
		userElements = usersList.querySelectorAll("li.user");
		for (var i = 0; i < userElements.length; i++) {
			if (userElements[i].querySelector("span.username").textContent.toLowerCase() > username.toLowerCase()) {
				return userElements[i];
			}
		}
		return null;
	}

	addUserButton.addEventListener("click", function(event) {
		addUserModal.show();
	});

	createUserForm.addEventListener("submit", function(event) {
		addUserModal.positiveButton.classList.add("working");
		addUserModal.positiveButton.disabled = true;
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
			addUserModal.positiveButton.disabled = false;
			if (res.error === 0) {
				var user_id = res.user_id;
				var li = document.createElement("li");
				li.setAttribute("user_id", user_id);
				li.classList.add("user");
				var usernameSpan = document.createElement("span");
				usernameSpan.classList.add("username");
				usernameSpan.textContent = usernameInput.value;
				li.appendChild(usernameSpan);
				var infoButton = document.createElement("span");
				infoButton.classList.add("user-info-button");
				infoButton.classList.add("fa");
				infoButton.classList.add("fa-info-circle");
				userInfoButtons.push(infoButton);
				addInfoButtonListener(infoButton);
				li.appendChild(infoButton);
				li.style.opacity = 0;
				li.style.height = "0px";
				var before = getInsertBeforeUsername(usernameInput.value);
				if (before === null) {
					usersList.appendChild(li);
				}
				else {
					usersList.insertBefore(li, before);
				}
				//Fixes race condition where element wouldn't fade
				window.getComputedStyle(li).opacity;
				window.getComputedStyle(li).height;
				li.style.opacity = 1;
				li.style.height = "";
				addUserModal.hide();
			}
			else if (res.error === 1) {
				window.location = "/login";
			}
			else if (res.error === 2) {
				usernameInput.setCustomValidity("Username already in use!");
				fakeCreateSubmitButton.click();
			}
		});

		addUserModal.element.addEventListener("neutral-pressed", function(event) {
			cancelRequest(request, addUserModal.positiveButton);
		});

		request.send(formData);
	});

	usernameInput.addEventListener("input", function(event) {
		this.setCustomValidity("");
	});

	passwordInput.addEventListener("input", function(event) {
		this.setCustomValidity("");
		if (this.value !== confirmPasswordInput.value) {
			this.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	confirmPasswordInput.addEventListener("input", function(event) {
		passwordInput.setCustomValidity("");
		if (passwordInput.value !== this.value) {
			passwordInput.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	addUserModal.element.addEventListener("positive-pressed", function(event) {
		event.preventDefault();
		//Through I would normally use createUserForm.submit(), this doesn't fire the "submit" event.
		fakeCreateSubmitButton.click();
	});

	addUserModal.element.addEventListener("hide", function(event) {
		createUserForm.reset();
		passwordInput.setCustomValidity("");
		confirmPasswordInput.setCustomValidity("");
		usernameInput.setCustomValidity("");
	});

	userInfoButtons.forEach(addInfoButtonListener);

	changePasswordButton.addEventListener("click", function(event) {
		changePasswordModal.show();
	});

	resetPasswordForm.addEventListener("submit", function(event) {
		changePasswordModal.positiveButton.classList.add("working");
		addUserModal.positiveButton.disabled = true;
		event.preventDefault();
		createUserForm.checkValidity();
		var formData = new FormData();
		formData.append("userId", currentUserId);
		formData.append(newPasswordInput.getAttribute("name"), newPasswordInput.value);
		var request = new XMLHttpRequest();
		request.open("POST", "/reset_password", true);
		request.addEventListener("load", function(event) {
			changePasswordModal.positiveButton.classList.add("working");
			addUserModal.positiveButton.disabled = false;
			var res = JSON.parse(request.responseText);
			if (res.error === 0) {
				changePasswordModal.hide();
			}
			else {
				window.location = "/login";
			}
		});

		addUserModal.element.addEventListener("neutral-pressed", function(event) {
			cancelRequest(request, addUserModal.positiveButton);
		});

		request.send(formData);
	});

	newPasswordInput.addEventListener("input", function(event) {
		newPasswordInput.setCustomValidity("");
		if (this.value !== confirmNewPasswordInput.value) {
			newPasswordInput.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	confirmNewPasswordInput.addEventListener("input", function(event) {
		newPasswordInput.setCustomValidity("");
		if (this.value !== newPasswordInput.value) {
			newPasswordInput.setCustomValidity(PASSWORDS_DO_NOT_MATCH);
		}
	});

	changePasswordModal.element.addEventListener("positive-pressed", function(event) {
		event.preventDefault();
		//Through I would normally use createUserForm.submit(), this doesn't fire the "submit" event.
		fakeResetSubmitButton.click();
	});

	changePasswordModal.element.addEventListener("hide", function(event) {
		resetPasswordForm.reset();
		newPasswordInput.setCustomValidity("");
	});

	editPermissionsButton.addEventListener("click", function(event) {
		editPermissionsModal.show();
		var request = new XMLHttpRequest();
		request.open("GET", "/get_user_info/" + currentUserId, true);
		request.addEventListener("load", function(event) {
			var res = JSON.parse(request.responseText);
			canChangeSettingsEditCheckbox.checked = res.info.permissions.indexOf("can_change_settings") > -1;
			canWritePostsEditCheckbox.checked = res.info.permissions.indexOf("can_write_posts") > -1;
		});
		request.send();
	});

	editPermissionsModal.element.addEventListener("positive-pressed", function(event){
		editPermissionsModal.positiveButton.classList.add("working");
		addUserModal.positiveButton.disabled = true;
		event.preventDefault();
		var formData = new FormData();
		formData.append("userId", currentUserId);
		if (canChangeSettingsEditCheckbox.checked) {
			formData.append(canChangeSettingsCheckbox.getAttribute("name"), "on");
		}
		if (canWritePostsEditCheckbox.checked) {
			formData.append(canWritePostsCheckbox.getAttribute("name"), "on");
		}
		var request = new XMLHttpRequest();
		request.open("POST", "/change_user_permisisons", true);
		request.addEventListener("load", function(event) {
			editPermissionsModal.positiveButton.classList.remove("working");
			addUserModal.positiveButton.disabled = false;
			editPermissionsModal.hide();
		});

		addUserModal.element.addEventListener("neutral-pressed", function(event) {
			cancelRequest(request, addUserModal.positiveButton);
		});

		request.send(formData);
	});
});
