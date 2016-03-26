/*jshint eqnull: true, eqeqeq: true */

var PASSWORDS_DO_NOT_MATCH = "Passwords do not match.";

document.addEventListener("DOMContentLoaded", function(event) {
	var addUserModalElement = document.getElementById("add-user-modal");
	var addUserModal = new Modal(addUserModalElement);
	addUserModal.positiveButton = addUserModal.element.querySelector("button.positive");
	var addUserButton = document.getElementById("add-user-button");
	var usersList = document.getElementById("users-list");
	var createUserForm = document.getElementById("create-user-form");
	var fakeCreateSubmitButton = createUserForm.querySelector("button");
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

	createUserForm.addEventListener("invalid", function(event){
		console.log("invalid");
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
				usernameInput.setCustomValidity("Username already in use!");
				fakeCreateSubmitButton.click();
			}
		});
		request.send(formData);
	});
	
	usernameInput.setCustomValidity("input", function(event){
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

});
