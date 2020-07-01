from imageai.Prediction.Custom import ModelTraining

model_trainer = ModelTraining()
model_trainer.setModelTypeAsResNet()
model_trainer.setDataDirectory("idenprof")
model_trainer.trainModel(num_objects=7, num_experiments=70,
                         enhance_data=True, batch_size=7, show_network_summary=True)


# Continuous Model Training on the same dataset

# from imageai.Prediction.Custom import ModelTraining
# import os

# trainer = ModelTraining()
# trainer.setModelTypeAsDenseNet()
# trainer.setDataDirectory("idenprof")
# trainer.trainModel(num_objects=10, num_experiments=50, enhance_data=True, batch_size=8, show_network_summary=True, continue_from_model="idenprof_densenet-0.763500.h5")
