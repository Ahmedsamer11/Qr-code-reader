import cv2
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
# set up camera object
cap = cv2.VideoCapture(2)
cap2 = cv2.VideoCapture(1)
# QR code detection object
detector = cv2.QRCodeDetector()
detector2 = cv2.QRCodeDetector()

cred = credentials.Certificate("--put ur api key here--")
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection('gates').document('gates_status')
doc = doc_ref.get()

while True:
    # get the image
    _, img = cap.read()
    _, img2 = cap2.read()
        # get bounding box coords and data
    data, bbox, _ = detector.detectAndDecode(img)
    data2, bbox2, _ = detector2.detectAndDecode(img2)
        # if there is a bounding box, draw one, along with the data
    if (bbox is not None):
        for i in range(len(bbox)):
            cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i + 1) % len(bbox)][0]), color=(255,0, 255), thickness=2)
        cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        if data:
            print( data)
            doc_ref.update({'entry_qr': data})
            time.sleep(1)
            doc_ref.update({'entry_qr': ''})
        # display the image preview


    if (bbox2 is not None):
        for i in range(len(bbox2)):
            cv2.line(img2, tuple(bbox2[i][0]), tuple(bbox2[(i + 1) % len(bbox2)][0]), color=(255,0, 255), thickness=2)
        cv2.putText(img2, data2, (int(bbox2[0][0][0]), int(bbox2[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 255, 0), 2)
        if data2:
            print( data2)
            doc_ref.update({'exit_qr': data2})
            time.sleep(2)
            doc_ref.update({'exit_qr': ''})
        # display the image preview
    cv2.imshow("code detector", img)
    cv2.imshow("code detector2", img2)
    if(cv2.waitKey(1) == ord("q")):
            break
cap.release()
cv2.destroyAllWindows()

