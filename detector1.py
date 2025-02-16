import dlib
import cv2
import sys
import numpy as np


class ObjectDetector(object): 
    def __init__(self,options=None,loadPath =None):
        #detector secenekleri olustulur
        self.options = options
        if self.options is None:
            self.options = dlib.simple_object_detector_training_options()

         #Test icin egitilmis detector yuklenir
        if loadPath is not None:
            self._detector = dlib.simple_object_detector(loadPath)
            
    #goruntulerin koordinatlarını alır 
    def _prepare_annotations(self,takejpg):
        takej = []
        for (x,y,xb,yb) in takejpg:
            takej.append([dlib.rectangle(left=int(x),top=int(y),right=int(xb),bottom=int(yb))])
        return takej
    #Alınan goruntuler RGB'ye cevrilir
    def _prepare_images(self,imagePaths):
        images = []
        for imPath in imagePaths:
            image = cv2.imread(imPath)
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            images.append(image)
        return images
    #Train secenegi fotograflar ve koordinatlar ile train islemini gerceklestirir
    def fit(self, imagePaths, takejpg, visualize=False, savePath=None):
        takejpg = self._prepare_annotations(takejpg)
        images = self._prepare_images(imagePaths)
        self._detector = dlib.train_simple_object_detector(images,takejpg, self.options)

        #HOG görselestirmesi
        if visualize:
            win = dlib.image_window()
            win.set_image(self._detector)
            dlib.hit_enter_to_continue()

        #Detector diske kaydededilir
        if savePath is not None:
            self._detector.save(savePath)

        return self
    #Tum goruntuler icin karelerin koordinatlari alinir
    #Verilen goruntudeki kareleri cizdirmek icin kullanılır
    def predict(self,image):
        boxes = self._detector(image)
        preds = []
        for box in boxes:
            (x,y,xb,yb) = [box.left(),box.top(),box.right(),box.bottom()]
            preds.append((x,y,xb,yb))
        return preds
    
    def detect(self,image,annotate=None):
        while True:
          #ret,imagePath=cap.read()
          image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
          preds = self.predict(image)
          font=cv2.FONT_HERSHEY_SIMPLEX
          for (x,y,xb,yb) in preds:
              image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
              gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
              confidence = self.predict(gray[y:y+yb,x:x+xb])
              
              for i in confidence:
                  print("Koordinatlar:",format(confidence))
                  son=confidence[0][0]+confidence[0][1]+confidence[0][2]+confidence[0][3]
                  son=son/4
                  if ( son < 100):
                      print("Tespit orani: %",son)
                      yüzde="Tespit orani:  {:.2f}%".format(son)
                      cv2.putText(image, str(yüzde), (x,y+yb), font, 1, (0,0,255), 2)
                      #cv2.putText(image, name, (x,y), font, 1, (0,0,255), 2)
                  else:
                      print("Tespit orani: %100")
                      yüzde="Tespit orani:  %100"
                      cv2.putText(image, str(yüzde), (x,y+yb), font, 1, (0,0,255), 2)
                      #cv2.putText(image, name, (x,y), font, 1, (0,0,255), 2)
                
               #resim cizdireme ve acıklama
              cv2.rectangle(image,(x,y),(xb,yb),(0,0,255),2)
              if annotate is not None and type(annotate)==str:
                  cv2.putText(image,annotate,(x+5,y-5),cv2.FONT_HERSHEY_SIMPLEX,1.0,(128,255,0),2)
          cv2.imshow("Detected",image)
          if cv2.waitKey(25) & 0xFF == ord("q"):
             cv2.destroyAllWindows()
             break
