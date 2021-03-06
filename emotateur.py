from ui import ui
from PyQt5 import QtCore, QtGui, QtWidgets
from face_comparator import *
import cv2
import sys

class emotateur():
    def __init__(self):
        self.Form=QtWidgets.QWidget()
        self.ui = ui(self.Form)
        self.ui.left_label.setPixmap(QtGui.QPixmap("img/home.jpg").scaled(640, 480))
        self.cap=cv2.VideoCapture()
        if not self.cap.open(0):
            print("camera configuration failed")
            sys.exit(0)
        ret, frame = self.cap.read()
        imgSize = list(frame.shape)
        outSize = imgSize[1::-1]

        self.fc = face_comparator(outSize)
        self.checkSimilarityTimer=QtCore.QTimer()
        self.ui.folder_button.clicked.connect(self.openImage)

        self.faceBB = [150, 75, 300, 300]
        self.checkSimilarityTimer.timeout.connect(self.updateFrame)
        self.checkSimilarityTimer.start(1000/2)

    def opencvimg_2_pixmap(self, srcMat):
        cv2.cvtColor(srcMat, cv2.COLOR_BGR2RGB,srcMat)
        height, width, bytesPerComponent= srcMat.shape
        bytesPerLine = bytesPerComponent* width
        srcQImage= QtGui.QImage(srcMat.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        return QtGui.QPixmap.fromImage(srcQImage)

    def openImage(self):
        self.checkSimilarityTimer.stop()
        img_reference_file_name, filetype = QtWidgets.QFileDialog.getOpenFileName(self.Form,  "choose a file",  "",  "Image Files (*.png *.bmp *.jpg *.tif *.GIF)")
        if 'test1' in img_reference_file_name:
            faceBB = [180, 50, 300, 300]
        elif 'test2' in img_reference_file_name:
            faceBB = [180, 60, 250, 250]
        elif 'test3' in img_reference_file_name:
            faceBB = [220, 120, 230, 230]
        elif 'test4' in img_reference_file_name:
            faceBB = [250, 90, 200, 200]
        elif 'test5' in img_reference_file_name:
            faceBB = [150, 75, 300, 300]
        img_reference = cv2.imread(img_reference_file_name)
        res_reference = cv2.resize(img_reference,(640, 480), interpolation = cv2.INTER_CUBIC)
        res_reference, self.face_key_points_reference = self.fc.get_face_key_points(res_reference, faceBB)
        self.ui.left_label.setPixmap(self.opencvimg_2_pixmap(res_reference))
        self.checkSimilarityTimer.start(1000/2)

    def updateFrame(self):
        ret, srcMat=self.cap.read()
        srcMat=cv2.resize(srcMat, (640, 480), interpolation=cv2.INTER_CUBIC)
        frame=cv2.flip(srcMat, 1)
        res, face_key_points = self.fc.get_face_key_points(frame, self.faceBB)
        self.faceBB = self.fc.computeBB(face_key_points, self.faceBB)
        self.ui.right_label.setPixmap(self.opencvimg_2_pixmap(res))
        try:
            similarity = self.fc.compare_face(self.face_key_points_reference, face_key_points)
            self.ui.similarity_number.setText( "%.2f%%" % (similarity*100))
            self.ui.verticalSlider.setValue(int(similarity*100))
        except:
            pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    e = emotateur()
    e.Form.show()
    sys.exit(app.exec_())
