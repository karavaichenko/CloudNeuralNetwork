from tensorflow import keras
from keras.layers import Dense, Flatten
import numpy as np
import csv
from lib.lib import Request, Model, Structure, Dataset, Train

############## backend test

# симуляция приходящих данных
file = open("../mnist_train.csv", "r")

model = Model(opt_fn="adam", loss_fn="categorical_crossentropy")
structure = Structure(neuron_count=[128, 200, 27], hidden_layer_count=2,
                      act_fn=['relu', 'relu', 'softmax'])
dataset = Dataset(learning_data=file, input_type="csv", depth_input_data=255)
train = Train(epochs=10, validation_split=0.1, batch_size=32)

request = Request(dataset=dataset, model=model, structure=structure, train=train)

####################


class NeuralNetwork(Request):
    def create_model(self):
        self.prepare_dataset()
        model = keras.models.Sequential()
        model.add(Flatten(input_shape=(self.dataset.input_data_scale, )))
        count: int = self.structure.hidden_layer_count
        for i in range(count):
            model.add(Dense(units=self.structure.neuron_count[i], activation=self.structure.act_fn[i]))
        model.add(Dense(units=self.structure.neuron_count[-1], activation=self.structure.act_fn[-1]))
        model.compile(optimizer=self.model.opt_fn, loss=self.model.loss_fn, metrics=["accuracy"])
        return model


    def prepare_dataset(self):
        self.dataset.prepare_data()
        self.dataset.learning_data_input = self.dataset.learning_data_input / self.dataset.depth_input_data
        self.dataset.learning_data_output = keras.utils.to_categorical(self.dataset.learning_data_output, self.structure
                                                                       .neuron_count[-1])

    def train_model(self, model):
        model.fit(x=self.dataset.learning_data_input, y=self.dataset.learning_data_output,
                  batch_size=self.train.batch_size, epochs=self.train.epochs,
                  validation_split=self.train.validation_split)
        return model

    def save_model(self, model, path: str):
        model.save(filepath=path)


neuralnetwork = NeuralNetwork(model=request.model, structure=request.structure,
                              train=request.train, dataset=request.dataset)

model = neuralnetwork.create_model()
model = neuralnetwork.train_model(model)
neuralnetwork.save_model(model, "../12122312312.keras")
