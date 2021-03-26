# Tanager

## Description

A dashboard app for visualizing [Inspyred](https://pythonhosted.org/inspyred/) evolutionary computation algorithms.

## Getting Started

The following steps will clone the GitHub repo, install a python virtual environment, activate the environment, install
all required python dependencies, and start the application.

```bash
git clone git@github.com:jogoodma/tanager.git
cd tanager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python ./app.py
```

You should see this in the terminal after executing the script.

```
Dash is running on http://127.0.0.1:8050/

 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
```

Once you see the above message, open up the URL in a browser.

## Development

The following information is important for developers of Tanager

### Setup

Developing for Tanager requires [yarn](https://yarnpkg.com/) or [npm](https://www.npmjs.com/get-npm) to be installed.
Please refer to their docs for further information on installing them.

1. Install css and js dependencies.

```
cd tanager
yarn install
```

or

```
cd tanager
npm install
```

### Directory Structure

* assets - Static assets (images, css, js, etc.) that Dash automatically pulls into the app.
* css - Tailwind CSS files
* package.json - CSS & JS dependencies and scripts.
* tailwind.config.js - Tailwind CSS cli configuration.
* requirements.txt - Python dependencies.

### CSS

This application uses the [Tailwind](https://tailwindcss.com/) CSS framework for some aspects of the application
styling. The main CSS file is located in [css/tailwind.css](css/tailwind.css). This is the file that should be edited
and expanded as needed. If you are not using Tailwind CSS classes then you do not need to worry about running the
Tailwind CSS client as the pre-built css files should already be in place.

To produce the final CSS file that gets included into the app you need to run:

```
yarn run build:css
```

This takes the [css/tailwind.css](css/tailwind.css) file and runs it through the Tailwind CSS client to produce the
final [assets/styles.css](assets/styles.css) file. **Do not manually edit the [assets/styles.css](assets/styles.css)
file as your changes will be overwritten.** The Tailwind client scans the python code for Tailwind css classes and
builds a css file that only contains the necessary styles for what was used in the application. This keeps the final CSS
file lean and mean.

When actively developing with Tailwind CSS classes you can use the dev mode, which periodically scans for changes in the
python source code and rebuilds the CSS when necessary.

```
yarn run dev
```

## See Also

* [Inspyred](https://pythonhosted.org/inspyred/)
* [Dash Documentation](https://dash.plotly.com/)
* [Tailwind CSS](https://tailwindcss.com/)
