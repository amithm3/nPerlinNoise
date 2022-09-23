module.exports = function override(config, env) {
    config.resolve.fallback = {"url": false};
    return config;
}
