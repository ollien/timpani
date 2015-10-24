var gulp = require("gulp");
var sass = require("gulp-sass");
var autoPrefixer = require("gulp-autoprefixer");
var minifyCss = require("gulp-minify-css");
var jshint = require("gulp-jshint");
var stylishJshint = require("jshint-stylish");
var uglify = require("gulp-uglify");
var plumber = require("gulp-plumber")
var merge = require("merge-stream")

var SASS = [
	{
		src: "./web-src/scss/*.scss",
		dest: "./static/css"
	}
]

var JS = [
	{
		src: "./web-src/js/*.js",
		dest: "./static/js"
	}
]

gulp.task("sass", function () {
	result = SASS.map(function(item){
		return gulp.src(item.src)
			.pipe(plumber())
			.pipe(sass().on("error", sass.logError))
			.pipe(autoPrefixer({
				browsers: [
					"last 2 versions",
					"IE 9" 
				]
			}))
			.pipe(minifyCss())
			.pipe(gulp.dest(item.dest));
	});
	return merge(result)
});

gulp.task("js", function() {
	result = JS.map(function(item){
		return gulp.src(item.src)
			.pipe(plumber())
			.pipe(jshint())
			.pipe(jshint.reporter(stylishJshint))
			.pipe(jshint.reporter("fail"))
			.pipe(uglify())	
			.pipe(gulp.dest(item.dest));
	})
	return merge(result)
});

gulp.task("watch", function () {
	//Watch Sass for changes.
	SASS.forEach(function(item){
		var sassWatch = gulp.watch(item.src, ["sass"]);
		sassWatch.on("change", function (event) {
			console.log("Event '"+ event.type + "' detected on " + event.path + ". Running sass.");
		});
	});

	//Watch JS for changes.
	JS.forEach(function(item){
		var jsWatch = gulp.watch(item.src, ["js"]);
		jsWatch.on("change", function(event) {
			console.log("Event '"+ event.type + "' detected on " + event.path + ". Running js.");
		});
	});
});
