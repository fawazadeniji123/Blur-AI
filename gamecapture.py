# bring in pynput for keypress capture
from pynput.keyboard import Key, Listener 
# Bring in mss
from mss import mss
# Bring in opencv for rendering 
import cv2
import numpy as np
import time
import uuid
import os 


class GamePlay:
  def __init__(self):
    # setup game area
    self.game_area = {"left": 0, "top": 0, "width": 640, "height": 480}
    self.capture = mss()
    self.current_keys = None
    self.start = True

  def collect_gameplay(self):
    # Listen for keystrokes
    listener = Listener(on_press=self.on_keypress, on_release=self.on_keyrelease) 
    listener.start()

    # Collect the frames
    id = str(uuid.uuid1())
    filename = lambda dir: os.path.join('data', f'{dir}', id)
    gamecap = np.array(self.capture.grab(self.game_area))

    if self.current_keys:  
      cv2.imwrite(f'{filename("images")}.jpg', gamecap)
      np.savetxt(f'{filename("target")}.txt', np.array([str(self.current_keys)]), fmt='%s')
    
    return self.start

  def on_keypress(self, key): 
    if self.current_keys == key:
      print(self.current_keys)
      return self.current_keys
    else: 
      print(self.current_keys)
      self.current_keys = key
      return self.current_keys 

  def on_keyrelease(self, key): 
    self.current_keys = None
    if key == Key.esc:
      self.start = False
      return False

if __name__ == '__main__':
  # Sleep for 10 seconds to allow us to get back into the game
  print('sleeping...') 
  time.sleep(5)
  print('starting...')

  game = GamePlay()

  start = True
  while start:
    time.sleep(1)
    start = game.collect_gameplay()