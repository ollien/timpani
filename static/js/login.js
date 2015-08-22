document.addEventListener("DOMContentLoaded", function(event){
	var form = document.getElementById("login-form")
	var usernameInput = document.getElementById("username-field")
	var passwordInput = document.getElementById("password-field")

	var addInvalid = function(event){
		this.classList.add("error")	
	}
	var resetInvalid = function(event){
		this.classList.remove("error")
	}

	usernameInput.addEventListener("invalid", addInvalid);
	passwordInput.addEventListener("invalid", addInvalid);
	usernameInput.addEventListener("input", resetInvalid);
	passwordInput.addEventListener("input", resetInvalid);
})
