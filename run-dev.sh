# Shell script to run the docker image locally at port 8000
# Requires "env" file is downloaded and put in this directory
#
# Identical to run.sh, but also ties internal code via volume, allowing for hot
# reloads

docker run -itp 8000:8000 \
    --env-file env \
    -v $(pwd)/cc_midterm/:/code \
    cc_midterm
