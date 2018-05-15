'use strict';

const path = require('path');

module.exports.cwd = file => {
  return path.join(process.cwd(), file || '');
};
