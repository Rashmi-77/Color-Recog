
'''
Given a color image, the program identifies the color name at any point the user clicks. 
There is list of 865 colors mentioned in http://en.wikipedia.org/wiki/List_of_colors which has been extracted into 
a csv file in  https://github.com/codebrainz/color-names/blob/master/output/colors.csv.
'''

#import the required libraries 

import cv2
import pandas as pd
import urllib.request
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)
FONT = cv2.FONT_HERSHEY_SIMPLEX
SIZE = 0.5

# The pixel's RGB value is used to ideltify the color name from the csv file. 
def get_color(red,green,blue):

	min_val = 1000#float('inf')
	for i in range(len(colors)):
		#d = abs(red- int(colors.loc[i,"red"])) + abs(green- int(colors.loc[i,"green"]))+ abs(blue- int(colors.loc[i,"blue"]))
		d = abs(red- colors.loc[i,"red"]) + abs(green- colors.loc[i,"green"])+ abs(blue- colors.loc[i,"blue"])
		if(d<=min_val):
			min_val = d
			clr = colors.loc[i,"color_name"]
	return clr	

#Capture the Mouse click event to get the pixel value and position on the image

def get_mouse_point(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDOWN:
		global mouse_click,x_pos,y_pos,r,g,b
		mouse_click = True
		x_pos = x
		y_pos = y

		#The image is stored in BGR format 		
		b,g,r = img[y,x]
	
#Get the image from the specified url.  

def get_image(url):
	response = urllib.request.urlopen(url)
	if response.status != 200:
		return False
	return response

#Read the csv file stored locally and drop the columns(id and hex value) that we don't need here for now

def read_color_file(csv):
	colors = pd.read_csv(csv)
	colors = colors.drop(['id','hex'],axis=1)
	return colors

color_url = "colorbrain.csv"
colors = read_color_file(color_url)
url = 'https://www.pngfind.com/pngs/m/567-5671593_color-palette-pantone-de-colores-cmyk-hd-png.png'
response = get_image(url)

if response.status == 200:
	#If response is success, convert the image into a numpy array:
	img_array = np.array(bytearray(response.read()), dtype=np.uint8)

	#Next decode the image:
	img = cv2.imdecode(img_array, -1)

	mouse_click = False 
	r=g=b=0
	x_pos=y_pos = 0

	cv2.namedWindow('Color-Recognition')
	cv2.setMouseCallback('Color-Recognition',get_mouse_point)

	while(1):
		cv2.imshow("Color-Recognition",img)
		if (mouse_click):
			
			c = get_color(r,g,b)

			#Calculate the brightness of the background and display the text black or white
			#Source : https://en.wikipedia.org/wiki/Relative_luminance

			bright = (0.2126*r + 0.7152*g + 0.0722*b)
			if bright >=100:
				cv2.putText(img,c,(x_pos,y_pos),FONT,SIZE,BLACK)
			else:
				cv2.putText(img,c,(x_pos,y_pos),FONT,SIZE,WHITE)
		mouse_click=False
		
		#Escape key exits the loop
		if cv2.waitKey(50) & 0xFF==27:
			break

	#Close all the windows
	cv2.destroyAllWindows()
else:
	print("Invalid URL")

