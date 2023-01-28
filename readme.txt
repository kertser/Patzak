General Idea:
Make a deivece, based on RPi0 to detect face, build features and classify the face to match one of the previously
trained groups.

- We will test the fastest algoritms for face detection and feature recognition (openCV is too large for Pi-Zero)
- We will construct the classifier, based on unsupervised learning algorithm (KNN? SVM?)
- We will implement the program into the electronic device (RPi0)

* Raw Data is placed inside the Data folders.
* Working version for embedded system at RPi02W (may be I will arange a docker image for that later on) is patzak.py 
It is taking about 1 minute to load all the dependencies.
* Working on client-server version for better speed

#Enable SPI on Rpi0