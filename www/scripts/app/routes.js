define(function() {
  'use strict';

  var routes = function(match) {
    match('', 'slides#show');
    match(':sid', 'slides#show', {constraints: {sid: /^s\d+$/}});
    match('', 'slides#show', {constraints: {index: /^\d+$/}});
  };

  return routes;
});
