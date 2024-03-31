# import the necessary packages
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from imutils import paths
import matplotlib.pyplot as plt
import numpy as np
import os

# initialize the initial learning rate, number of epochs to train for,
# and batch size
# initially make sure that our learning rate is less, so that our loss will be calculated properly,
# learning rate represents the size of the steps taken which indicates how aggressive you like to train the AI.If the learning rate increases, the area covered in the search space will increase, so we might reach global minimum faster, however we can overshoot the target. for smaller learning rates, training will take much longer to reach optimized weight values.
INIT_LR = 1e-4
# practice makes perfect, similar to humans, AI learns overtime and its intelligence amplifies as we continually feed the training data.
# An epoch means that AI has been fed with the entire dataset once.
EPOCHS = 20
# when AI is trained, we generally don't feed the entire dataset to the AI model due to computation and memory limitations.,we generally breakdown the training data into smaller batches which are fed to the model indivdually. An epoch contains one or more batches.
BS = 32

DIRECTORY = r"D:\covid_mask_and_social_distancing\dataset"
CATEGORIES = ["with_mask", "without_mask"]

# grab the list of images in our dataset directory, then initialize
# the list of data (i.e., images) and class images
print("[INFO] loading images...")

data = []
labels = []

for category in CATEGORIES:
    path = os.path.join(DIRECTORY, category)
    for img in os.listdir(path):
		img_path = os.path.join(path, img)
		# load_img is class from keras.preprocessing.image, which loads an image from an library path, and we here set the height and width of the image to 224
		image = load_img(img_path, target_size=(224, 224))
		# img_to_array is also class from keras.preprocessing.image, which converts an image to numpy array
		image = img_to_array(image)
		# preprocess_input is class from keras.applications.mobilenet_v2 which is required when using with mobilenet_v2
		image = preprocess_input(image) 
		# append image and category to data and label lists
		data.append(image)
		labels.append(category)

# perform one-hot encoding on the labels
lb = LabelBinarizer()
# fit_transform from sklearn.preprocessing converts multi-class labels to binary labels, output is 2d matrix with 0 and 1 only
labels = lb.fit_transform(labels)
# to_categorical method is from keras.utils converts a class vector to binary class matrix
labels = to_categorical(labels)

#data type expected is float32 when using with to_categorical function
# we need to convert lists into arrays, as deep learing models only work with arrays.
data = np.array(data, dtype="float32")
labels = np.array(labels)

#we split the dataset into 20 % testing data and 80% training data. there is no validation dataset separated as such,
# we have used stratified samplying method, using statifying the labels, so that the class proportions are preserved even after spliting.
(trainX, testX, trainY, testY) = train_test_split(data, labels,
	test_size=0.20, stratify=labels, random_state=42)

# construct the training image generator for data augmentation
# we do data augmentation to create new data based on modifications of our existing data, we create new augmented data by making reasonable modifications to the data in our training set.here we did data augmentation to create more samples from original dataset and to reduce overfitting.
aug = ImageDataGenerator(
	rotation_range=20,
	zoom_range=0.15,
	width_shift_range=0.2,
	height_shift_range=0.2,
	shear_range=0.15,
	horizontal_flip=True,
	fill_mode="nearest")

# load the MobileNetV2 network, ensuring the head FC layer sets are
# left off
baseModel = MobileNetV2(weights="imagenet", include_top=False,
	input_tensor=Input(shape=(224, 224, 3)))

# construct the head of the model that will be placed on top of the
# the base model
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(2, activation="softmax")(headModel)

# place the head FC model on top of the base model (this will become
# the actual model we will train)
model = Model(inputs=baseModel.input, outputs=headModel)

# loop over all layers in the base model and freeze them so they will
# *not* be updated during the first training process
for layer in baseModel.layers:
	layer.trainable = False

# compile our model
print("[INFO] compiling model...")
opt = Adam(lr=INIT_LR, decay=INIT_LR / EPOCHS)
model.compile(loss="binary_crossentropy", optimizer=opt,
	metrics=["accuracy"])

# train the head of the network
print("[INFO] training head...")
H = model.fit(
	aug.flow(trainX, trainY, batch_size=BS),
	steps_per_epoch=len(trainX) // BS,
	validation_data=(testX, testY),
	validation_steps=len(testX) // BS,
	epochs=EPOCHS)

# make predictions on the testing set
print("[INFO] evaluating network...")
predIdxs = model.predict(testX, batch_size=BS)

# for each image in the testing set we need to find the index of the
# label with corresponding largest predicted probability
predIdxs = np.argmax(predIdxs, axis=1)

# show a nicely formatted classification report
print(classification_report(testY.argmax(axis=1), predIdxs,
	target_names=lb.classes_))

# serialize the model to disk
print("[INFO] saving mask detector model...")
model.save("mask_detector.model", save_format="h5")

# plot the training loss and accuracy
N = EPOCHS
plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, N), H.history["loss"], label="train_loss")
plt.plot(np.arange(0, N), H.history["val_loss"], label="val_loss")
plt.plot(np.arange(0, N), H.history["accuracy"], label="train_acc")
plt.plot(np.arange(0, N), H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig("plot.png")