'use strict';

const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const webpackConfig = require('./webpack.dev');
const config = require('./config');

let compiler;
try {
  compiler = webpack(webpackConfig);
} catch (err) {
  console.log(err.message);
  process.exit(1);
}

const app = new WebpackDevServer(compiler, {
  publicPath: webpackConfig.output.publicPath,
  inline: true,
  historyApiFallback: true,
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': '*',
    'Access-Control-Allow-Headers': '*'
  }
});
app.listen(config.port);
