import uvicorn
import uuid
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from neural_network.main import NeuralNetwork
from server.dataModels.models import User, Data, Final
from lib.lib import Request, Model, Structure, Dataset, Train
from database.main import Database

app = FastAPI()
print('start')

path = 'localhost'
if 'MY_PATH' in os.environ:
    path = os.environ["MY_PATH"]

database = Database()


@app.post("/auth/registration")
def registration(user: User):
    results = database.put_user(user.login, user.password, user.email)
    response = {
        "resultCode": 0,
        "email": user.email,
        "login": user.login
    }
    if results[0] == "0":
        return response
    else:
        response["resultCode"] = 1
        response["email"] = ""
        response["login"] = ""
        return response


@app.post("/auth/login")
def login(user: User):
    results = database.take_user(user.login)
    response = {
        "resultCode": 2,
        "email": "",
        "login": ""
    }

    if results == []:
        return response
    elif results[0][2] == user.password:
        response = {
            "resultCode": 0,
            "email": results[0][3],
            "login": results[0][1]
        }
        return response
    else:
        return response

@app.post("/dataset")
def user_data(dataset: UploadFile):
    contents = dataset.file.read()
    file_name = "".join(str(uuid.uuid4()).split("-")) + dataset.filename
    file_path = "./datasets/" + file_name
    with open(file_path, "wb") as f:
        f.write(contents)
    dataset.file.close()

    response = {"dataset_file_name": file_name}
    return response


@app.post("/data")
def user_data(data: Data):
    model = Model(opt_fn=data.opt_fn, loss_fn=data.loss_fn)
    structure = Structure(neuron_count=data.neuron_count,
                          hidden_layer_count=data.hidden_layer_count,
                          act_fn=data.act_fn)
    file_path = "./datasets/" + data.dataset_filename
    file = open(file_path, "r")
    dataset_model = Dataset(learning_data=file,
                            input_type=data.dataset_filename.split(".")[-1],
                            depth_input_data=data.depth_input_data)
    train = Train(epochs=data.epochs, validation_split=data.validation_split,
                  batch_size=data.batch_size)

    request = Request(dataset=dataset_model, model=model, structure=structure,
                      train=train)
    neuralnetwork = NeuralNetwork(model=request.model,
                                  structure=request.structure,
                                  train=request.train, dataset=request.dataset)

    model = neuralnetwork.create_model()
    model = neuralnetwork.train_model(model)
    neuralnetwork_file_name = "".join(str(uuid.uuid4()).split("-"))
    neuralnetwork_file_path = "./final/" + neuralnetwork_file_name + ".keras"
    neuralnetwork.save_model(model, neuralnetwork_file_path)

    results = database.put_network(data.name, neuralnetwork_file_name, data.login,
                                   data.opt_fn, data.loss_fn, data.act_fn, data.neuron_count)
    resultCode = results[0][0]
    print(resultCode)

    response = {"neuralnetwork_file_name": neuralnetwork_file_name}
    return response

@app.post("/final")
def download_file(final: Final):
    return FileResponse(path=("./final/" + final.neuralnetwork_file_name + ".keras"))

@app.get("/networks/{login}")
def get_user_networks(login: str):
    results = database.take_users_networks(login)
    print(results)
    response = []
    for i in results:
        network = {
            "id" : i[0],
            "name" : i[1],
            "path" : i[3]
        }
        response.append(network)
    return response


@app.get("/networksParams/{id}")
def get_networks_params(id: int):
    results = database.take_network_params(id)
    if len(results) != 0:
        response = {}
        for i in results:
            response["optimization"] = i[4]
            response["lossFn"] = i[5]
            response["activations"] = i[6]
            response["neuronCounts"] = i[7]
        return response
    else:
        return {
            "resultCode" : 1
        }


origins = [
    "http://localhost",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app")