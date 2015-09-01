function Modal(element) {
	if (element instanceof HTMLElement) {
		this.element = element	
	}
	else{
		this.element = document.querySelector(element)	
		if (this.element == null) {
			throw new Error("element does not exist.")	
		}
		else if (!this.element.classList.contains("modal")) {
			throw new Error("element must have class modal")	
		}
	}
}

Modal.prototype.show = function() {
	this.element.classList.add("active")
}

Modal.prototype.hide = function() {
	this.element.classList.remove("active")
}

Modal.prototype.toggle = function() {
	if (this.element.classList.contains("active")) {
		this.element.classList.remove("active")
	}
	else {
		this.element.classList.add("active")	
	}
}
