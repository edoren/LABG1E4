const gulp = require("gulp")
const gulp_typings = require("gulp-typings");
const gulp_typescript = require("gulp-typescript")

var ts_project = gulp_typescript.createProject("./tsconfig.json");

var source_folder = "psychologyTest/static/src";
var build_folder = "psychologyTest/static/js";

var paths = {
    // typescript files
    source_files: [
        "./" + source_folder + "/**/*.ts",
        "./" + source_folder + "/**/*.tsx"
    ],
    typings: [
        "./typings/**/*.d.ts"
    ]
};

gulp.task("install_typings", function () {
    return gulp.src("./typings.json").pipe(gulp_typings());
});

gulp.task("compile", function () {
    return gulp.src(paths.source_files.concat(paths.typings))
        .pipe(ts_project()).js
        .pipe(gulp.dest(build_folder));
});

gulp.task("watch", function () {
    gulp.watch(paths.source_files, ["compile"]);
});

gulp.task("runserver", ["compile"], function () {
    const spawn = require("child_process").spawn;

    var address = process.env.ADDRESS || "localhost";
    var port = process.env.PORT || 8000;

    var server = spawn("python", ["manage.py", "runserver", `${address}:${port}`], {
        stdio: "inherit"
    });

    server.on("close", function (code) {
        if (code !== 0) {
            console.log(`server process exited with code ${code}`);
        }
    });
});

gulp.task("default", ["watch", "runserver"]);
gulp.task("build", ["compile"]);
