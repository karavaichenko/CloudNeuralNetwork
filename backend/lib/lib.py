import csv
import numpy as np

class Request:
    def __init__(self, structure, model, dataset, train):
        self.train = train
        self.dataset = dataset
        self.model = model
        self.structure = structure


class Dataset:
    def __init__(self, learning_data: [], input_type: str,
                 depth_input_data: int):
        # array??? / датасет и вход и выход
        self.learning_data = learning_data
        # String / тип входных данных
        self.input_type = input_type
        # int глубина входных данных / (255 для RGB картинки)
        self.depth_input_data = depth_input_data

        # int / размер входных данных (кол-во пикселей одной картинки)
        self.input_data_scale = None
        # np.array
        self.learning_data_output = None
        # np.array
        self.learning_data_input = None
    def prepare_data(self):
        # чтение csv
        datafile = list(csv.reader(self.learning_data, delimiter=','))
        # удаление метаданных
        datafile.pop(0)
        x_train = []
        y_train = []
        # разделение на входную и выходную
        for i in datafile:
            e = list(i)
            x_train.append(e[1:])
            y_train.append(e[:1])

        x_train = np.array(x_train, dtype="int")
        y_train = np.array(y_train, dtype="int")
        # размерность входных данных
        scale = len(x_train[0])

        # нормализация
        # x_train / self.depth_input_data

        self.input_data_scale = scale
        self.learning_data_input = x_train
        self.learning_data_output = y_train

class Structure:
    def __init__(self, hidden_layer_count: int, neuron_count: [int],
                act_fn: [str]):
        # int / кол-во скрытых слоёв нейронов
        self.hidden_layer_count = hidden_layer_count
        # int_array / кол-во нейронов в каждом слое
        self.neuron_count = neuron_count
        # string_array / функция активации (длинна массива на 1 больше hidden_layer_count)
        self.act_fn = act_fn


class Model:
    def __init__(self, opt_fn: str, loss_fn: str):
        # string / способ оптимизации (градиентный спуск)
        self.opt_fn = opt_fn
        # string / функция потерь
        self.loss_fn = loss_fn


class Train:
    def __init__(self, epochs: int, validation_split: float, batch_size: int):
        # int / кол-во повторений обучения
        self.epochs = epochs
        # float / доля на валидацию
        self.validation_split = validation_split
        # int / размер партии на которую делится обучающая выборка
        self.batch_size = batch_size