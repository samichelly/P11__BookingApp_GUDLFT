# PROJECT_11__gudlift_registration

## Project Description

This is a proof of concept (POC) project to show a light-weight version of our competition booking platform. The aim is to keep things as light as possible and use feedback from the users to iterate.

## Table of Contents

- [Getting Started](#getting-started)
- [Installation](#installation)
- [Current Setup](#current-setup)
- [Testing](#testing)

## Getting Started

This project uses the following technologies:

- Python v3.x+
- [Flask](https://flask.palletsprojects.com/en/1.1.x/)

  Whereas Django does a lot of things for us out of the box, Flask allows us to add only what we need.

- [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

  This ensures you'll be able to install the correct packages without interfering with Python on your machine. Before you begin, please ensure you have this installed globally.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/samichelly/PROJECT_11_gudlift_registration.git
   ```
2. Navigate to the project directory and set up a virtual environment:
   ```bash
   cd PROJECT_11_gudlift_registration
   python -m venv env
   ```
3. Activate the virtual environment:
   - On Windows:
     ```bash
     env\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the Flask application environment variable to `server.py`:
   ```bash
   export FLASK_APP=server.py
   ```
   For Windows, use:
   ```bash
   set FLASK_APP=server.py
   ```
6. Run the application:
   ```bash
   flask run
   ```
   or
   ```bash
   python -m flask run
   ```

## Current Setup

The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a database until we actually need one. The main JSON files are:
- `competitions.json` - list of competitions
- `clubs.json` - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

## Testing

You are free to use whatever testing framework you like—the main thing is that you can show what tests you are using. We also like to show how well we're testing, so there's a module called [coverage](https://coverage.readthedocs.io/en/coverage-5.1/) you should add to your project.
