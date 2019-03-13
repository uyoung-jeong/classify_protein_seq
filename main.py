import numpy as np
from xgboost import XGBClassifier, Booster

import pickle
import ipdb
import tqdm
from data_loader import Dataset
from sklearn.model_selection import train_test_split
import os

# read and preprocess data
dataset = Dataset()

# split data into train and valid set
X = np.asarray(dataset.X)
Y = np.asarray(dataset.Y)
x_train, x_valid, y_train, y_valid = train_test_split(X, Y, test_size=0.2, random_state=42)

# build model
param = {'objective': 'multi:softprob',
		 }
evallist = [(x_valid, y_valid)]
model = XGBClassifier()
if not os.path.isfile('model.bin'):
	print('start training')
	model.fit(x_train, y_train, eval_set=evallist, verbose=True, early_stopping_rounds=20)

	print('validation result')
	print(model.score(x_valid, y_valid))
	model.save_model('model.bin')

else:
	booster = Booster()
	booster.load_model('model.bin')
	model._Booster = booster
print('check Nematostella vectensis seq')
nv_seq = "TSPDIMSSSFYIDSLISKAKSVPTSTSEPRHTYESPVPCSCCWTPTQPDPSSLCQLCIPTSASVHPYMHHVRGASIPSGAGLYSRELQKDHILLQQHYAATEEERLHLASYASSRDPDSPSRGGNSRSKRIRTAYTSMQLLELEKEFSQNRYLSRLRRIQIAALLDLSEKQVKIWFQNRRVKWKKDKKAAQHGTTTETSSCPSSPASTGRMDGV"
nv_vec = dataset.one_hot(nv_seq)
predict_data = np.asarray([nv_vec]*2)
prediction = model.predict_proba(predict_data)
print('prediction: ')
print(prediction)

ipdb.set_trace()
print('finished execution')
