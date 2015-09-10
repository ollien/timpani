var gulp = require("gulp");
var sass = require("gulp-sass");
var autoPrefixer = require("gulp-autoprefixer");
var minifyCss = require("gulp-minify-css");
var jshint = require("gulp-jshint");
var stylishJshint = require("jshint-stylish");
var uglify = require("gulp-uglify");

var SASS_SRC = "./scss/*.scss";
var SASS_DEST = "./static/css";
var JS_SRC = "./js/*.js"
var JS_DEST = "./static/js"

gulp.task("sass", function () {
	return gulp.src(SASS_SRC).pipe(sass())
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
		.pipe(jshint())
		.pipe(jshint.reporter(stylishJshint))
		.pipe(jshint.reporter("fail"))
		.pipe(uglify())	
		.pipe(gulp.dest(JS_DEST));
})

gulp.task("watch", function () {
	//Watch Sass for changes.
	var sassWatch = gulp.watch(SASS_SRC, ["sass"]);
	sassWatch.on("change", function (event) {
		var change_type = event.type;
		change_type[0] = change_type[0].toUpperCase();
		console.log(change_type + " detected on " + event.path + ". Running sass.");
	});
});
