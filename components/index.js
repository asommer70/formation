const fs = require('fs');

const assets =  '../assets/js/vendor/';
const cssAssets = '../assets/css/vendor/';

if (!fs.existsSync('../assets')) {
  fs.mkdirSync('../assets');

  if (!fs.existsSync('../assets/js')) {
    fs.mkdirSync('../assets/js');

    if (!fs.existsSync('../assets/js/vendor')) {
      fs.mkdirSync('../assets/js/vendor');
    }
  }

  
  if (!fs.existsSync('../assets/css')) {
    fs.mkdirSync('../assets/css');

    if (!fs.existsSync('../assets/css/vendor')) {
      fs.mkdirSync('../assets/css/vendor');
    }
  }
}


// Foundation and jQuery.
fs.createReadStream('./node_modules/foundation-sites/dist/js/foundation.min.js')
  .pipe(fs.createWriteStream(assets + 'foundation.min.js'));

fs.createReadStream('./node_modules/jquery/dist/jquery.min.js')
  .pipe(fs.createWriteStream(assets + 'jquery.min.js'));

fs.createReadStream('./node_modules/jQuery.serializeObject/dist/jquery.serializeObject.min.js')
  .pipe(fs.createWriteStream(assets + 'jquery.serializeObject.min.js'));


// CodeMirror
fs.createReadStream('./node_modules/codemirror/lib/codemirror.js')
  .pipe(fs.createWriteStream(assets + 'codemirror.js'));

fs.createReadStream('./node_modules/codemirror/mode/xml/xml.js')
  .pipe(fs.createWriteStream(assets + 'xml.js'));

fs.createReadStream('./node_modules/codemirror/mode/htmlmixed/htmlmixed.js')
  .pipe(fs.createWriteStream(assets + 'htmlmixed.js'));

fs.createReadStream('node_modules/codemirror/lib/codemirror.css')
  .pipe(fs.createWriteStream(cssAssets + 'codemirror.css'));


// Vue
fs.createReadStream('node_modules/vue/dist/vue.min.js')
  .pipe(fs.createWriteStream(assets + 'vue.min.js'));
