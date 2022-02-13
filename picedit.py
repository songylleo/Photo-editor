import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math


def change_brightness(image, value):
    image1 = image.copy()
    length = len(image[0])
    width = len(image)
    for r in range(0,width):
        for c in range(0,length):
            image1[r,c,0]=image[r,c,0]+value
            image1[r,c,1]=image[r,c,1]+value
            image1[r,c,2]=image[r,c,2]+value
    for r in range(0,width):
        for c in range(0,length):
            for i in range(3):
                if image1[r,c,i]<0:
                    image1[r,c,i]=0
                elif image1[r,c,i]>255:
                    image1[r,c,i]=255
    return np.array(image1) 
    

def change_contrast(image, value):
    image1 = image.copy()
    length = len(image[0])
    width = len(image)
    F=259*(value+255)/(255*(259-value))
    for r in range(0,width):
        for c in range(0,length):
            image1[r,c,0]=F*(image[r,c,0]-128)+128
            image1[r,c,1]=F*(image[r,c,1]-128)+128
            image1[r,c,2]=F*(image[r,c,2]-128)+128
    for r in range(0,width):
        for c in range(0,length):
            for i in range(3):
                if image1[r,c,i]<0:
                    image1[r,c,i]=0
                elif image1[r,c,i]>255:
                    image1[r,c,i]=255
    return np.array(image1)


def grayscale(image):
    image1 = image.copy()
    length = len(image[0])
    width = len(image)
    for r in range(0,width):
        for c in range(0,length):
            image1[r,c,0] = 0.3 * image[r,c,0] + 0.59 * image[r,c,1] + 0.11 * image[r,c,2]
            image1[r,c,1] = 0.3 * image[r,c,0] + 0.59 * image[r,c,1] + 0.11 * image[r,c,2]
            image1[r,c,2] = 0.3 * image[r,c,0] + 0.59 * image[r,c,1] + 0.11 * image[r,c,2]
    for r in range(0,width):
        for c in range(0,length):
            for i in range(3):
                if image1[r,c,i]<0:
                    image1[r,c,i]=0
                elif image1[r,c,i]>255:
                    image1[r,c,i]=255
    return np.array(image1) 

def blur_effect(image):
    length = len(image[0])
    width = len(image)
    image2 = image.copy()
    for r in range(1,width-1):
        for c in range(1,length-1):
            for i in range(0,3):
                image2[r,c,i] = 0.0625 * image[r-1,c-1,i] + 0.125 * image[r-1,c,i] + 0.0625 * image[r-1,c+1,i] + \
                                0.125 * image[r,c-1,i] + 0.25 * image[r,c,i] + 0.125 * image[r,c+1,i] + \
                                0.0625 * image[r+1,c-1,i] + 0.125 * image[r+1,c,i] + 0.0625 * image[r+1,c+1,i]
    for r in range(0,width):
        for c in range(0,length):
            for i in range(3):
                if image[r,c,i]<0:
                    image[r,c,i]=0
                elif image[r,c,i]>255:
                    image[r,c,i]=255
    return np.array(image2) 

def edge_detection(image):
    length = len(image[0])
    width = len(image)
    image3 = image.copy() 
    for r in range(1, width-1):
        for c in range(1, length-1):
            for i in range(0,3):
                image3[r,c,i] = (-1) * image[r-1,c-1,i] + (-1) * image[r-1,c,i] + (-1) * image[r-1,c+1,i] + \
                                (-1) * image[r,c-1,i] + 8 * image[r,c,i] + (-1) * image[r,c+1,i] + \
                                (-1) * image[r+1,c-1,i] + (-1) * image[r+1,c,i] + (-1) * image[r+1,c+1,i] + 128
                if image3[r,c,i] < 0:
                    image3[r,c,i] = 0
                elif image3[r,c,i] > 255:
                    image3[r,c,i] = 255
    return np.array(image3)


def embossed(image):
    length = len(image[0])
    width = len(image)
    image4 = image.copy() 
    for r in range(1, width-1):
        for c in range(1, length-1):
            for i in range(0,3):
                image4[r,c,i] = -1 * image[r-1,c-1,i] + (-1) * image[r-1,c,i]+ \
                                (-1)* image[r,c-1,i] + 1 * image[r,c+1,i]+ \
                                1 * image[r+1,c,i] + 1 * image[r+1,c+1,i] + 128
                if image4[r,c,i]<0:
                    image4[r,c,i]=0
                elif image4[r,c,i]>255:
                    image4[r,c,i]=255
                else:
                    continue

    return np.array(image4)

def rectangle_select(image, x, y):

    mask2 = np.zeros((len(image), len(image[0])))
    for i in range(int(x[0]),int(y[0])+1):
        for j in range(int(x[1]),int(y[1])+1):
            mask2[i,j] = 1
    latest_mask = mask2
    return np.array(mask2)


               
def magic_wand_select(image, x, thres):                

    checked = np.zeros ((len(image), len(image[0])),dtype=bool)
    length=len(image[0])
    width = len(image)
    x1=int(x[0])
    x2=int(x[-1])
    selection = [[x1,x2]]                  
    while selection!=[]:              
        m,n = selection[-1]                
        checked[m][n] = 1            
        selection.pop()
        for row in (m-1,m+1):
          c=n
          if 0<=row<width and 0<=c<length:
            r = 1/2*(image[row,c,0]+image[x1,x2,0])
            delta_RED = image[row,c,0]-image[x1,x2,0]
            delta_GREEN = image[row,c,1]-image[x1,x2,1]
            delta_BLUE = image[row,c,2]-image[x1,x2,2]
            distance = math.sqrt((2+r/256)*((delta_RED)**2)+4*((delta_GREEN)**2)+(2+(255-r)/256)*((delta_BLUE)**2))

            if checked[row][c]==0:
                if distance<=thres:
                    selection.append([row,c])
        for c in (n-1,n+1):
          row=m
          if 0<=row<width and 0<=c<length:
                r = 1/2*(image[row,c,0]+image[x1,x2,0])
                delta_RED = image[row,c,0]-image[x1,x2,0]
                delta_GREEN = image[row,c,1]-image[x1,x2,1]
                delta_BLUE = image[row,c,2]-image[x1,x2,2]
                distance = math.sqrt((2+r/256)*((delta_RED)**2)+4*((delta_GREEN)**2)+(2+(255-r)/256)*((delta_BLUE)**2))

                if checked[row][c]==0:
                    if distance<=thres:
                        selection.append([row,c])
                    
 
    mask3 = np.zeros ((len(image), len(image[0])))   
    for i in range (0, width):
        for j in range (0, length):
            if checked[i][j] == True:
                mask3 [i][j] = 1
    latest_mask=mask3      
    return np.array(mask3)
def compute_edge(mask):           
    rsize, csize = len(mask), len(mask[0]) 
    edge = np.zeros((rsize,csize))
    if np.all((mask == 1)): return edge        
    for r in range(rsize):
        for c in range(csize):
            if mask[r][c]!=0:
                if r==0 or c==0 or r==len(mask)-1 or c==len(mask[0])-1:
                    edge[r][c]=1
                    continue
                
                is_edge = False                
                for var in [(-1,0),(0,-1),(0,1),(1,0)]:
                    r_temp = r+var[0]
                    c_temp = c+var[1]
                    if 0<=r_temp<rsize and 0<=c_temp<csize:
                        if mask[r_temp][c_temp] == 0:
                            is_edge = True
                            break
    
                if is_edge == True:
                    edge[r][c]=1
            
    return edge

def save_image(filename, image):
    img = image.astype(np.uint8)
    mpimg.imsave(filename,img)

def load_image(filename):
    img = mpimg.imread(filename)
    if len(img[0][0])==4: 
        img = np.delete(img, 3, 2)
    if type(img[0][0][0])==np.float32: 
        img = img*255
        img = img.astype(np.uint8)
    mask = np.ones((len(img),len(img[0]))) 
    img = img.astype(np.int32)
    return img, mask

def display_image(image, mask):
    
    tmp_img = image.copy()
    edge = compute_edge(mask)
    for r in range(len(image)):
        for c in range(len(image[0])):
            if edge[r][c] == 1:
                tmp_img[r][c][0]=255
                tmp_img[r][c][1]=0
                tmp_img[r][c][2]=0
 
    plt.imshow(tmp_img)
    plt.axis('off')
    plt.show()
    print("Image size is",str(len(image)),"x",str(len(image[0])))

def menu():
    
    img = mask = np.array([])
    print("What do you want to do ?")
    print("e - exit")
    print("l - load a picture")
    print()
    choicenum=input("Your choice: ")
    if choicenum=='e':
        pass
    elif choicenum=='l':
        filename=input("Please enter the filename: ")
        while True:
            try:  
                load_image(filename)
                break
            except IOError:
                filename=input("Please enter a valid filename: ")
            except AttributeError:
                filename=input("Please enter a valid filename: ")
        latest_mask = load_image(filename)[1]
        display_image(load_image(filename)[0],latest_mask)
        original_img = load_image(filename)[0]
        img = load_image(filename)[0]
        newimg = img
        while True:
             print("What do you want to do ?")
             print("e - exit")
             print("l - load a picture")
             print("s - save the current picture")
             print("1 - adjust brightness")
             print("2 - adjust contrast")
             print("3 - apply grayscale")
             print("4 - apply blur")
             print("5 - edge detection")
             print("6 - embossed")
             print("7 - rectangle select")
             print("8 - magic wand select")
             print()
             choicenum=input("Your choice: ")
             if choicenum=='e':
                 break
             elif choicenum=='l':
                filename=input("Please enter the filename: ")
                while True:
                    try:  
                        load_image(filename)
                        break
                    except IOError:
                        filename=input("Please enter a valid filename: ")
                    except AttributeError:
                        filename=input("Please enter a valid filename: ")
                latest_mask = load_image(filename)[1]
                display_image(load_image(filename)[0],latest_mask)
                original_img = load_image(filename)[0]
                img = load_image(filename)[0]
                newimg = img

             elif choicenum=='s':
                 file_saved = input("Please enter the filename: ")
                 while True:
                     try:  
                         save_image(file_saved,newimg)
                         break
                     except ValueError:
                         file_saved = input("Please enter a valid filename: ")
                     except KeyError:
                         file_saved = input("Please enter a valid filename: ")
                         
                 print ("The image is saved successfully")
                 
             elif choicenum=='1':
                 
                  value=input("Please enter the value: ")
                  while value.isdigit()==0 or int(value)>255 or int(value)<-255:
                      value=input("Please enter an integer value(in digit and between -255 and 255):")
          
                  value=int(value)
                  
                  img = change_brightness(img,value)
                 
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])
                  
                  
             elif choicenum=='2':
                 
                  value=input("Please enter the value: ")
                  while value.isdigit()==0 or int(value)>255 or int(value)<-255:
                    value=input("Please enter an integer value(in digit and between -255 and 255):")
          
                  value=int(value)
                  img = change_contrast(img,value)
                  
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])
                  
             elif choicenum=='3':
                 
                  img = grayscale(img)
                  
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])

             elif choicenum=='4':
                 
                  img = blur_effect(img)
                 
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])
          
             elif choicenum=='5':
                  img = edge_detection(img)
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])
             elif choicenum=='6':
                  img = embossed(img)
                  length = len(img[0])
                  width = len(img)
                  newimg = img.copy()
                  for r in range(0,width):
                      for c in range(0,length):
                          if latest_mask[r,c] == 0:
                                   newimg[r,c,0]=original_img[r,c,0]
                                   newimg[r,c,1]=original_img[r,c,1]
                                   newimg[r,c,2]=original_img[r,c,2]                               
                  display_image(newimg, load_image(filename)[1])
             elif choicenum=='7':
                 original_img = newimg.copy()
                 img = newimg.copy()
                 start_up = 0
                 while start_up != 1:
                     x=str(input("Enter a top left pixel position(e.g. 3,4 ) : "))           
                     y=str(input("Enter a bottom right pixel position(e.g. 3,4): "))
                     if x.count(',') != 1:
                            print("Please seperate the coordinates by one comma.")
                     elif y.count(',') != 1:
                            print("Please seperate the coordinates by one comma.")
                     else:
                            x1 = x[0:x.find(',')]
                            x2 = x[x.find(',')+1:]
                            y1 = y[0:y.find(',')]
                            y2 = y[y.find(',')+1:]
                            if x1.isdigit() == False or\
                               x2.isdigit() == False or\
                               y1.isdigit() == False or\
                               y2.isdigit() == False or\
                               int(x1) < 0 or int(x1) > len(img)-1 or\
                               int(x2) < 0 or int(x2) > len(img[0])-1 or\
                               int(y1) < 0 or int(y1) > len(img)-1 or\
                               int(y2) < 0 or int(y2) > len(img[0])-1 or\
                               int(x1) > int(y1) or int(x2) > int(y2):
                                   print("Please enter an integer coordinate within the length",len(img)-1,"and width",len(img[0])-1)
                                   print("The value of the bottom right coordinate shounld not be smaller than the top left coordinate.")
                            else:
                                start_up = 1
                 a = tuple([x1,x2])
                 b = tuple([y1,y2])
                 latest_mask = rectangle_select(img, a, b)
                 display_image(newimg, latest_mask)
                 print("Mask selection done.")

             elif choicenum=='8':
                 original_img = newimg.copy()
                 img = newimg.copy()
                 x=input("Enter a pixel position in the form a,b(e.g. 1,2): ")
                 
                 length = len(img[0])
                 width = len(img)
                 x1=x[0:x.find(',')]
                 x2=x[x.find(',')+1:]
                 while x1.isdigit()==0 or x2.isdigit()==0 \
                 or int(x1)<0 or int(x1)>=width \
                 or int(x2)<0 or int(x2)>=length\
                 or x.count(',')!=1:
                     x=input("(ATTENTION:/1.SEPERATE WITH COMMA /2.IN DIGIT FORM /3.MUST BE IN THE RANGE) e.g 1,2: ")
                     x1=x[0:x.find(',')]
                     x2=x[x.find(',')+1:]
                     
                     
                 x1=int(x1)
                 x2=int(x2)
                
                         
                 a=tuple([x1,x2])
                 thres=input("Enter a threshold value: ")
                 while thres.count('.') > 1:
                     thres=input("Enter a threshold value (There must be at most one decimal point): ")
                 i = 0
                 while i == 0:
                     if thres.count('.') == 1:
                         check_thres = thres[0:thres.find('.')] + thres[thres.find('.')+1:]
                         if check_thres.isdigit() == 0:
                             thres=input("Enter a threshold value (!in digit!): ")
                             i = 0
                         else:
                             i = 1
                     else:
                         if thres.isdigit() == 0:
                             thres=input("Enter a threshold value (!in digit!): ")
                             i = 0
                         else:
                             i = 1
                 thres=float(thres)
                 latest_mask = magic_wand_select(img,a,thres)
                 display_image(newimg, latest_mask)
                 print("Mask selection done.")
             else:
                 print("Please follow the instruction !")
                 print()
                 continue
    
    else:
        print("Please enter 'e' or 'l'")
        print()
        return menu()

if __name__ == "__main__":
    menu()



 