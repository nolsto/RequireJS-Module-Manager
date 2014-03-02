// For any third party dependencies, like jQuery, place them in the lib folder.

// Configure loading modules from the lib directory,
// except for 'app' ones, which are in a sibling
// directory.
requirejs.config({
  baseUrl: 'js/lib',
  paths: {
    app: '../app',
    dev: '../dev',
    polyfill: '../polyfill',
    webfont: [
      '//ajax.googleapis.com/ajax/libs/webfont/1.5.0/webfont',
      'webfont'
    ]
  },
  map: {
    '*': {
      'zepto': 'zepto.custom'
    },
    'zepto.custom': {
      'zepto': 'zepto'
    }
  }
});
