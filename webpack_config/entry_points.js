'use strict';

const path = require('path');
const config = require('./config');

const entryPoints = {
  // common vendor modules
  vendor: config.vendor,
  // custom modules
  common: [path.join(__dirname, '..', 'elsagest/static/common/js/index.js')],
  librosoci: [path.join(__dirname, '..', 'elsagest/librosoci/static/librosoci/js/index.js')],
  elsahome: [path.join(__dirname, '..', 'elsagest/elsahome/static/elsahome/js/index.js')],
  // giurisprudenza: [path.join(__dirname, '..', 'les/giurisprudenza/static/giurisprudenza/js/index.js')],
  // legislazione: [path.join(__dirname, '..', 'les/legislazione/static/legislazione/js/index.js')],
  // lawyertools: [path.join(__dirname, '..', 'les/lawyertools/static/lawyertools/js/index.js')]
  // legislazione_print: [path.join(__dirname, '..', 'les/legislazione/static/legislazione/js/index-print.js')]
};

// apply dev-server only on dev mode
if (process.env.NODE_ENV !== 'production') {
  Object.keys(entryPoints).forEach(k => {
    if (k !== 'vendor') {
      entryPoints[k].unshift(`webpack-dev-server/client?${config.host}`);
    }
  });
}

module.exports = entryPoints;
