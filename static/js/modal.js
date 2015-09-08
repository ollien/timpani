function Modal(element, config) {
	this.overlay = document.createElement("div")
	this.overlay.classList.add("modal-overlay")

	if (config == null) {
		this.config = {keyboard: true}	
	}

	else {
		this.config = config	
	}

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


	if (this.overlay.style.zIndex === undefined || this.overlay.style.zIndex === ""){
		this.overlay.style.zIndex = 0
	}

	this.element.style.zIndex = this.overlay.style.zIndex + 1

	buttonsEl = this.element.querySelector(".modal-buttons")
	if (buttonsEl != null){
		buttons = Array.prototype.slice.call(buttonsEl.childNodes)
		var _this = this

		document.addEventListener("keyup", function(event){
			if (_this.config.keyboard){
				if (event.keyCode == 27) {
					event.preventDefault()	
					_this.hide()
				}
			}
		})
		buttons.forEach(function(button){
			//Checks if the button is actually an element.
			if (button.nodeType == 1){
				if (button.classList.contains("positive")){
					document.addEventListener("keyup", function(event){
						if (_this.config.keyboard){
							if (event.keyCode == 13){ //Enter
								event.preventDefault()
								button.click()
							}
						}
					})
				}

				button.addEventListener("click", function(event){
					var mainEvent = new Event("pressed", {cancelable: true})
					mainEvent.el = this
					if (this.classList.contains("positive")){
						var secondaryEvent = new Event("positive-pressed", {cancelable: true})
					}

					else if (this.classList.contains("negative")){
						var secondaryEvent = new Event("negative-pressed", {cancelable: true})
					}	
					
					_this.element.dispatchEvent(mainEvent)

					if (secondaryEvent != null){
						secondaryEvent.el = this
						_this.element.dispatchEvent(secondaryEvent)
					}

					if (!(mainEvent.defaultPrevented || (secondaryEvent != null && secondaryEvent.defaultPrevented))){
						_this.hide()
					}
				})
			}
		})
	}
}


Modal.prototype.show = function() {
	var event = new Event("show", {cancelable: true})
	this.element.dispatchEvent(event)
	if (!event.defaultPrevented){
		this.element.classList.add("active")
		document.body.appendChild(this.overlay)
		this.overlay.classList.add("active")
	}
}

Modal.prototype.hide = function() {
	var event = new Event("hide", {cancelable: true})	
	this.element.dispatchEvent(event)
	if (!event.defaultPrevented){
		this.element.classList.remove("active")
		this.overlay.addEventListener("transitionend", function(event){
			this.remove()
		})
		this.overlay.classList.remove("active")
	}
}

Modal.prototype.toggle = function() {
	if (this.element.classList.contains("active")) {
		this.hide()
	}
	else {
		this.show()
	}
}

Modal.prototype.addEventListener = function(){
	this.element.addEventListener.apply(this, arguments)
}

