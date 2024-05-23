#!/bin/bash

for i in {1..10}
do
	TIMESTAMP=$(date +"%Y%m%dT%H%M%S")
	fswebcam --no-banner -r 1280x1024 --jpeg 85 "./photo/${TIMESTAMP}.jpg"
done
