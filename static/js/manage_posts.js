document.addEventListener("DOMContentLoaded", function(event){
	var modal = new Modal(".modal")
	modal.element.addEventListener("positive-pressed", function(event){
		alert("pressed");	
	})

	var deleteButtons = document.querySelectorAll("span.button.delete")
	var deletePostTitle = document.querySelector("span.delete-post-title")
	Array.prototype.slice.call(deleteButtons).forEach(function(button){
		button.addEventListener("click", function(event){
			var title = button.parentNode.parentNode.querySelector("span.post-title").textContent
			deletePostTitle.textContent = title
			modal.show();
		})	
	})
})
