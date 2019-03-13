import numpy as np
from xgboost import XGBClassifier

import pickle
import ipdb
import tqdm
import os
import random

class Dataset():
	def __init__(self):
		self.fasta_pickle_path = os.path.join(os.getcwd(), 'data', 'fasta_data.pkl')
		self.x_pickle_path = os.path.join(os.getcwd(), 'data', 'x_data.pkl')
		self.y_pickle_path = os.path.join(os.getcwd(), 'data', 'y_data.pkl')
		self.acid_codes = ['A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', 'Z', 'X']
		self.idx_dict = {}
		for i, c in enumerate(self.acid_codes):
			self.idx_dict[c] = i
		self.max_len = 500
		self.X = []
		self.Y = []
		self.num_class = 5
		self.target_genes = ['a2', 'b2', 'b8', 'c8', 'd8']

		self.label_dict = {}
		for i, c in enumerate(self.target_genes):
			self.label_dict[c] = i
		self.label_sheet = np.eye(self.num_class, dtype='int64')
		
		if not os.path.isfile(self.fasta_pickle_path):
			# read data
			base_filename = 'uniprot-gene_hox'

			data_dir = os.path.join(os.getcwd(),'data')
			files = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

			def check_target_genes(filename):
				isFound = False
				for gene in self.target_genes:
					if filename.find(gene) != -1:
						isFound = True
						return True
				return isFound
				
			target_files = [f for f in files if check_target_genes(f) == True]
			nontarget_files = [f for f in files if f not in target_files]
			file_paths = [os.path.join(os.getcwd(), 'data', fname) for fname in files]
			
			# parse
			data_list = []
			for path in file_paths:
				f = open(path, 'r')
				data_list.append(f.readlines())
				f.close()
			def parse_fasta(data):
				dic = {}
				i=0
				Y_label = self.get_label(data[0])
				while i < len(data):
					if data[i].find('>') != -1:
						header = data[i].replace('\n', '')
						header = data[i].replace('>', '')
						tokens = header.split()
						name = tokens[0]
						desc = ' '.join(tokens[1:])
						seq = ""
						i += 1
						while i < len(data) and data[i].find('>') == -1:
							seq += data[i].replace('\n', '')
							i += 1
						if len(seq) > self.max_len:
							self.max_len = len(seq)
						dic[name] = [name, desc, seq]
						self.X.append(self.one_hot(seq))
						self.Y.append(Y_label)
					i += 1
				return dic

			parsed_data = [parse_fasta(data) for data in data_list]
			data_len_list = [len(data) for data in parsed_data]
			print('max_len: ' + str(self.max_len))
			# save data
			with open(self.fasta_pickle_path, 'wb') as f:
				pickle.dump(parsed_data, f, pickle.HIGHEST_PROTOCOL)
			
			with open(self.x_pickle_path, 'wb') as f:
				pickle.dump(self.X, f, pickle.HIGHEST_PROTOCOL)
			
			with open(self.y_pickle_path, 'wb') as f:
				pickle.dump(self.Y, f, pickle.HIGHEST_PROTOCOL)
		
		# load data
		print('loading data')
		with open(self.fasta_pickle_path, 'rb') as f:
			self.data = pickle.load(f)
		with open(self.x_pickle_path, 'rb') as f:
			self.X = pickle.load(f)
		with open(self.y_pickle_path, 'rb') as f:
			self.Y = pickle.load(f)

	def one_hot(self, s):
		s = s.upper()
		str2vec = np.zeros((self.max_len,len(self.acid_codes)), dtype='int64')
		max_length = min(len(s), self.max_len)
		for i in range(max_length):
			c = s[i]
			if c in self.acid_codes:
				str2vec[i][self.idx_dict[c]] = 1
			else:
				ipdb.set_trace()
				print(c)
		return str2vec.flatten()

	def get_label(self, s):
		if False:
			if s.find('A2') != -1:
				return self.label_sheet[0]
			elif s.find('B2') != -1:
				return self.label_sheet[1]
			elif s.find('B8') != -1:
				return self.label_sheet[2]
			elif s.find('C8') != -1:
				return self.label_sheet[3]
			elif s.find('D8') != -1:
				return self.label_sheet[4]
			else:
				print("ERROR: invalid label")
				exit()
		if True:	
			if s.find('A2') != -1:
				return 1
			elif s.find('B2') != -1:
				return 2
			elif s.find('B8') != -1:
				return 3
			elif s.find('C8') != -1:
				return 4
			elif s.find('D8') != -1:
				return 5
			else:
				print("ERROR: invalid label")
				exit()
			
			
			
