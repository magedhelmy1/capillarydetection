const Dotenv = require('dotenv-webpack');

module.exports = {

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

    performance: {
        maxEntrypointSize: 5120000,
        maxAssetSize: 5120000
    }
};