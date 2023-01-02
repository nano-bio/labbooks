const {series, src, dest} = require('gulp');

function bootstrap() {
  return src('node_modules/bootstrap/dist/**/*')
    .pipe(dest('src/_vendor/bootstrap'))
}

function bootstrapIcons() {
  return src('node_modules/bootstrap-icons/font/**/*')
    .pipe(dest('src/_vendor/bootstrap-icons'))
}

function clusterize() {
  return src('node_modules/clusterize.js/clusterize*')
    .pipe(dest('src/_vendor/clusterize'))
}

function dygraphs() {
  return src('node_modules/dygraphs/dist/**/*')
    .pipe(dest('src/_vendor/dygraph'))
}

function flot() {
  return src('node_modules/flot/*.js')
    .pipe(dest('src/_vendor/flot'))
}

function jquery() {
  return src('node_modules/jquery/dist/**/*')
    .pipe(dest('src/_vendor/jquery'))
}

function jqueryDeparam() {
  return src('node_modules/jquery-deparam/jquery-deparam.js')
    .pipe(dest('src/_vendor/jquery.deparam'))
}

function jqueryToast() {
  return src('node_modules/jquery-toast-plugin/dist/*')
    .pipe(dest('src/_vendor/jquery.toast'))
}


function jsCookie() {
  return src('node_modules/js-cookie/dist/js.cookie.min.js')
    .pipe(dest('src/_vendor/js.cookie'))
}

function plotly() {
  return src('node_modules/plotly.js/dist/**/*')
    .pipe(dest('src/_vendor/plotly'))
}

function simpleLightBox() {
  return src('node_modules/simplelightbox/dist/**/*')
    .pipe(dest('src/_vendor/simple-lightbox'))
}


exports.default = series(
  bootstrap,
  bootstrapIcons,
  clusterize,
  dygraphs,
  flot,
  jquery,
  jqueryDeparam,
  jqueryToast,
  jsCookie,
  plotly,
  simpleLightBox
)
