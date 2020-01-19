from imutils.video import VideoStream
from imagezmq.imagezmq import ImageSender
import argparse
import socket
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-s",
                "--server-ip",
                required=True,
                help="ip of the server which the client will connect to")

args = vars(ap.parse_args())

sender = ImageSender(connect_to='tcp://{}:5555'.format(args['server-ip']))

rpi_name = socket.gethostname()
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

while True:
    frame = vs.read()
    sender.send_image(rpi_name, frame)
