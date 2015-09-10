var gulp = require("gulp")
var sass = require("gulp-sass")
var autoPrefixer = require("gulp-autoprefixer")
var minifyCss = require("gulp-minify-css")
var ugilfy = require("gulp-uglify")

gulp.task("sass", function(){
	return gulp.src("./scss/*.scss")
		.pipe(sass())
		.pipe(autoPrefixer({browsers: ["last 2 versions", "IE 9"]}))
		.pipe(minifyCss())
		.pipe(gulp.dest("./static/css/"))
})
