class classify:
    from tensorflow.keras.preprocessing.image import img_to_array
    from tensorflow.keras.models import load_model
    import numpy as np
    import argparse
    import imutils
    import pickle
    import cv2
    import os

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model", required=True,
        help="path to trained model model")
    ap.add_argument("-l", "--labelbin", required=True,
        help="path to label binarizer")
    ap.add_argument("-i", "--image", required=False,
        help="path to input image")
    args = vars(ap.parse_args())
    # load the image
    #image = cv2.imread(args["image"])
    image =cv2.VideoCapture(0)
    output = image.read()

    image = cv2.resize(image, (96, 96))
    image = image.astype("float") / 255.0
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)

    # load the trained convolutional neural network and the label
    print("[INFO] loading network...")
    model = load_model(args["model"])
    lb = pickle.loads(open(args["labelbin"], "rb").read())

    # classify the input image
    print("[INFO] classifying image...")
    proba = model.predict(image)[0]
    idx = np.argmax(proba)
    label = lb.classes_[idx]

    filename = args["image"][args["image"].rfind(os.path.sep) + 1:]
    correct = " " if filename.rfind(label) != -1 else " "
    # build the label and draw the label on the image
    label = "{}: {:.2f}% {}".format(label, proba[idx] * 100, correct)
    output = imutils.resize(output, width=400)
    cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 255, 0), 2)
        
    # show the output image
    print("[INFO] {}".format(label))
    cv2.imshow("Output", output)
    cv2.waitKey(0)
if __name__ == "__main__":
    test = classify()
