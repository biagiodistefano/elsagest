'use strict';

const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const config = require('./config');
const entryPoints = require('./entry_points');
const utils = require('./utils');

module.exports = {
  entry: entryPoints,
  output: {
    path: config.outputPath,
    filename: '[name].[chunkhash].js',
    publicPath: `${config.host}/${config.publicPath}`
  },
  resolve: {
    extensions: ['.js', '.css', '.scss'],
    modules: [utils.cwd('elsagest'), utils.cwd('node_modules')],
    alias: {
      elsagest: config.srcPath,
      librosoci: `${config.srcPath}/librosoci/static/librosoci/`,
      elsahome: `${config.srcPath}/elsahome/static/elsahome/`,
      elsausers: `${config.srcPath}/elsausers/static/elsausers/`,
      elsamail: `${config.srcPath}/elsamail/static/elsamail/`,
      common: `${config.srcPath}/static/common/`,
      'CodeMirror': 'codemirror'
      // commonUtils: `${config.srcPath}/static/common/js/index`,
      // home: `${config.srcPath}/home/static/home/`,
      // giurisprudenza: `${config.srcPath}/giurisprudenza/static/giurisprudenza/`,
      // legislazione: `${config.srcPath}/legislazione/static/legislazione/`,
      // lawyertools: `${config.srcPath}/lawyertools/static/lawyertools/`
    }
  },
  module: {
    rules: [
      {
        test: /\.(js)$/,
        enforce: 'pre',
        use: [
          {
            loader: 'eslint-loader',
            options: {
              fix: false
            }
          }
        ],
        exclude: [/node_modules/]
      },
      {
        test: /\.(js)$/,
        use: 'babel-loader',
        exclude: [/node_modules/]
      },
      {
        test: /\.(eot|otf|ttf|woff|woff2)(\?.*)?$/,
        use: [
          {
            loader: 'file-loader',
            options: {
              name: '[name].[ext]',
              outputPath: 'fonts/'
            }
          }
        ]
      },
      {
        test: /\.(jpe?g|png|gif|svg)$/i,
        use: [
          'file-loader?limit=100000',
          {
            loader: 'img-loader',
            options: {
              enabled: true,
              optipng: true
            }
          }
        ]
      },
      {
        test: /\.(ico|webp)(\?.*)?$/,
        use: 'file-loader?limit=100000'
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      jquery: 'jquery',
      'global.jQuery': 'jquery',
      'window.jQuery': 'jquery',
      'window.$': 'jquery',
      Popper: ['popper.js', 'default'],
      Cookies: 'js-cookie',
      'window.Cookies': 'js-cookie',
      jsPDF: 'jspdf',
      'window.jsPDF': 'jspdf'
      // commonUtils: 'commonUtils',
      // 'window.commonUtils': 'commonUtils'
    }),
    new webpack.DefinePlugin({
      'process.env.BROWSER': true
    }),
    new webpack.DefinePlugin({
      'require.specified': 'require.resolve'
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor'
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'runtime'
    }),
    new webpack.NamedModulesPlugin(),
    new webpack.NamedChunksPlugin(),
    // new BundleAnalyzerPlugin(),
    new BundleTracker({ filename: './elsagest/static/webpack-stats.json' })
  ],
  target: 'web'
};
