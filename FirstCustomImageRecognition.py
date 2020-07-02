# from imageai.Prediction.Custom import CustomImagePrediction
# import os


# # #   dali
# # #   klimt
# # #   leo
# # #   picasso
# # #   pollock
# # #   roerich
# # #   vanGogh


# def image_recognition(testing_image):

#     new_predictions = None

#     execution_path = os.getcwd()

#     prediction = CustomImagePrediction()
#     prediction.setModelTypeAsResNet()
#     prediction.setModelPath("model_ex-048_acc-0.879121_7.h5")
#     prediction.setJsonPath("idenprof/json/model_class_7.json")
#     prediction.loadModel(num_objects=7)

#     predictions, probabilities = prediction.predictImage(
#         testing_image, result_count=7)

#     new_predictions = {}

#     for eachPrediction, eachProbability in zip(predictions, probabilities):
#         # print(eachPrediction, " : ", round(eachProbability, 3))
#         new_predictions[eachPrediction] = round(eachProbability, 3)
#         # print(new_predictions)

#     del prediction
#     del predictions
#     del probabilities

#     return new_predictions


# # testing_image = "imgTest/picasso2.jpg"
# # image_recognition(testing_image)
