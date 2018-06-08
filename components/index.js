const fs = require('fs');

const assets =  '../assets/js/vendor/';

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

fs.createReadStream('./node_modules/foundation-sites/dist/js/foundation.min.js')
  .pipe(fs.createWriteStream(assets + 'foundation.min.js'));

fs.createReadStream('./node_modules/jquery/dist/jquery.min.js')
  .pipe(fs.createWriteStream(assets + 'jquery.min.js'));

