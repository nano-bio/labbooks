const {series, src, dest} = require('gulp');

function bootstrap() {
  return src('node_modules/bootstrap/dist/**/*')
    .pipe(dest('_vendor/bootstrap'))
}

function bootstrapIcons() {
  return src('node_modules/bootstrap-icons/font/**/*')
    .pipe(dest('_vendor/bootstrap-icons'))
}

function clusterize() {
  return src('node_modules/clusterize.js/clusterize*')
    .pipe(dest('_vendor/clusterize'))
}

function dygraphs() {
  return src('node_modules/dygraphs/dist/**/*')
    .pipe(dest('_vendor/dygraphs'))
}

function flot() {
  return src('node_modules/flot/*.js')
    .pipe(dest('_vendor/flot'))
}

function jquery() {
  return src('node_modules/jquery/dist/**/*')
    .pipe(dest('_vendor/jquery'))
}

function jqueryDeparam() {
  return src('node_modules/jquery-deparam/jquery-deparam.js')
    .pipe(dest('_vendor/jquery.deparam'))
}

function jqueryToast() {
  return src('node_modules/jquery-toast-plugin/dist/*')
    .pipe(dest('_vendor/jquery.toast'))
}


function jsCookie() {
  return src('node_modules/js-cookie/dist/js.cookie.min.js')
    .pipe(dest('_vendor/js.cookie'))
}

function plotly() {
  return src('node_modules/plotly.js/dist/**/*')
    .pipe(dest('_vendor/plotly'))
}

function simpleLightBox() {
  return src('node_modules/simplelightbox/dist/**/*')
    .pipe(dest('_vendor/simple-lightbox'))
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
