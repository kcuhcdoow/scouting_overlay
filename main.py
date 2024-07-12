import numpy as np
from vidgear.gears import CamGear
import cv2

dictOne = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 1
}
dictTwo = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 2
}
dictThree = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 3
}
dictFour = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 4
}
dictFive = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 5
}
dictSix = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 6
}
dictSeven = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 7
}
dictEight = {
  'link': 'https://www.youtube.com/watch?v=tG5j-kMV67s',
  'placement': -1,
  'opponents': [],
  'stream': 8
}

streams = [dictOne, dictTwo, dictThree, dictFour, dictFive, dictSix, dictSeven, dictEight]

# stream = CamGear(source=dictOne['link'], stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start() # YouTube Video URL as input
# streamTwo = CamGear(source=dictOne['link'], stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamThree = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamFour = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamFive = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamSix = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamSeven = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
# streamEight = CamGear(source='https://www.youtube.com/watch?v=tG5j-kMV67s', stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start()
#streams = [stream]#, streamTwo, streamThree, streamFour, streamFive, streamSix, streamSeven, streamEight]
userActivePlacement = 0
template = cv2.imread('CrossedSwords.png',cv2.IMREAD_GRAYSCALE)
USER_PLACEMENT_X_CORD_TO_SEARCH = 1832
SENSITIVITY = 30
USER_FACING_X_CORD_TO_SEARCH = 1845
inPlaceColor = [0,0,0]
opponentPresent = False

def getColorOfPoint(frame, x, y):
  return frame[y, x]

def likeColor(color1, color2):
  for i in range(3):
    if abs(color1[i] - color2[i]) > SENSITIVITY:
      return False
  return True

def findTemplateLocations(frame):
  # Apply template matching
  res = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
  threshold = 0.1
  loc = np.where(res >= threshold)

  # Draw bounding boxes around template matches
  for pt in zip(*loc[::-1]):
    cv2.rectangle(frame, pt, (pt[0] + template.shape[1], pt[1] + template.shape[0]), (255, 0, 0), 2)

  return frame


def findPlayerPosition(frame):
  # Find health bar position for this color
  color_to_find = [48, 184, 226]
  # Replace with the color you want to find
  height, width, _ = frame.shape
  for y in range(210, height):
    pixel_color = getColorOfPoint(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, y)
    if likeColor(pixel_color, color_to_find):
      return y
  return 0

def makeCross(frame, x = -1, y = -1, color=(0, 255, 0)):
  if x == -1 or y == -1:
    x = frame.shape[1] // 2
    y = frame.shape[0] // 2

  size = 7
  thickness = 2
  
  cv2.line(frame, (x - size, y), (x + size, y), color, thickness)
  cv2.line(frame, (x, y - size), (x, y + size), color, thickness)

def drawCrossOnUserPlacement(frame, x, y):
  makeCross(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, y, (255, 255, 255))

def determineAndSetUserPlacement(yHeight):
  global userActivePlacement
  afterHeight = yHeight - 200
  # print("AfterHeight: " + str(afterHeight))
  if afterHeight > 0:
    placement = int(round((afterHeight+54.638)/74.774))
    print("Placement: " + str(placement))
  else:
    placement = userActivePlacement
  userActivePlacement = placement

def doUserPlacementCode(frame):
  userY = findPlayerPosition(frame) 
  if (userY != -1):
    # Don't Do User Place 
    # print("printUserY:" + str(userY))
    drawCrossOnUserPlacement(frame, USER_PLACEMENT_X_CORD_TO_SEARCH, userY)
    determineAndSetUserPlacement(userY) 

def doOpponentFacingCode(frame, i):
  global opponentPresent
  global streams
  img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
  threshold = 0.755
  w, h = template.shape[::-1]
  loc = np.where( res >= threshold)
  if len(tuple(zip(*loc[::-1]))) == 0:
    opponentPresent = False
    streams[i]['opponents'] = []
  else:
    opponentPresent = True
  for pt in zip(*loc[::-1]):
    placement = round((pt[1]+38.821)/75.488)
    streams[i]['opponents'].append(placement)
    # print('opponent at: ' + str(pt[1]))
    # print(placement)
    cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
  streams[i]['opponents'] = list(set(streams[i]['opponents']))
  print(streams[i]['opponents'])



def processFrame(frame, i):
  # getColorOfPoints(frame) 
  # placeCrossOnPixelsToTrack(frame)
  # drawGrid(frame)
  doOpponentFacingCode(frame[190:880, 1600:1920], i)
  if opponentPresent == True:
    doUserPlacementCode(frame)
  # drawCrossOnUserPlacement(userY)
  # print(getColorOfPoint(frame, colorSamplingLocation[0], colorSamplingLocation[1]))
  # makeCross(frame, colorSamplingLocation[0], colorSamplingLocation[1], (255, 0, 0))
  
# infinite loop

framesToSkip = 0

while True:
  for i in range(len(streams)):
    stream = CamGear(source=streams[i]['link'], stream_mode = True, logging=True, options={"THREADED_QUEUE_MODE", False}).start() # YouTube Video URL as input
    frame = stream.read()
    # read frames
    # if (framesToSkip > 0):
    #   framesToSkip -= 1
    #   continue
    # framesToSkip = (stream.framerate / 1)
    # check if frame is None
    if frame is None:
      #if True break the infinite loop
      break
    
    
    processFrame(frame, i)
    # print(streams[i])
    # cv2.imshow("Output Frame", frame[190:880, 1600:1920])

    # Show output window
    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
      #if 'q' key-pressed break out
      break
  

    cv2.destroyAllWindows()
    # close output window

    # safely close video stream.
    stream.stop()


  def getColorOfPoint(frame, x, y):
    return frame[y, x]
    print('test')
  