import numpy as np
import cv2

class BoxSelect(object):
    def __init__(self, image, window_name,color=(0,0,255)):
        #görüntüyü saklar ve orjinal kopyasını oluşturur
        self.image = image
        self.orig = image.copy()
        #Başlangıc ve bitiş koordinatlarını yakalar
        self.start = None
        self.end = None
        self.track = False
        self.color = color
        self.window_name = window_name

        #Adlandırılan pencereyi geri cagırma
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name,self.mouseCallBack)

    def mouseCallBack(self, event, x, y, flags, params):
        #mouse'a sol tıklandıysa izleme baslatılır 
        if event==cv2.EVENT_LBUTTONDOWN:
            self.start = (x,y)
            self.track = True

        elif self.track and (event==cv2.EVENT_MOUSEMOVE or event==cv2.EVENT_LBUTTONUP):
            self.end = (x,y)
            if not self.start==self.end:
                self.image = self.orig.copy()
                #baslangıc ve bitis koordinatları ile kare cizilir
                cv2.rectangle(self.image, self.start, self.end, self.color, 2)
                #mouse'un sol tuşunu bırakıldıgında izleme biter
                if event==cv2.EVENT_LBUTTONUP:
                    self.track=False
            #yanlıslıkla tıklandıgında izlemeyi restler
            else:
                self.image = self.orig.copy()
                self.start = None
                self.track = False
            cv2.imshow(self.window_name,self.image)
#c++ taki protectet gibi kullanılır 
    @property 
    def koordinat(self):
        if self.start and self.end:
            pts = np.array([self.start,self.end])
            s = np.sum(pts,axis=1)
            (x,y) = pts[np.argmin(s)]
            (xb,yb) = pts[np.argmax(s)]
            return [(x,y),(xb,yb)]
        else:
            return []
