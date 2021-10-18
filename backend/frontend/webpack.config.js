const Dotenv = require('dotenv-webpack');

module.exports = {

    // resolve: {
    //     fallback: {
    //         "os": false,
    //         "fs": false,
    //         "tls": false,
    //         "net": false,
    //         "path": false,
    //         "zlib": false,
    //         "http": false,
    //         "https": false,
    //         "stream": false,
    //         "crypto": false,
    //         "crypto-browserify": require.resolve('crypto-browserify'), //if you want to use this module also don't forget npm i crypto-browserify
    //     }
    // },

    // webpack.config.js
    plugins: [
        new Dotenv()
    ],

    module: {

        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: "babel-loader",
            },
            {
                test: /\.scss$/,
                use: ['style-loader', 'css-loader', 'sass-loader'],
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|jpg|gif)$/i,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                        },
                    },
                ],
            },
        ]
    },

    // performance: {
    //     hints: false,
    //     maxEntrypointSize: 512000,
    //     maxAssetSize: 512000
    // }
};