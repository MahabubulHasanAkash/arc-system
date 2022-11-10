from keras import models
from collections import deque
import numpy as np
import imutils
from imutils.video import VideoStream
import cv2
import datetime

model = models.load_model('rock_classifier.h5')
print("Model Loaded")

labels  = ['Basalt','Highland','Coal', 'Granite','Limestone','Marble','Quartzite', 'Sandstone']
# initialize the predictions queue
Q = deque(maxlen=128)

# initialize the video stream, pointer to output video file, and
# frame dimensions
vs= VideoStream(src=0).start()
writer = None
(W, H) = (None, None)
 
# loop over frames from the video file stream
while True:
	# read the next frame from the file
	(grabbed, frame) = vs.read()
 
	# if the frame was not grabbed, then we have reached the end
	# of the stream
	if not grabbed:
		break
 
	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]

	# clone the output frame, then convert it from BGR to RGB
	# ordering and resize the frame to a fixed 224x224
	output = frame.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
	frame = cv2.resize(frame, (224, 224))
	frame = frame.astype("float32")
	frame = cv2.normalize(frame, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
	
	# make predictions on the frame and then update the predictions
	# queue
	preds = model.predict(np.expand_dims(frame, axis=0))[0]
	Q.append(preds)

	# perform prediction averaging over the current history of
	# previous predictions
	results = np.array(Q).mean(axis=0)
  
	i = np.argmax(results)
	label = labels[i]

	# draw the activity on the output frame
	text = "Detected: {}".format(label)
	cv2.putText(output, text, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
		1.25, (0, 255, 0), 5)
 
	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter('Videos/{:%Y-%m-%d}.avi'.format(datetime.datetime.now())
 , fourcc, 30,
			(W, H), True) 
	# write the output frame to disk
	writer.write(output)

 
 
# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()