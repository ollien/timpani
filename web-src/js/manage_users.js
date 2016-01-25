/*jshint eqnull: true, eqeqeq: true */

document.addEventListener("DOMContentLoaded", function(event) {
	var addUserModalElement = document.getElementById("add-user-modal");
	var addUserModal = new Modal(addUserModalElement);
	var addUserButton = document.getElementById("add-user-button");

	addUserButton.addEventListener("click", function(event){
		addUserModal.show();	
	});


});
