#! /usr/bin/python
from pynput import keyboard
import os
words=[]
def on_press(key):
	global words
	try:
		k=key.char
	except:
		k=key.name
	os.system('clear')
	if(len(words)>20):
		words=[]
	words.append(k)
	print("|".join(words))

print("Keypress:")
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()
