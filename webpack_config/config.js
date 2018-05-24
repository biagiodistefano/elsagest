'use strict';
const path = require('path');
const utils = require('./utils');

module.exports = {
  port: 3000,
  host: process.env.NODE_ENV === 'development' ? 'http://localhost:3000' : '46.101.168.89',
  publicPath: 'elsagest/static/build/',
  srcPath: path.join(__dirname, '..', 'elsagest'),
  outputPath: path.join(__dirname, '..', 'elsagest', 'static', 'build'),
  vendor: [
    // npm libs
    'babel-polyfill',
    'jquery',
    'jquery-ui-dist/jquery-ui.min.js',
    'jquery-ui-dist/jquery-ui.theme.min.css',
    'popper.js',
    'bootstrap/dist/js/bootstrap.min.js',
    'bootstrap/dist/css/bootstrap.min.css',
    'bootstrap/dist/css/bootstrap-theme.min.css',
    'moment',
    'moment/locale/it',
    'js-cookie',
    'jquery-visible',
    'lodash.isundefined',
    'qs',
    'bootstrap-datepicker/dist/js/bootstrap-datepicker.min.js',
    'bootstrap-datepicker/dist/locales/bootstrap-datepicker.it.min.js',
    'bootstrap-datepicker/dist/css/bootstrap-datepicker3.min.css',
    'bootstrap-slider/dist/bootstrap-slider.min.js',
    'bootstrap-slider/dist/css/bootstrap-slider.min.css',
    // // custom stuff
    //'elsagest/static/vendor/js/bootstrap3-typeahead.min.js',
    'elsagest/static/vendor/scss/fonts.scss'
  ]
};
