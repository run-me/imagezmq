from imutils import build_montages
from datetime import datetime
from imagezmq.imagezmq import ImageHub
import argparse
import imutils
import cv2

# constructing the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mW", "--montage_width", required=True, type=int)
ap.add_argument("-mH", "--montage_height", required=True, type=int)
args = vars(ap.parse_args())

ESTIMATED_NUM_PIS = 1
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_PIS * ACTIVE_CHECK_PERIOD

image_hub = ImageHub()

frame_dict = dict()

last_active = {}
last_active_check = datetime.now()

mW = args['montage_width']
mH = args['montage_height']

print(f"[INFO] hosting server for {ESTIMATED_NUM_PIS} pis")

while True:
    (rpi_name, frame) = image_hub.recv_image()
    image_hub.send_reply(b'OK')
    if rpi_name not in last_active.keys():
        print(f"[INFO] receiving data from {rpi_name}")
    frame = imutils.resize(frame, width=400)
    (h, w) = frame.shape[:2]

    # update the new frame in frame dictionary
    frame_dict[rpi_name] = frame

    montages = build_montages(frame_dict.values(), (w, h), (mW, mH))

    key = cv2.waitKey(1)

    if (datetime.now() - last_active_check).seconds > ACTIVE_CHECK_SECONDS:
        for (rpi_name, ts) in list(last_active.items()):
            if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
                print(f"[INFO] connection lost to {rpi_name}")
                last_active.pop(rpi_name)
                frame_dict.pop(rpi_name)

            last_active_check = datetime.now()

    if key == ord('q'):
        break

cv2.destroyAllWindows()
