# Cloud-Computing-Midterm

## Overview

This repo contains our Cloud Computing midterm for Spring 2021, tasking us to
learn Microsoft Azure while analyzing how to make a customer's life easier with
preset data.

## Development

### Installation

1. Install `docker`
1. Clone repo
1. Retrieve an `env` file from one of the contributors
1. Place `env` file within the top directory of the repo

### Build

`sh ./build.sh`

This will build a docker image locally

### Run

`sh ./run.sh`

This will run the built docker image. If run successfully, it will create a
server accessible at `http://127.0.0.1:8000`.
