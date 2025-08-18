#! /bin/bash
home=`realpath "$(dirname "$0")"/../`
cd $home && sudo docker build -t bipedal_navigation -f docker/Dockerfile.x64 --no-cache . 