#	CS669 - Assignment 2 (Group-2) 
#	Last edit: 28/10/17
#	About: 
#		This program extracts 2-D feature vectors from B/W test images for a few overlapping patch sizes to test later.

import numpy as np
import math
import os
import random
from PIL import Image

patchSize=2									#	Size of overlapping patches in the images.

#	Extracts features from images.
def calcPrereq(direct,directOut):

	#	Reading images...
	tempData=[]
	for filename in os.listdir(direct):
		image=Image.open(direct+filename)
		if image is not None:
			tempData.append(np.array(image))
	N=len(tempData)

	#	Making patches and writing feature vectors to a file...
	for n in range(N):
		file=open(os.path.join(directOut,"trainingFeaturesPatchSize"+str(patchSize)+"_"+str(n+1)+".txt"),"w")
		imgSize=np.shape(np.array(tempData[n]))
		file.write(str(imgSize[0]-patchSize+1)+" "+str(imgSize[1]-patchSize+1)+"\n")
		start_x=0
		for end_x in range(patchSize-1,imgSize[0]):
			
			#	First calculating data for first patch.
			start_y,end_y=0,patchSize-1
			tempMean=0.0
			tempVariance=0.0
			
			for i in range(start_x,end_x+1):
				for j in range(start_y,end_y+1):
					tempMean+=tempData[n][i][j]
			tempMean/=patchSize**2
			for i in range(start_x,end_x+1):
				for j in range(start_y,end_y+1):
					tempVariance+=(tempData[n][i][j]-tempMean)**2
			
			tempVariance/=patchSize**2
			
			file.write(str(tempMean)+" "+str(tempVariance)+"\n")
			
			#	Now using it to calculate data for next patches in that row, efficiently.
			for end_y in range(patchSize,imgSize[1]):
				oldMean=tempMean
				oldVariance=tempVariance
				newMean=oldMean*patchSize**2
				
				for x in range(start_x,end_x+1):
					newMean-=tempData[n][x][start_y]
				for x in range(start_x,end_x+1):
					newMean+=tempData[n][x][end_y]
				
				newMean/=patchSize**2
				newVariance=oldVariance*patchSize**2
				newVariance+=patchSize**2*(newMean**2-oldMean**2)
				newVariance-=2*(patchSize**2)*oldMean*(newMean-oldMean)
				
				for x in range(start_x,end_x+1):
					newVariance+=(tempData[n][x][end_y]-newMean)**2
				for x in range(start_x,end_x+1):
					newVariance-=(tempData[n][x][start_y]-newMean)**2
				
				newVariance/=patchSize**2
				start_y=start_y+1
				file.write(str(tempMean)+" "+str(tempVariance)+"\n")
				tempMean=newMean
				tempVariance=newVariance
			start_x=start_x+1
		file.close()

#	Program starts here...
print ("\nThis program extracts 2-D feature vectors from test B/W images for different patch sizes.\n")

#	Parsing Input... 
choice= raw_input("Do you want to use your own directory for test input and output or default (o/d): ")

directT=""
directOtest=""

if(choice=='o'):
	directT=raw_input("Enter the path (relative or complete) of the test images directory: ")
	directO=raw_input("Enter the path (relative or complete) of the directory to store these feature vectors: ")
	directOtest=os.path.join(directO,"test")
else:
	directT="../../data/Input/Clustering/Dataset 2/C/test"
	directOtest="../../data/Output/Clustering/Dataset 2/C/featureVectorsTest"

maxP=input("Make test files for patch size from 2 up to: ")

if directT[len(directT)-1]!='/':
	directT+="/"
if directOtest[len(directOtest)-1]!='/':
	directOtest+="/"

print "Reading images and generating feature vectors from test data for different patch sizes. (this may take a while)..."
for i in range(maxP-1):
	patchSize=i+2
	calcPrereq(directT,directOtest)

print "Features extracted successfully."

#	End.