import argparse
import cv2
import pathlib
import os
import sys
import numpy as np
import yaml


# create two variable fx, fy where you define the function
def draw_line(event,x,y,flag,param):
    global fx, fy, new_x, new_y
    if event == cv2.EVENT_LBUTTONDOWN:
        if fx == -1 & fy == -1:
            fx, fy = x, y
            new_x, new_y = x, y # to draw the fouth line automatically
        else:
            cv2.line(frame,(fx,fy),(x,y),(247,174,7),3)
            fx, fy = x, y 
    print(" the value of fx = {}, fy = {}, new_x = {}, new_y = {}".format(fx,fy,new_x,new_y))

def putText():
    global frame
    XminAll = np.min([cord_list[0][0],cord_list[1][0],cord_list[2][0],cord_list[3][0]])
    XmaxAll = np.max([cord_list[0][0],cord_list[1][0],cord_list[2][0],cord_list[3][0]])
    midx = XminAll + (XmaxAll-XminAll)//2
    midy = np.abs(cord_list[0][1] + cord_list[2][1])//2
    serial = input("Enter the ID number of the selected space\n")
    frame = cv2.putText(frame, str(serial), (midx,midy), cv2.FONT_HERSHEY_SIMPLEX,.5, (7,247,57),1,cv2.LINE_AA)
    return int(midx),int(midy),serial

def putTextRectangle(point1,point2,ID):
    global frame
    midx = (point1[0] + point2[0])//2
    midy = (point1[1] + point2[1])//2
    cv2.putText(frame, str(ID), (midx,midy), cv2.FONT_HERSHEY_SIMPLEX,.5, (247,7,57),1,cv2.LINE_AA)

def draw_fourcorners(event, x, y , param, flag):
    global n, fx, fy, new_x, new_y, cord_list, cord_list_dict
    if event == cv2.EVENT_LBUTTONDOWN:
        print("The value of n - ", n)
        if n >= 5:  # new assignment of all global variable
            n = 1
            fx, fy, new_x, new_y = -1, -1, -1, -1  
        if n <= 3:
            draw_line(event,x,y, flag, param)
            cord_list.append((x,y))
            n += 1
        else:  
            draw_line(event,x,y,flag,param)
            cord_list.append((x,y))
            draw_line(event,new_x, new_y, flag, param) # drawing the fourth line
            x1, y1,ID = putText()
            cord_list.append((x1,y1,ID))
            cord_list_dict[ID] = cord_list
            #file_path = pathlib.Path.cwd().joinpath('required_text_file',"four_corners_cordinate.txt")
            #with open(file_path,'a') as cordinate:
                #cordinate.writelines(str(cord_list))
                #cordinate.writelines("\n")
            cord_list = []            
            n+=1   


def draw_rectangles(event,x,y,param,flag):
    global point1, point2, drawing,frame, x_cord,y_cord, cord_list,key_min, pointsDict
    
    #draw rectangles with point1 and point2
    if event == cv2.EVENT_LBUTTONDOWN:
        if drawing is False:
            point1 = x,y
            point2 = ()
            drawing = True
        else:
            drawing = False
            ID = input("Enter the Id number of the selected space\n")
            pointsDict[ID] = [point1,point2]          # in points we have all the rectangles
            
    
    #for continues rectangles
    if event == cv2.EVENT_MOUSEMOVE:
        x_cord, y_cord = x,y
        if drawing is True:
            point2 = x,y

    # to remove a point


    if event == cv2.EVENT_RBUTTONDOWN: 
        if bool(pointsDict):
            for n,[item1, item2] in enumerate(pointsDict.values()):
                if x >= item1[0] and x <= item2[0]:
                    if y >= item1[1] and y<=item2[1]:
                        cord_list.append([item1,item2,list(pointsDict.keys())[n]])  #took all the values of intersecting rectangles
            if len(cord_list)==1:
                key_min = cord_list[0][2]  #If the rectangle is one we will delete it.
                cord_list = []
            elif cord_list!=[]:
                distance = {}   #else we measure the distance of all rectangles from the selected point and delete the nearest rectangles.
                for row1, row2, row3 in cord_list:
                    dist = np.abs(x - row1[0]) + np.abs(x - row2[0]) + np.abs(y - row1[1]) + np.abs(y - row2[1])  #taking the distance of the points to delete the nearset point 
                    distance[row3] = dist
                key_min = min(distance.keys(), key = (lambda k: distance[k]))
                cord_list = []
            


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--four_corners', action = 'store_true', help = 'Take every four corners')
    parser.add_argument('--rectangles', action = 'store_true', help = 'Take two corners of rectangles')
    parser.add_argument('--data', type =str, help = 'data directory to save the files')
    parser.add_argument('--source', type = str, help = 'Image file name')
    opt = parser.parse_args()
    source_image = opt.source
    #if source_image.exists():
    frame = cv2.imread(source_image, cv2.IMREAD_UNCHANGED)
    #else:
        #print("Source path does not exists")

    if opt.four_corners:
        n = 1
        fx, fy, new_x, new_y = -1, -1, -1, -1
        cord_list = []
        cord_list_dict = {}
        print('height : {} width : {}'.format(frame.shape[0], frame.shape[1]))
        
        delete_existing_file = input("\nWarning - It will delete the existing file in directory {} if any. \nDo you want to proceed?\n 'Y' or 'N'\n".format(opt.data))
        if delete_existing_file.lower() == 'n' or delete_existing_file.lower() == 'no' :
            print("Execution Stopped.......")
            sys.exit()
        elif delete_existing_file.lower() == 'y' or delete_existing_file.lower() == 'yes' :
            cv2.namedWindow('Four Corners Image')
            cv2.setMouseCallback('Four Corners Image', draw_fourcorners)
            while True:
                cv2.imshow('Four Corners Image',frame)
                k = cv2.waitKey(1) & 0xff
                if k == 27 or k == ord('q'):
                    break
            cv2.destroyAllWindows()
            data = opt.data
            with open(data) as file:
                parsed_yaml_file = yaml.load(file, Loader = yaml.FullLoader)
            filepath = parsed_yaml_file['four_corners']
            file_path = pathlib.Path.cwd().joinpath(filepath)
            with open(file_path, 'w') as file:
                documents = yaml.dump(cord_list_dict, file)
        else:
            print("\nPlease input correctly\n")
            sys.exit()
    

    if opt.rectangles:
        delete_existing_file = input("\nWarning - It will delete the existing file. \nDo you want to proceed?\n 'Y' or 'N'\n")
        if delete_existing_file.lower() == 'n' or delete_existing_file.lower() == 'no' :
            print("Execution Stopped.......")
            sys.exit()
            
        point1, point2 = (), ()
        pointsDict = {}
        x_cord, y_cord, key_min = -1, -1, -1  #key_min to delete an item
        drawing = False
        cord_list = []
        cv2.namedWindow('Rectangle Image')
        cv2.setMouseCallback('Rectangle Image',draw_rectangles)
        while True:
            frame = cv2.imread(source_image, cv2.IMREAD_UNCHANGED)
        
            #draw the perpendicular lines on screen
            if x_cord != -1 and y_cord != -1:  
                cv2.line(frame,(0,y_cord),(frame.shape[1],y_cord),(255,0,255),2)
                cv2.line(frame,(x_cord,0),(x_cord,frame.shape[0]),(255,0,255),3)
            
            #draw the continuos rectangle for drawing purpose 
            if point1 and point2:
                cv2.rectangle(frame,point1,point2, (0,255,0),2)

            #to delete the rectangle before printing in the frame
            if key_min != -1:  
                print("Now to be deleted",key_min)
                del pointsDict[key_min]
                key_min = -1
            
            #print rectangles
            for ID,[item1,item2] in pointsDict.items():
                cv2.rectangle(frame,item1,item2, (0,255,0),2)
                putTextRectangle(item1,item2,ID)

            cv2.imshow('Rectangle Image', frame)
            k = cv2.waitKey(1) & 0xff
            if k == 27 or k == ord('q'):
                break
        cv2.destroyAllWindows()
        data = opt.data
        with open(data) as file:
            parsed_yaml_file = yaml.load(file, Loader = yaml.FullLoader)
        filepath = parsed_yaml_file['rectangle_cordinates']
        file_path = pathlib.Path.cwd().joinpath(filepath)
        with open(file_path, 'w') as file:
            documents = yaml.dump(pointsDict, file)
