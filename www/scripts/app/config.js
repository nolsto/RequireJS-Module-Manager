requirejs.config({
  baseUrl: './scripts/app',
  paths: {
    // aliases
    'templates': '../../templates/app',
    // vendor libraries
    'require': '../vendor/require-2.1.1',
    'chaplin': '../vendor/chaplin-1.0.0-pre-c2dc4ce',
    'jquery': '../vendor/jquery-1.8.2',
    'underscore': '../vendor/underscore-1.4.2',
    'backbone': '../vendor/backbone-0.9.2',
    'backbone-relational': '../vendor/backbone-relational-0.6.0',
    'handlebars': '../vendor/handlebars-1.0.rc.1',
    // require.js plugins
    'text': '../vendor/require-text-2.0.3'
  },
  shim: {
    'backbone': {
      deps: ['jquery', 'underscore'],
      exports: 'Backbone'
    },
    'underscore': {
      exports: '_'
    },
    'backbone-relational': {
      deps: ['backbone']
    },
    'handlebars': {
      exports: 'Handlebars'
    }
  }
});
