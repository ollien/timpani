/*jshint eqnull: true, eqeqeq: true */

document.addEventListener("DOMContentLoaded", function(event) {
	var modalElement = document.getElementById("delete-modal");
	var modal = new Modal(modalElement);
	modal.positiveButton = modal.element.querySelector("button.positive");
	var deleteButtons = document.querySelectorAll("a.button.delete");
	var deletePostTitle = document.querySelector("span.delete-post-title");

	//For use with event listeners for when the cancel button is pressed on a pending ajax request
	function cancelRequest(request, button) {
		request.abort();
		button.classList.remove("working");
		button.disabled = false;
	}

	modal.element.addEventListener("positive-pressed", function(event) {
		event.preventDefault();
		var postId = modal.element.getAttribute("post-id");
		var request = new XMLHttpRequest();
		request.open("POST", "/delete_post/" + postId);

		request.addEventListener("load", function(event) {
			var res = JSON.parse(request.responseText);
			if (res.error === 0) {
				modal.positiveButton.classList.remove("working");
				modal.positiveButton.disabled = false;
				modal.hide();
				var li = document.querySelector("li[post-id=\"" + postId + "\"]");
				li.addEventListener("transitionend", function(event) {
					this.remove();
				});

				li.classList.add("deleting");
			}
			else if (res.error === 1) {
				window.location = "/login";
			}
		});
		modal.positiveButton.disabled = true;
		modal.positiveButton.classList.add("working");
		this.addEventListener("neutral-pressed", function(event) {
			cancelRequest(request, modal.positiveButton);
		});
		request.send();
	});

	Array.prototype.slice.call(deleteButtons).forEach(function(button) {
		button.addEventListener("click", function(event) {
			var li = button.parentNode.parentNode;
			var title = li.querySelector("a.post-title").textContent;
			modalElement.setAttribute("post-id", li.getAttribute("post-id"));
			deletePostTitle.textContent = title;
			modal.show();
		});
	});
});
