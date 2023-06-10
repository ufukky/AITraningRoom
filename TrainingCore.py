import numpy as np
import csv
from sklearn.neural_network import MLPRegressor
from sklearn.utils import Bunch
from datetime import datetime
import os
import pickle

DATA_PATH = "C:/Users/uky54/Documents/School/Bitirme 2/Training/Data/"
MODEL_SAVE_PATH = "C:/Users/uky54/Documents/School/Bitirme 2/Training/Models/"

class TrainingCore:
    def load_dataset(filename = "*.cvs"):
        with open(DATA_PATH+filename) as csv_file:
            data_reader = csv.reader(csv_file)
            firstline = next(data_reader)
            feature_names = firstline[:6]
            target_names = firstline[6:8]
            print(target_names)
            data = []
            target = []
            for row in data_reader:
                features = row[0:6]
                label = row[6:8]
                data.append([float(num) for num in features])
                target.append([float(_label) for _label in label])
            
            data = np.array(data)
            target = np.array(target)
        return Bunch(data=data, target=target, feature_names=feature_names,target_names=target_names) 
    
    def train(X_train, y_train,save = True, filename = "") -> MLPRegressor:
        nn = MLPRegressor(
            activation='relu',
            hidden_layer_sizes=(5, 20),
            alpha=0.001,
            random_state=20,
            early_stopping=False
            )
            #
            # Train the model
        nn.fit(X_train, y_train)
        if save:
            if filename == "":
                _filename = f'nn_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}.pkl'
            else:
                _filename = filename
            with open(MODEL_SAVE_PATH+_filename,'wb') as f:
                pickle.dump(nn,f)
        return nn
    
    def load_model(filename = ""):
        with open(MODEL_SAVE_PATH+filename,'rb') as f:
            nn = pickle.load(f)
        if nn == None:
            raise Exception(f"No model named {filename} exsists in {MODEL_SAVE_PATH}")
        return nn

    def load_model_latest():
        os.chdir(MODEL_SAVE_PATH)
        files = filter(os.path.isfile, os.listdir(MODEL_SAVE_PATH))
        files = [f for f in files] # add path to each file
        files.sort(key=lambda x: os.path.getmtime(x))
        print("Loaded model: " + files[-1])
        return TrainingCore.load_model(files[-1])