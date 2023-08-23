import cv2
import os
import numpy as np

current_matrix1 = []
current_matrix2 = []

flag = 0
buffer_idx = 0
cam = 0

MAX_POINT = 4
DATA_PATH = 'C:/Users/User/OneDrive/Desktop/projects/images/homography_matrix'
img1 = 0
img2 = 0
img_zoom = 0
num = 0

def load_img_matrix(path, idx) :
    global current_matrix1
    global current_matrix2
    global matrix_buffer

    if os.path.isfile(path + '/go/test1_{0:04d}.jpg'.format(idx)):
        img_2 = cv2.imread(path + '/go/test1_{0:04d}.jpg'.format(idx))
        img_2 = cv2.resize(img_2, dsize = (1000,1000))
        img_1 = cv2.imread(path + '/back/test2_{0:04d}.jpg'.format(idx))
        if not os.path.isfile(path+'/matrix/matrix_{0:04d}.txt'.format(idx)):
            print('check')
            f = open(path+'/matrix/matrix_{0:04d}.txt'.format(idx),'w')
            f.close
        matrix = open(path+'/matrix/matrix_{0:04d}.txt'.format(idx),'r')
        current_matrix1 = matrix.readline().split()
        current_matrix2 = matrix.readline().split()
        
        for i, _str in enumerate(current_matrix1):
            current_matrix1[i] = tuple(map(int, _str.split(',')))
        for i, _str in enumerate(current_matrix2):
            current_matrix2[i] = tuple(map(int, _str.split(',')))

        print_current_matrix(idx)
        matrix.close()
        
        return img_1, img_2
    else :
        print("error : no file exist")
        quit()
    
def print_current_matrix(idx) :
    global current_matrix1
    global current_matrix2
    print("current file num : {0:04d}".format(idx))
    if cam == 1 :
        print("current file : camera image")
    else :
        print("current file : monitor image")
    print("matrix1 : ", current_matrix1)
    print("matrix2 : ", current_matrix2)
    print()

def mouse_callback(event, x, y, flags, param) :
    idx = 0
    global img1
    global img2
    global img_zoom
    global current_matrix1
    global current_matrix2

    img = 0

    if cam == 0:
        img = img1
    else :
        img = img2
    img = cv2.copyMakeBorder(img, 50,50,50,50, cv2.BORDER_CONSTANT)
    img_zoom = img[y:y+100, x:x+100,:].copy()
    img_zoom = cv2.resize(img_zoom, dsize = (400,400), interpolation=cv2.INTER_LINEAR)

    cv2.circle(img_zoom, center=(200,200), radius = 10, color = (0,0,255), thickness=1, lineType=cv2.LINE_AA)
    cv2.line(img_zoom, (200, 190), (200,210), color = (0,0,255), thickness = 1, lineType=cv2.LINE_AA)
    cv2.line(img_zoom, (190, 200), (210,200), color = (0,0,255), thickness = 1, lineType=cv2.LINE_AA)
    
    cv2.imshow('zoom',img_zoom)

    if event == cv2.EVENT_FLAG_LBUTTON:
        
        if cam == 0:
            if len(current_matrix1) == 4 :
                print("error : already 4 point is saved")
            else :
                current_matrix1.append((x,y))

        elif cam == 1:
            if len(current_matrix2) == 4 :
                print("error : already 4 point is saved")
            else :
                current_matrix2.append((x,y))

        print_current_matrix(idx = num)

    if event == cv2.EVENT_FLAG_RBUTTON:
        
        if cam == 0:
            if len(current_matrix1) == 0 :
                print("error : no point is saved")
            else :
                idx = len(current_matrix1) - 1
                current_matrix1.pop(idx)

        elif cam == 1:
            if len(current_matrix2) == 0 :
                print("error : no point is saved")
            else :
                idx = len(current_matrix2) - 1
                current_matrix2.pop(idx)
                
        save_point(path=DATA_PATH, idx = num)
        img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)
        print_current_matrix(idx = num)

def draw_point(img) :
    
    matrix = []
    
    if cam == 0:
        for idx, ((x,y)) in enumerate(current_matrix1):
            cv2.circle(img, center = (x,y), radius = 10, color = (255,255,0), lineType=cv2.LINE_AA)  
    else :
        for idx, ((x,y)) in enumerate(current_matrix2):
            cv2.circle(img, center = (x,y), radius = 10, color = (0,255,255), lineType=cv2.LINE_AA)

    



def save_point(path, idx):
    matrix_buffer = open(path+'/matrix/matrix_{0:04d}.txt'.format(idx),'w')

    for idx in range(len(current_matrix1)):
        x = str(current_matrix1[idx][0])+','+str(current_matrix1[idx][1])+' '
        matrix_buffer.write(x)
    matrix_buffer.write('\n')

    for idx in range(len(current_matrix2)):
        y = str(current_matrix2[idx][0])+','+str(current_matrix2[idx][1])+' '
        matrix_buffer.write(y)
    matrix_buffer.write('\n')

    matrix_buffer.close()
    

if __name__ == "__main__" :

    cv2.namedWindow('image')
    cv2.namedWindow('zoom')
    cv2.setMouseCallback('image', mouse_callback)
    num = 0
    total_file_num = len(os.listdir(path=DATA_PATH +'/test1/'))
    print(total_file_num)

    img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)
    
    while True :
        if cam == 0 :
            img = img1
        else :
            img = img2

        draw_point(img=img)
        cv2.imshow('image', img)

        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            save_point(path=DATA_PATH, idx = num)
            print("exit")
            break
        elif k == 97:
            cam = 0
            save_point(path=DATA_PATH, idx = num)
            img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)
        elif k == 100:
            cam = 1
            save_point(path=DATA_PATH, idx = num)
            img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)

        elif k == 101:
            save_point(path=DATA_PATH, idx = num)
            num += 1
            if not num > (total_file_num-1):
                img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)

            else :
                num -= 1
        elif k == 113:
            save_point(path=DATA_PATH, idx = num)
            num -= 1
            if not num < 0:
                img1, img2 = load_img_matrix(path=DATA_PATH, idx = num)

            else :
                num += 1

    cv2.destroyAllWindows