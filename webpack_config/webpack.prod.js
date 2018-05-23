'use strict';

process.env.NODE_ENV = 'production';

const exec = require('child_process').execSync;
const path = require('path');
const glob = require('glob');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');
const ProgressPlugin = require('webpack/lib/ProgressPlugin');
const base = require('./webpack.base');
const config = require('./config');

exec('rm -rf elsagest/static/build');
base.devtool = 'source-map';
base.module.rules.push(
  {
    test: /\.css$/,
    use: ExtractTextPlugin.extract({
      fallback: 'style-loader',
      use: ['css-loader', 'postcss-loader']
    })
  },
  {
    test: /\.scss$/,
    use: ExtractTextPlugin.extract({
      fallback: 'style-loader',
      use: ['css-loader', 'postcss-loader', 'sass-loader']
    })
  }
);

base.plugins.push(
  new ProgressPlugin(),
  new ExtractTextPlugin('[name].[chunkhash].css'),
  new webpack.DefinePlugin({
    'process.env.NODE_ENV': JSON.stringify(process.env.NODE_ENV)
  }),
  new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /it/),
  new webpack.optimize.AggressiveMergingPlugin(),
  new OptimizeCssAssetsPlugin(),
  new webpack.optimize.UglifyJsPlugin({
    sourceMap: true,
    compress: {
      warnings: false
    },
    output: {
      comments: false
    }
  }),
  new CompressionPlugin()
);

// minimize webpack output
base.stats = {
  // Add children information
  children: false,
  // Add chunk information (setting this to `false` allows for a less verbose output)
  chunks: false,
  // Add built modules information to chunk information
  chunkModules: false,
  chunkOrigins: false,
  modules: false
};

module.exports = base;
