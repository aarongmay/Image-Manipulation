#Author: Aaron May

#Apply and display a number of filters on a user selected image and then output original and final images side to side for comparison
#Filters include:
# -grey scale
# -posterise
# -sobel
# -posterise and sobel merge

#Process and output each image filter on a user selected image
def applyFilters():
  image = makePicture(pickAFile())  
  greyScaleImage = greyScale(image)#pictureCopy will be used in the final step and is therefore passed down as a parameter through the whole program until the final step    
  posterisedImage = posterise(greyScaleImage)#pictureCopy will be used in the final step
  sobelImage = sobel(posterisedImage)#pictureCopy will be used in the final step
  mergedImage = mergeImages(posterisedImage, sobelImage)#pictureCopy will be used in the final step
  finalImage = ouputOriginalAndFinalImages(image, mergedImage)
  return finalImage  
     

#Applies grey scale filter to image
def greyScale(image):
  greyScaleImage = makeEmptyPicture(getWidth(image),getHeight(image))#creates a copy of the original picture

  for x in range(0,getWidth(image)):
    for y in range(0, getHeight(image)):
      color = getColor(getPixel(image, x,y))
      setColor(getPixel(greyScaleImage,x,y),color)
    
  for p in getPixels(greyScaleImage): 
    amount = (getRed(p) + getGreen(p) + getBlue(p))/3
    setColor(p, makeColor(amount))    
  repaint(greyScaleImage)
  return(greyScaleImage)
  
     
#Calculates the mid range of a pixel
#8 equally spaced grey-scale values between (0-255)
def midRange(value):
  if value < 32:
    value = 16
  elif value < 64:
    value = 48
  elif value < 96:
    value = 80
  elif value < 128:
    value = 110
  elif value < 160:
    value = 144
  elif value < 192:
    value = 176
  elif value < 224:
    value = 208
  else:
    value = 240
  return value
  

#Create a posterised image
#Posterising is applied by replacing each channel of every pixel with the mid range of values it lies in 
def posterise(image):
#The pic is posterised by replacing each channel of every pixel with the mid range of values it lies in
  posterisedImage = makeEmptyPicture(getWidth(image),getHeight(image))#creates a copy of the greyScale picture
  
  for x in range(0,getWidth(image)):
    for y in range(0, getHeight(image)):
      color = getColor(getPixel(image, x,y))
      setColor(getPixel(posterisedImage,x,y),color)
    
  for px in getPixels(posterisedImage):
    setRed(px, midRange(getRed(px)))
    setGreen(px, midRange(getGreen(px)))
    setBlue(px, midRange(getBlue(px)))
  repaint(posterisedImage)
  return(posterisedImage)  
  
  
#Create a sobel edge image 
def sobel(image):
  sobelImage = makeEmptyPicture(getWidth(image),getHeight(image))#creates a copy of the posterised picture

  for x in range(0,getWidth(image)):
    for y in range(0, getHeight(image)):
      color = getColor(getPixel(image, x,y))
      setColor(getPixel(sobelImage,x,y),color)
    
  for x in range(1, getWidth(image)-1): # 1 and -1 because the end pixels don't have all 8 pixels around them 
    for y in range(1, getHeight(image) -1):
      
      #defines the location of each pixel around the centre pixel
      centrePix = getPixel(sobelImage,x,y)
      topL = getPixel(image,x - 1,y - 1)
      top = getPixel(image,x,y - 1)
      topR = getPixel(image,x + 1,y - 1)
      left = getPixel(image,x - 1,y)
      right = getPixel(image,x + 1,y)
      bottomL = getPixel(image,x - 1,y + 1)
      bottom = getPixel(image,x,y + 1)
      bottomR = getPixel(image,x + 1,y + 1)
      
      #horizontal and vertical mask calculation
      gHorizontal = (getRed(topL)*1)+(getRed(top)*2)+(getRed(topR)*1)+(getRed(left)*0)+(getRed(centrePix)*0)+(getRed(right)*0)+(getRed(bottomL)*-1)+(getRed(bottom)*-2)+(getRed(bottomR)*-1)
      gVertical = (getRed(topL)*-1)+(getRed(top)*0)+(getRed(topR)*1)+(getRed(left)*-2)+(getRed(centrePix)*0)+(getRed(right)*2)+(getRed(bottomL)*-1)+(getRed(bottom)*0)+(getRed(bottomR)*1)      

      sobelGrey = makeColor(abs(gHorizontal) + abs(gVertical))#abs added to ensure is positive number
      setColor(centrePix,sobelGrey)
  repaint(sobelImage)
  threshold = 150 # this applies a threshold of 150 to the sobelThreshold function
  return(sobelThreshold(sobelImage,threshold))#posterisedPic will be used in mergeImages() and pictureCopy will be used in the final step) 
  
  
#Alter the background white and the edges blue  
def sobelThreshold(sobelImage,threshold):
  sobelThresholdImage = makeEmptyPicture(getWidth(sobelImage),getHeight(sobelImage))#creates a copy of the sobel picture

  for x in range(0,getWidth(sobelImage)):
    for y in range(0, getHeight(sobelImage)):
      color = getColor(getPixel(sobelImage, x,y))
      setColor(getPixel(sobelThresholdImage,x,y),color)

  for px in getPixels(sobelThresholdImage):
    redC = getRed(px)
    blueC = getBlue(px)
    greenC = getGreen(px)
    if redC < threshold:
      setRed(px,0)
    if blueC < threshold:
      setBlue(px,0)
    if greenC < threshold:
      setGreen(px,0)
  
  for px in getPixels(sobelThresholdImage):#inverts the colors
    color = getColor(px)
    negColor = makeColor(255-getRed(px),255-getBlue(px),255-getGreen(px))
    setColor(px,negColor)
    
  for px in getPixels(sobelThresholdImage):#makes outline blue
    redC = getRed(px)
    blueC = getBlue(px)
    greenC = getGreen(px)
    if redC < 255:
      setRed(px,0)
    if blueC < 255:
      setBlue(px,150)
    if greenC < 255:
      setGreen(px,0)
  repaint(sobelThresholdImage)
  return(sobelThresholdImage)  
 

#Apply posterised picture and sobel edge image with threshold
#and add edge colour from the sobel image on top of the posterised image       
def mergeImages(posterisedImage, sobelThresholdImage):
 
  for x in range(0, getWidth(sobelThresholdImage)):
    for y in range(0, getHeight(sobelThresholdImage)):
      pix1 = getPixel(posterisedImage, x, y)
      pix2 = getPixel(sobelThresholdImage, x, y)
      if getRed(pix2) < 200:#amount to ensure that all red pixels are transferred over 
        newRed = getRed(pix2)
        newGreen =  getGreen(pix2)
        newBlue =  getBlue(pix2)
        newColour = makeColor(newRed, newGreen, newBlue)
        setColor(pix1, newColour)
        
  mergedImage = makeEmptyPicture(getWidth(posterisedImage),getHeight(posterisedImage))#creates a copy of the posterised picture

  for x in range(0,getWidth(posterisedImage)):
    for y in range(0, getHeight(posterisedImage)):
      color = getColor(getPixel(posterisedImage, x,y))
      setColor(getPixel(mergedImage,x,y),color)

  show(mergedImage) 
  return(mergedImage)                    


#Output 2 images side by side with a black border
def ouputOriginalAndFinalImages(pictureCopy, mergedImagePic):
    canvas = makeEmptyPicture((getWidth(pictureCopy) * 2) + 6, (getHeight(pictureCopy) + 4))#+6 and +4 to allow for border to be added to canvas
    targetX = 2#border will be located in 0 and 1
    
    for sourceX in range(0,getWidth(pictureCopy)):
        targetY = 2
        for sourceY in range(0,getHeight(pictureCopy)):
            color = getColor(getPixel(pictureCopy,sourceX,sourceY))
            setColor(getPixel(canvas,targetX,targetY),color)
            targetY = targetY + 1
        targetX = targetX + 1
 
    targetX = getWidth(mergedImagePic)+4#+4 to allow for border to not overlay picture
    
    for sourceX in range(0,getWidth(mergedImagePic)):
        
        targetY = 2
        for sourceY in range(0,getHeight(mergedImagePic)):
            color = getColor(getPixel(mergedImagePic,sourceX,sourceY))
            setColor(getPixel(canvas,targetX,targetY),color)
            targetY = targetY + 1
        targetX = targetX + 1
       
    addRectFilled(canvas,0,0,getWidth(canvas),2,black)#top border
    addRectFilled(canvas,0,0,2,getHeight(canvas),black)#left side
    addRectFilled(canvas,getWidth(canvas)-2,0,2,getHeight(canvas),black)#right side
    addRectFilled(canvas,0,getHeight(canvas)-2,getWidth(canvas),2,black)#bottom
    addRectFilled(canvas,getWidth(pictureCopy)+2,0,2,getHeight(canvas),black)#middle
    repaint(canvas)
    return(canvas) 
