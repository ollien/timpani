var gulp = require("gulp");
var sass = require("gulp-sass");
var autoPrefixer = require("gulp-autoprefixer");
var minifyCss = require("gulp-minify-css");
var jshint = require("gulp-jshint");
var stylishJshint = require("jshint-stylish");
var uglify = require("gulp-uglify");
var plumber = require("gulp-plumber");
var glob = require("glob");
var path = require("path");
var colors = require("colors");

var SASS_SRC = "./web-src/scss/*.scss";
var SASS_DEST = "./static/css";
var JS_SRC = "./web-src/js/*.js";
var JS_DEST = "./static/js";

//Search themes folder for theme gulpfiles
//This must be synchronus so it runs before gulp searches for tasks
files = glob("themes/*/*(gulpfile|gulp|build).js", {sync: true});
files.forEach(function(file){
	require(path.resolve(file)); //We don't have to store this, beacuse we just need its code to execute.
});

function customErrorHandler(error) {
	console.log("\u0007");
	console.log("Error".red + " details:");
	console.log(error.stack);
}

gulp.task("sass", function() {
	return gulp.src(SASS_SRC)
		.pipe(plumber({
			errorHandler: customErrorHandler	
		}))
		.pipe(sass().on("error", sass.logError))
		.pipe(autoPrefixer({
			browsers: [
				"last 2 versions",
				"IE 9"
			]
		}))
		.pipe(minifyCss())
		.pipe(gulp.dest(SASS_DEST));
});

gulp.task("js", function() {
	return gulp.src(JS_SRC)
		.pipe(plumber({
			errorHandler: customErrorHandler 
		}))
		.pipe(jshint())
		.pipe(jshint.reporter(stylishJshint))
		.pipe(jshint.reporter("fail"))
		.pipe(uglify())	
		.pipe(gulp.dest(JS_DEST));
});


gulp.task("watch", function() {
	//Watch Sass for changes.
	var sassWatch = gulp.watch(SASS_SRC, ["sass"]);
	sassWatch.on("change", function (event) {
		console.log("Event '"+ event.type + "' detected on " + event.path + ". Running sass.");
	});

	//Watch JS for changes.
	var jsWatch = gulp.watch(JS_SRC, ["js"]);
	jsWatch.on("change", function(event) {
		console.log("Event '"+ event.type + "' detected on " + event.path + ". Running js.");
	});
});
