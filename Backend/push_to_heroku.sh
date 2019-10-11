#!/usr/bin/env bash

# Do it one time in the terminal before running this script

# heroku login
# docker login

heroku container:login
docker build -t registry.heroku.com/company-search-engine-backend/web:latest .;
docker push registry.heroku.com/company-search-engine-backend/web:latest;
heroku container:release web -a company-search-engine-backend ;
