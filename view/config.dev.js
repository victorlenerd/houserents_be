const webpack = require('webpack');
const path = require('path');

module.exports = {
    entry: "./src/index.js",
    watch: true,
    mode: "development",
    devtool: "sourcemap",
    target: "web",
    module: {
        rules: [
            {
                test: /\.js?$/,
                use: [
                    {
                        loader: "babel-loader",
                        options: {
                            babelrc: false,
                            presets: [
                                "@babel/preset-env",
                                "@babel/preset-react",
                            ],
                            plugins: [
                                "transform-regenerator",
                                "@babel/plugin-syntax-dynamic-import",
                                ["@babel/plugin-transform-runtime", { useESModules: true }],
                                "transform-class-properties"
                            ]
                        }
                    }
                ],
                exclude: /node_modules/
            },
            {
                test: /\.css$/,
                use: ["style-loader", "css-loader"]
            },
            {
                test: /\.(png|jpg|gif|svg)$/,
                loader: 'url-loader'
            }
        ]
    },
    plugins: [
        new webpack.DefinePlugin({
            NODE_ENV: "development"
        })
    ],

    output: {
        path: path.join(__dirname, "/public/dist"),
        filename: "bundle.js"
    }
};