var gulp = require("gulp");
var sass = require("gulp-sass");
var autoPrefixer = require("gulp-autoprefixer");
var minifyCss = require("gulp-minify-css");
var ugilfy = require("gulp-uglify");

var SASS_SRC = "./scss/*.scss";
var SASS_DEST = "./static/css";

gulp.task("sass", function () {
	return gulp.src(SASS_SRC).pipe(sass())
		.pipe(autoPrefixer({
			browsers: [
				"last 2 versions",
				"IE 9"
			]
		}))
		.pipe(minifyCss()).pipe(gulp.dest(SASS_DEST));
});

gulp.task("watch", function () {
	//Watch Sass for changes.
	var sassWatch = gulp.watch(SASS_SRC, ["sass"]);
	sassWatch.on("change", function (event) {
		var change_type = event.type;
		change_type[0] = change_type[0].toUpperCase();
		console.log(change_type + " detected on " + event.path + ". Running sass.");
	});
});
