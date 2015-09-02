document.addEventListener("DOMContentLoaded", function(event){
	var modalElement = document.querySelector(".modal")
	var modal = new Modal(modalElement)
	modal.element.addEventListener("positive-pressed", function(event){
		var postId = modal.element.getAttribute("post-id")
		var request = new XMLHttpRequest();
		request.open("POST", "/delete_post/"+postId)
		request.addEventListener("load", function(event){
			var res = JSON.parse(request.responseText)
			if (res.error === 0){
				var li = document.querySelector("li[post-id=\""+postId+"\"]")		
				console.log(li);
				li.addEventListener("transitionend", function(event){
					this.remove()
				})
				li.classList.add("deleting")
			}
			else if (res.error === 1) {
				window.location = "/login"
			}
		})
		request.send();
	})

	var deleteButtons = document.querySelectorAll("span.button.delete")
	var deletePostTitle = document.querySelector("span.delete-post-title")
	Array.prototype.slice.call(deleteButtons).forEach(function(button){
		button.addEventListener("click", function(event){
			var li = button.parentNode.parentNode;
			var title = li.querySelector("a.post-title").textContent
			modalElement.setAttribute("post-id", li.getAttribute("post-id"))
			deletePostTitle.textContent = title
			modal.show();
		})	
	})
})
