# Creating a Web Application using Flask, Docker, Heroku

This project ties together some important concepts and technologies from The Data Incubator (TDI) 12-day course, including Git, Flask, JSON, Pandas, Requests, Heroku, and Bokeh for visualization. Using a Docker container (as opposed to the [conda-buildpack](https://github.com/thedataincubator/conda-buildpack)) allows us to use a wider variety of packages than a bare Heroku install and overcomes limitations associated with Heroku slug limit (useful for deploying complex scikit-learn models, for example). This is motivated by [python-miniconda](https://github.com/heroku-examples/python-miniconda).

Click [here](https://asl367-stocks-vis-docker1.herokuapp.com/index) for a finished example.

The repository contains all the necessary pieces to deploy a Flask app (using a Docker container) to Heroku:
- A Python-based app (and associated "home" and "index" html files) that involves both 'GET' and 'POST' methods (before this I followed [this tutorial](https://github.com/bev-a-tron/MyFlaskTutorial) to make a functional app in debug mode).
- A Docker file that creates a docker container for your app, the foundation of which is [Miniconda3](https://hub.docker.com/r/continuumio/miniconda3) (although [other Docker containers](https://hub.docker.com/u/continuumio) can be utilized if you are running different versions of Python or the full Anaconda distribution).
- Anaconda package requirements which will be installed as part of the Docker container.
- Standard Python WSGI (Web Server Gateway Interface) file that acts as an interface between the webserver and the web-app you want to run.

## Step 0: Before You Begin
- Read through the Docker Desktop for Windows [Documentation](https://docs.docker.com/docker-for-windows/install/), ESPECIALLY "System Requirements". I had to purchase Windows 10 Pro (Docker won't work with the student version I had) and enable virtualization.
- Read through the Heroku CLI [quickstart guide](https://devcenter.heroku.com/articles/getting-started-with-python), where you'll see some additional pre-requisites for Heroku to work properly.
- Most notably, I had to install PostgreSQL and a number of associated app add-ons using "Application Stack Builder", including:
  - (Add-ons, tools, and utilities) pgAgent v3.4.0-3
  - (Add-ons, tools, and utilities) pgBouncer v1.9.0-1
  - (Database Drivers) Npgsql v3.2.6-1
  - (Database Drivers) pgJDBC v42.2.2-1
  - (Database Server) PostgreSQL (64 bit) v11.2.1
  - (Spatial Extensions) PostGIS 2.5 Bundle for PostgreSQL 11 (64 bit)
  - (Web Development) ApacheHTTPD v2.4.33-1
    - Note: I took a "more is better" approach and installed all the available add-on apps I could. These may not be required to get your web-application up and running, and you can go back and install any additional components at any time, just by running the "Application Stack Builder" application.

## Step 1: Install and Login to Docker & Heroku
- Create a [Docker account](https://hub.docker.com/signup), then download and install [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows).
- Create a [Heroku account](https://signup.heroku.com/login), then download and install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
- Open Anaconda Prompt or your prefered command prompt.
- Double check that Docker Desktop is running on your computer (default settings will open Docker on startup) using `docker --version`.
- Login to Heroku using `heroku login` - will open a browser window where you can login to Heroku CLI.
- Double check that this was successful with `heroku --version`.

## Step 2: Create and Deploy Test Webapp
- Git clone this template repository, navigate to that directory.
- Create Heroku application with `heroku create -a <app_name>` (maybe call this yourusername-webapp-test).
- Login to container with `heroku container:login`.
- Deploy to Heroku: `heroku container:push web -a <app_name>`.
- Release image on Heroku: `heroku container:release web -a <app_name>`.
- You should be able to see your site at `https://<app_name>.herokuapp.com/index` (note "/index" is needed at the end due to the decorator on line 17 of `app.py`.

## Step 3: Make Modifications to Create Your Own App!
- Create your own web-application `app.py` and associated html file(s). Again, consult this [helpful tutorial](https://github.com/bev-a-tron/MyFlaskTutorial) to create an app that runs locally in debug mode.
- If your app requires additional conda packages, add them to `conda-requirements.txt`.
- If your app requires additional packages not available through [Anaconda](https://anaconda.org), uncomment lines 3 and 6 in `Dockerfile` and create a `requirements.txt` file in the `/app` directory (analogous to `conda-requirements.txt`).
- The goal here is to create a Docker container that has the minimal conda environment to run your web-app.
- Repeat _Step 2_ for each additional web-app you would like to create.
- You can view, modify, delete your web-apps in your Heroku account the same way as you would with Github.