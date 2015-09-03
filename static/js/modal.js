function Modal(element) {
	this.overlay = document.createElement("div");
	this.overlay.classList.add("modal-overlay");
	this.overlay.style.zIndex = -1;

	if (element instanceof HTMLElement) {
		this.element = element	
	}

	else {
		this.element = document.querySelector(element)	
		if (this.element == null) {
			throw new Error("element does not exist.")	
		}
		else if (!this.element.classList.contains("modal")) {
			throw new Error("element must have class modal")	
		}
	}

	buttonsEl = this.element.querySelector(".modal-buttons")
	if (buttonsEl != null){
		buttons = Array.prototype.slice.call(buttonsEl.childNodes)
		var _this = this;
		buttons.forEach(function(button){
			button.addEventListener("click", function(event){
				var mainEvent = new Event("pressed")
				mainEvent.el = button
				if (button.classList.contains("positive")){
					var secondaryEvent = new Event("positive-pressed");
				}

				else if (button.classList.contains("negative")){
					var secondaryEvent = new Event("negative-pressed");
				}	
				
				_this.element.dispatchEvent(mainEvent)
				if (secondaryEvent != null){
					secondaryEvent.el = button;
					_this.element.dispatchEvent(secondaryEvent)
				}
				if (!mainEvent.defaultPrevented && (secondaryEvent != null && !secondaryEvent.defaultPrevented)){
					_this.hide()
				}
			})
		})
	}
	
}


Modal.prototype.show = function() {
	this.element.classList.add("active")
	document.body.appendChild(this.overlay);
	this.overlay.classList.add("active")
}

Modal.prototype.hide = function() {
	this.element.classList.remove("active")
	this.overlay.addEventListener("transitionend webkitTransitionEnd", function(event){
		this.remove()
	})
	this.overlay.classList.remove("active")
}

Modal.prototype.toggle = function() {
	if (this.element.classList.contains("active")) {
		this.hide();
	}
	else {
		this.show();
	}
}
