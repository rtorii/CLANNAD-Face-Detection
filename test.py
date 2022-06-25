from keras.models import load_model
from PIL import Image
import cv2
import numpy as np
import os

characters = ["Fuko","Kotomi","Kyou","Nagisa","Ryou","Youhei","Tomoya","Tomoyo"]

colors = [
(0,128,0), #green
(216,191,216),#thistle
(128,0,128),#purple
(255,248,220),#cornsilk
(255,0,255), #fuchsia
(255,255,0),#yellow
(0,0,128), #navy
(192,192,192)# silver
]

# @st.cache(allow_output_mutation=True)
def load_nnmodel():
    model = load_model("model_200_160_80_epoch30_30.h5")
    return model

def main():
    model = load_nnmodel()
    anime_cascade = cv2.CascadeClassifier('lbpcascade_animeface.xml') #save lbpcascade_animeface.xml in the samme directory as test.py
    input_img = cv2.imread('test_pics/clannad-1.jpeg',1) #  test image
    img_gray=cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
    faces=anime_cascade.detectMultiScale(img_gray, scaleFactor=1.1, minNeighbors=2, minSize=(10,10))#
    if len(faces)>0:
        for (x,y,w,h) in faces:
            face = input_img[y:y+h, x:x+w]
            face_rgb = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_rgb = Image.fromarray(face_rgb)
            face_rgb = np.array(face_rgb.resize((100,100)))
            face_rgb = face_rgb.transpose(2, 0, 1)
            face_rgb = face_rgb.reshape(1, face_rgb.shape[0] * face_rgb.shape[1] * face_rgb.shape[2]).astype("float32")[0]
            result = np.argmax(model.predict(np.array([face_rgb / 255])), axis=-1)
            # print(characters[result[0]])
            cv2.rectangle(input_img, pt1=(x, y), pt2=(x+w, y+h), color=colors[result[0]], thickness=3, lineType=cv2.LINE_8, shift=0)
            cv2.putText(input_img, text=characters[result[0]], org=(x+1, y-1), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=colors[result[0]], thickness=3, lineType=cv2.LINE_4)
    cv2.imshow("face",input_img)
    cv2.waitKey(0)



if __name__ == '__main__':
    main()
