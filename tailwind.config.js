module.exports = {
    mode: 'jit',
    purge: [
        './app.py',
        './apps/**/*.py',
        './tanager/**/*.py'
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {},
    },
    variants: {
        extend: {},
    },
    plugins: [],
}
