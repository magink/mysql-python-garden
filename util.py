import os
def pause_for_any_key():
  """Blocks program execution until any key is pressed"""
  print("\nPress any key to return to menu") 
  os.system("pause >nul") 
  # Couldn't figure out something without importing, but at least OS module doesn't need to be installed with pip
  # I have only tested on Windows, might be different on other OSes. 