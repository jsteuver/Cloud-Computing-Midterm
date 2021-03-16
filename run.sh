# Shell script to run the docker image locally at port 8000
# Requires "env" file is downloaded and put in this directory
docker run -itp 8000:8000 --env-file env cc_midterm
