var gulp = require("gulp");
var sass = require("gulp-sass");
var autoPrefixer = require("gulp-autoprefixer");
var minifyCss = require("gulp-minify-css");
var rename = require("gulp-rename");
var plumber = require("gulp-plumber");

gulp.task("default-theme", function(){
	return gulp.src("./themes/default/src.scss")
		.pipe(plumber())
		.pipe(sass().on("error", sass.logError))
		.pipe(autoPrefixer({
			browsers: [
				"last 2 versions",
				"IE 9"
			]
		}))
		.pipe(minifyCss())
		.pipe(rename("theme.css"))
		.pipe(gulp.dest("./themes/default"));
});
