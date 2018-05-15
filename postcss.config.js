// For some weird reason, env param is not honoured
module.exports = ({ file, options, env }) => {
    return {
        plugins: {
            'postcss-import': {},
            'postcss-cssnext': {},
            // stylelint: env === 'production'
            //   ? false
            //   : {
            //     extends: ['stylelint-config-standard'],
            //     rules: {
            //       indentation: 'tab'
            //     }
            //   },
            'postcss-browser-reporter': {},
            'postcss-reporter': {}
        }
    };
};
