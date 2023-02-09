import numpy as np
import cv2

img255 = 0
img0 = 0


def loadImage(imgPath):
    img = cv2.imread(imgPath, 0)
    thresh, img = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return img


def makeConnectedComponents(img):
    connections = np.zeros((len(img), len(img[0])))
    numbersUsed = [0]
    conns = {}
    for row in range(len(img)):
        for column in range(len(img[row])):
            if img[row, column] == 0:
                if img[row - 1, column] == 255 and img[row, column - 1] == 255:
                    connections[row, column] = max(numbersUsed) + 1
                    numbersUsed.append(max(numbersUsed) + 1)
                    conns[connections[row, column]] = connections[row, column]
                elif img[row - 1, column] == 255 and img[row, column - 1] == 0:
                    connections[row, column] = connections[row, column - 1]
                elif img[row - 1, column] == 0 and img[row, column - 1] == 255:
                    connections[row, column] = connections[row - 1, column]
                elif img[row - 1, column] == 0 and img[row, column - 1] == 0:
                    connections[row, column] = min(connections[row - 1, column], connections[row, column - 1])
    for i in range(3):
        for row in range(len(connections)):
            for column in range(len(connections[row])):
                if connections[row, column] != 0:
                    if connections[row, column] != connections[row, column + 1] and connections[row, column + 1] != 0:
                        conns[connections[row, column]] = min(conns[connections[row, column + 1]],
                                                              conns[connections[row, column]])
                    elif connections[row + 1, column] and connections[row, column] != connections[row + 1, column] and \
                            connections[row + 1, column] != 0:
                        conns[connections[row, column]] = min(conns[connections[row + 1, column]],
                                                              conns[connections[row, column]])
                    elif connections[row - 1, column] and connections[row, column] != connections[row - 1, column] and \
                            connections[row - 1, column] != 0:
                        conns[connections[row, column]] = min(conns[connections[row - 1, column]],
                                                              conns[connections[row, column]])
                    elif connections[row, column - 1] and connections[row, column] != connections[row, column - 1] and \
                            connections[row, column - 1] != 0:
                        conns[connections[row, column]] = min(conns[connections[row, column - 1]],
                                                              conns[connections[row, column]])

    for row in range(len(connections)):
        for column in range(len(connections[row])):
            if connections[row, column] != 0 and connections[row, column] in conns:
                connections[row, column] = conns[connections[row, column]]
    return connections

def getBoundingBoxes(img):
    bounding = {}

    for row in range(len(img)):
        for column in range(len(img[row])):
            if img[row, column] != 0 and img[row, column] not in bounding:
                bounding[img[row, column]] = {'rowmin': row,
                                               'rowmax': row,
                                               'colmin': column,
                                               'colmax': column}
            elif img[row, column] != 0 and img[row, column] in bounding:
                bounding[img[row, column]]['rowmin'] = min(bounding[img[row, column]]['rowmin'], row)
                bounding[img[row, column]]['rowmax'] = max(bounding[img[row, column]]['rowmax'], row)
                bounding[img[row, column]]['colmin'] = min(bounding[img[row, column]]['colmin'], column)
                bounding[img[row, column]]['colmax'] = max(bounding[img[row, column]]['colmax'], column)

    print(bounding)
    for i in bounding:
        for row in range(bounding[i]['rowmin'], bounding[i]['rowmax']):
            img[row, bounding[i]['colmin']] = i
            img[row, bounding[i]['colmax']] = i
        for column in range(bounding[i]['colmin'], bounding[i]['colmax']):
            img[bounding[i]['rowmin'], column] = i
            img[bounding[i]['rowmax'], column] = i

    print(bounding)
    return img

def cleanImg(img):
    unique = []
    for i in cons:
        for j in i:
            if j not in unique:
                unique.append(j)

    print(len(unique))

    labels = {}

    for row in img:
        for j in row:
            if j not in labels:
                labels[j] = 1
            else:
                labels[j] += 1

    for row in range(len(img)):
        for column in range(len(img[row])):
            if (labels[img[row, column]] < 10):
                img[row, column] = 0

    unique = []
    for i in img:
        for j in i:
            if j not in unique:
                unique.append(j)

    print(unique)
    print(len(unique))
    return unique, img

def colorizeImage(img, unique):
    colors = {}

    for i in unique:
        colors[i] = [np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255)]

    newimg = np.zeros((int(len(img)), int(len(img[0])), 3))

    for row in range(len(img)):
        for column in range(len(img[row])):
            if img[row, column] != 0:
                newimg[row, column] = colors[cons[row, column]]

    return newimg

def saveShowImage(img):
    cv2.imwrite('color_img.jpg', img)
    img = cv2.imread('color_img.jpg')
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



img = loadImage('cc_input.png')

cons = makeConnectedComponents(img)
unique, cons = cleanImg(cons)
#cons = getBoundingBoxes(cons)
cons = colorizeImage(cons, unique)
saveShowImage(cons)



