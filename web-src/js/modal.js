/*jshint eqnull: true, eqeqeq: true, expr: true*/

function Modal(element, config) {
	this.overlay = document.createElement("div");
	this.overlay.classList.add("modal-overlay");
	this.overlay.addEventListener("transitionend", function(event) {
		this.parentNode.removeChild(this);
	});
	this.zIndex = -1;

	if (config == null) {
		this.config = { keyboard: true };
	}
	else {
		this.config = config;
	}


	if (element instanceof HTMLElement) {
		this.element = element;
	}
	else {
		this.element = document.querySelector(element);
		if (this.element == null) {
			throw new Error("element does not exist.");
		}
		else if (!this.element.classList.contains("modal")) {
			throw new Error("element must have class modal");
		}
	}

	buttonsEl = this.element.querySelector(".modal-buttons");

	if (buttonsEl != null) {
		buttons = Array.prototype.slice.call(buttonsEl.childNodes);
		var _this = this;
		document.addEventListener("keyup", function(event) {
			if (_this.config.keyboard) {
				if (event.keyCode === 27 && _this.element.classList.contains("active")) {
					//IE Proofing
					event.preventDefault ? event.preventDefault() : (event.returnValue = false);
					_this.hide();
				}
			}
		});
		buttons.forEach(function(button) {
			//Checks if the button is actually an element.
			if (button.nodeType === 1) {
				if (button.classList.contains("positive")) {
					document.addEventListener("keyup", function(event) {
						if (_this.config.keyboard) {
							console.log(event.keyCode);
							console.log(_this.element.classList.contains("active"));
							console.log(_this.zIndex);
							console.log(Modal.highestZIndex);
							if (event.keyCode === 13 && _this.element.classList.contains("active") && _this.zIndex === Modal.highestZIndex) {
								//Enter
								//IE Proofing
								event.preventDefault ? event.preventDefault() : (event.returnValue = false);
								event.stopImmediatePropagation();
								button.click();
							}
						}
					});
				}

				button.addEventListener("click", function(event) {
					var mainEvent = null;
					var secondaryEvent = null;

					try {
						mainEvent = new Event("pressed", { cancelable: true });
					}
					//Legacy support for IE and the likes
					catch (e) {
						mainEvent = document.createEvent("event");
						mainEvent.initEvent("pressed", false, true);
					}

					mainEvent.el = this;

					if (this.classList.contains("positive")) {
						try {
							secondaryEvent = new Event("positive-pressed", { cancelable: true });
						}
						//Legacy support for IE and the likes
						catch (e) {
							mainEvent = document.createEvent("event");
							mainEvent.initEvent("positive-pressed", false, true);
						}
					}
					else if (this.classList.contains("negative")) {
						secondaryEvent = new Event("negative-pressed", { cancelable: true });
						try {
							secondaryEvent = new Event("negative-pressed", { cancelable: true });
						}
						//Legacy support for IE and the likes
						catch (e) {
							mainEvent = document.createEvent("event");
							mainEvent.initEvent("negative-pressed", false, true);
						}
					}

					_this.element.dispatchEvent(mainEvent);

					if (secondaryEvent !== null) {
						secondaryEvent.el = this;
						_this.element.dispatchEvent(secondaryEvent);
					}
					//event.returnValue is IE Proofing
					if (!((mainEvent.defaultPrevented || !mainEvent.returnValue) || (secondaryEvent != null && (secondaryEvent.defaultPrevented || !secondaryEvent.returnValue)))) {
						_this.hide();
					}
				});
			}
		});
	}
}

Modal.prototype.show = function() {
	var event = null;
	try {
		event = new Event("show", { cancelable: true });
	}
	catch (e) {
		//Legacy support for IE and the likes.
		event = document.createEvent("event");
		event.initEvent("show", false, true);
	}

	this.element.dispatchEvent(event);
	//event.returnValue is IE Proofing
	if (!event.defaultPrevented || event.returnValue) {
		if (!this.element.classList.contains("active")) {
			this.overlay.style.zIndex = Modal.highestZIndex;
			this.element.style.zIndex = Modal.highestZIndex + 1;
			Modal.highestZIndex += 2;
			this.zIndex = Modal.highestZIndex;
		}
		this.element.classList.add("active");
		document.body.appendChild(this.overlay);
		this.overlay.classList.add("active");
	}
};

Modal.prototype.hide = function() {
	var event = null;
	try {
		event = new Event("hide", { cancelable: true });
	}

	catch (e){
		event = document.createEvent("event");
		event.initEvent("hide", false, true);
	}

	this.element.dispatchEvent(event);
	//event.returnValue is IE Proofing
	if (!event.defaultPrevented || event.returnValue) {
		if (this.element.classList.contains("active")) {
			this.overlay.style.zIndex = "";
			this.element.style.zIndex = "";
			Modal.highestZIndex -= 2;
		}
		this.element.classList.remove("active");
		var count = 0;
		this.overlay.classList.remove("active");
	}
};

Modal.prototype.toggle = function() {
	if (this.element.classList.contains("active")) {
		this.hide();
	}
	else {
		this.show();
	}
};

Modal.prototype.addEventListener = function() {
	this.element.addEventListener.apply(this, arguments);
};

//Stores the highest ZIndex of any modal. -1 indicates that there is no active modal.
Modal.highestZIndex = 0;
