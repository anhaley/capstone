# -----------------------------------------------------------------------------
#                                 About heroku
# -----------------------------------------------------------------------------

# Heroku lets you deploy, run and manage applications written in Ruby, Node.js, Java, Python, Clojure, Scala, Go and PHP.
# Heroku is a polyglot platform – it lets you build, run and scale applications in a similar manner across all the
# languages – utilizing the dependencies and Procfile.

# Terminology: A slug is a bundle of your source, fetched dependencies, the language runtime, and compiled/generated
# (basically GZip) output of the build system - ready for execution. These slugs are a fundamental aspect of what happens
# during application execution - they contain your compiled, assembled application - ready to run - together with the
# instructions (the Procfile) of what you may want to execute.

# Terminology: Dynos are isolated, virtualized Unix containers, that provide the environment required to run an application.

# Heroku executes applications by running a command you specified in the Procfile, on a dyno that’s been preloaded
# with your prepared slug. to run your application on a dyno, the Heroku platform loaded the dyno with your most recent
# slug.

# You have control over how many dynos are running at any given time. Given the Procfile example earlier,
# you can start 5 dynos, 3 for the web and 2 for the queue process types, as follows:

heroku ps:scale web=3 queue=2

# Heroku lets you run your application with a customizable configuration - the configuration sits outside of your
# application code and can be changed independently of it. The configuration for an application is stored in config vars

# Terminology: Config vars contain customizable configuration data that can be changed independently of your source code
# The configuration is exposed to a running application via environment variables.

heroku config:set ENV_NAME=VALUE

# All dynos in an application will have access to the exact same set of config vars at runtime.
# All releases are automatically persisted in an append-only ledger. Use the "heroku releases" command to see the audit
# trail of release deploys. Every time you deploy a new version of an application, a new slug is created and release is
# generated. As Heroku contains a store of the previous releases of your application, it’s very easy to rollback and
# deploy a previous release.

# Because Heroku manages and runs applications, there’s no need to manage operating systems or other internal system
# configuration. One-off dynos can be run with their input/output attached to your local terminal. These can also be
# used to carry out admin tasks that modify the state of shared resources

heroku run bash

# Changes to the filesystem on one dyno are not propagated to other dynos and are not persisted across deploys and dyno
# restarts. A better and more scalable approach is to use a shared resource such as a database or queue.

# Terminology: Each dyno gets its own ephemeral filesystem - with a fresh copy of the most recent release. It can be
# used as temporary scratchpad, but changes to the filesystem are not reflected to other dynos.

# heroku also supports add-ons, logging and monitoring, HTTP routing.


# -----------------------------------------------------------------------------
#                           Using heroku w/ git
# -----------------------------------------------------------------------------

# first install heroku CLI by dling from this website: https://devcenter.heroku.com/articles/heroku-cli#download-and-install
# standalone install: curl https://cli-assets.heroku.com/install.sh | sh
# ubuntu install: curl https://cli-assets.heroku.com/install-ubuntu.sh | sh

# login to heroku so you are properly authenticated. If you don't have a login it opens a browser tab w/ a signup option.
heroku login

# Create the app
heroku create

# verify heroku remotes
git remote -v

# to add an existing remote:
heroku git:remote -a REMOTE_NAME

# to rename remotes (default name is "heroku")
git remote rename NAME NEW_NAME

# to deploy code, push it to the heroku remote:
git push heroku master

# if you want to push a specific branch do the following:
git push heroku BRANCH_NAME:master

# if you start a deployment, you can CTL+C to cancel out and it will continue building and deploying in the background.

# default git transport is HTTP but it can be configured for SSH as well using. Some additional lines of code are also used so that
# it rewrites git URLs to use SSH on the fly.
heroku create --ssh-git

# Install the free postgreSQL addon
heroku addons: create heroku-postgresql:hobby-dev



# -----------------------------------------------------------------------------
#                 Using heroku w/ git & Docker containers:
# -----------------------------------------------------------------------------

# Be sure to initialize the Git repository in your app’s root directory.
# If your app is in a subdirectory of your repository, it won’t run when it is pushed to Heroku.

# first include the file heroku.yml which is used to configure the dyno.

# Set the various environment variables and config vars...
heroku config:set ENV_NAME=VALUE

# deploy it
git push heroku master

# run it and initialize the database
heroku run APP_NAME --trace db:migrate

# lastly open web app in browser...
heroku open
