from threading import Thread
# from imageai.Prediction import ImagePrediction


class ImageProcessingThread(Thread):

    def __init__(self, db_image_collection):
        ''' Constructor. '''
        Thread.__init__(self)
        self.db_image_collection = db_image_collection
        print("Thread initialised!")

    def run(self):
        print("Thread run")
        images_list = self.db_image_collection.find({"processed": False})
        for image_entry in images_list:
            image = open(image_entry.get("path"))

            # prediction = ImagePrediction()
            # prediction.setModelTypeAsSqueezeNet()
            # prediction.setModelPath("squeezenet_weights_tf_dim_ordering_tf_kernels.h5")
            # prediction.loadModel()
            #
            # predictions, probabilities = prediction.predictImage(image, result_count=5)
            # for eachPrediction, eachProbability in zip(predictions, probabilities):
            #     print(eachPrediction, " : ", eachProbability)
