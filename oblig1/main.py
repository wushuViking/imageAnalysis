import numpy as np
import cv2

img255 = 0
img0 = 0

#function for loading an img
def loadImage(imgPath):
    img = cv2.imread(imgPath, 0)
    thresh, img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img



#function for finding all the connected components
def makeConnectedComponents(img):
    #initilizing connected components array
    connections = np.zeros((len(img), len(img[0])))
    numbersUsed = 0
    conns = {}
    #Loop through the img
    for row in range(len(img)):
        for column in range(len(img[row])):
            #checking if pixel is white or black
            if img[row,column] == 0:
                #finding the neighbors
                neighbors = [connections[row, column-1], connections[row-1, column-1], connections[row-1, column], connections[row-1, column+1]]
                cconns = []
                #Checking if any of the neighbors have been found before
                for i in neighbors:
                    #Adding previously seen neighbors to an list
                    if i != 0:
                        cconns.append(conns[i])
                #if no previously found neighbors, giving it a value, one higher then the last one found, and incrementing the value
                if(len(cconns) == 0):
                    connections[row, column] = numbersUsed + 1
                    numbersUsed += 1
                    #adding the new value to the relathionship dict
                    conns[connections[row, column]] = connections[row, column]
                else:
                    #finds the neighbor with the lowest value
                    low = min(cconns)
                    #setting the current pixel to the lowest value
                    connections[row,column] = low
                    #updating the realtionship dict, to the lowest value for all the neighbors
                    for i in cconns:
                        conns[i] = low
    #looping through the new img
    for row in range(len(connections)):
        for column in range(len(connections[row])):
            #checking if the pixel is not 0 and is in the relationship dict
            if connections[row, column] != 0 and connections[row, column] in conns:
                #updating the pixel, to the value in the relationship dict
                connections[row, column] = conns[connections[row, column]]
    return connections


def cleanImg(img):
    unique = []
    #finding all the unique values in the image
    for i in cons:
        for j in i:
            if j not in unique:
                unique.append(j)

    print(len(unique))

    labels = {}
    #counting how many frames each value has
    for row in img:
        for j in row:
            if j not in labels:
                labels[j] = 1
            else:
                labels[j] += 1
    #looping through the img, setting all the pixels to 0, if the component has less pixels than the threshold
    for row in range(len(img)):
        for column in range(len(img[row])):
            if (labels[img[row, column]] < 20):
                img[row, column] = 0
    #finding all the new unique values in the pictures
    unique = []
    for i in img:
        for j in i:
            if j not in unique:
                unique.append(j)

    print(unique)
    print(len(unique))
    return unique, img


#function for making bounding boxes for the components
def getBoundingBoxes(img):
    bounding = {}

    #looping though the image, finding the range of the components
    for row in range(len(img)):
        for column in range(len(img[row])):
            #if the component is not seen before, add it to the dict
            if img[row, column] != 0 and img[row, column] not in bounding:
                bounding[img[row, column]] = {'rowmin': row,
                                              'rowmax': row,
                                              'colmin': column,
                                              'colmax': column}
            #if the component has been seen, update the ranges of the component
            elif img[row, column] != 0 and img[row, column] in bounding:
                bounding[img[row, column]]['rowmin'] = min(bounding[img[row, column]]['rowmin'], row)
                bounding[img[row, column]]['rowmax'] = max(bounding[img[row, column]]['rowmax'], row)
                bounding[img[row, column]]['colmin'] = min(bounding[img[row, column]]['colmin'], column)
                bounding[img[row, column]]['colmax'] = max(bounding[img[row, column]]['colmax'], column)

    totheight = 0
    totwidth = 0
    #finding the avergage height and widht of the components
    for i in bounding:
        totheight+= bounding[i]['rowmax']-bounding[i]['rowmin']
        totwidth += bounding[i]['colmax']-bounding[i]['colmin']
    averageh = totheight/len(bounding)
    averagew = totwidth/(len(bounding)-1)

    #looping though the bounding box dict
    for i in bounding:
        #checking if the component is larger than the average of all the components
        if(bounding[i]['rowmax']-bounding[i]['rowmin']) >= averageh and (bounding[i]['colmax']-bounding[i]['colmin']) >= averagew:
            #drawing the vertical lines of the bounding box
            for row in range(bounding[i]['rowmin'], bounding[i]['rowmax']):
                img[row, bounding[i]['colmin']] = i
                img[row, bounding[i]['colmax']] = i
            #drawing the horizontal lines of the bounding box
            for column in range(bounding[i]['colmin'], bounding[i]['colmax']):
                img[bounding[i]['rowmin'], column] = i
                img[bounding[i]['rowmax'], column] = i

    return img



def colorizeImage(img, unique):
    colors = {}
    #giving a random color to each of the unique components and their bounding boxes
    for i in unique:
        colors[i] = [np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255)]

    #initializing a new array, to use rgb colors
    newimg = np.zeros((int(len(img)), int(len(img[0])), 3))

    #adding all the components to the rgb image
    for row in range(len(img)):
        for column in range(len(img[row])):
            if img[row, column] != 0:
                newimg[row, column] = colors[cons[row, column]]

    return newimg

#function for saving an image
def saveShowImage(img):
    cv2.imwrite('color_img.jpg', img)
    img = cv2.imread('color_img.jpg')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#Loading the img
img = loadImage('cc_input.png')
#making all the connected components
cons = makeConnectedComponents(img)
#removing small components and noise
unique, cons = cleanImg(cons)
#adding bounding boxes
cons = getBoundingBoxes(cons)
#making the image an rgb image
cons = colorizeImage(cons, unique)
#saving the image
saveShowImage(cons)