import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplolib import style 
import datetime as dt
import sqlite3 
import os 
import csv


'''
Variable List 



'''

#file extensions
CSV = 'csv'
EXCEL1 = 'xlsx'
EXCEL2 = 'xls'


#data types
STR = 'str'
INT = 'int'
FLOAT = 'float'

#affinities
R = 'REAL' 
T = 'TEXT'



class Pipeline(object):
	"""docstring for Pipeline"""

	def __init__(self, path, db = False, dbName = ''):	
		'''Initialization of global variables
			params: path (str): Doc Path for the desired csv file 

			Pandas DataFrame built into the object
			
			Examines file extension in order to intialize pandas DataFrame
		 		''' 
		if not db:
		 		
			if path[-3:] == CSV:
				self.DataFrame = pd.read_csv(path)
			elif path[-3:] == EXCEL2 or path[-4:] == EXCEL1:
				self.DataFrame = pd.read_excel(path)
		

		else:
			if len(dbName)> 0 and dbName[:-2] == ".db":
				if path[-3:] == CSV:
					self.DataFrame = pd.read_csv(path)
				elif path[-3:] == EXCEL2 or path[-4:] == EXCEL1:
					self.DataFrame = pd.read_excel(path)
			
				self.conn = sqlite3.connect(dbName)
				self.sqlCursor = conn.cursor()
			else:
				raise ValueError('')
	
	def GetHeader(self):
		'''Retrieves the header row of the dataframe
		returns the header row as list of terms  '''
		return list(self.DataFrame)

	# def DataSummary(self):
	# 	'''Returns overview of data'''


	def ListToString(self, array):
		string = ''
		for item in array:
			string += str(item) + ', '
		return string 

	def SetDataArray(self, header, array):
		self.DataFrame[header] = array 
		return self.DataFrame
		

	def DataBaseInit(self, tableName, dtypeArray, headerarray = [], FinalStep = False):

		queryInitial = """CREATE TABLE IF NOT EXISTS %s"""%(tableName)
		print(queryInitial)	

		if len(headerarray) == 0:
			queryString = self.InitQueryBuilder(zip(self.GetHeader(), dtypeArray))
			query = queryInitial + queryString
		else:
			queryString = self.InitQueryBuilder(zip(headerarray, dtypeArray))
			query = queryInitial + queryString

		self.sqlCursor.execute(query)
		self.conn.commit()

		if FinalStep:
			self.sqlCursor.close()
			self.conn.close()

	def InitQueryBuilder(self, tupList):
		queryString = ''
		for tup in range(len(tupList)): 
		 	if tup[i][1] == INT or tup[i][1] == FLOAT:
		 		queryString += tup[i][0] + ' ' + R + ', '

		 	elif tup[i][1] == STR:
		 		queryString += tup[i][0] + ' ' + T + ', '
		return '(%s)'%(queryString[:-1])

	def RowEntry(self, tableName, values = [], single = True):

		entry = """INSERT INTO """ + tableName + """ VALUES""" + str(tuple(values))
		self.sqlCursor.execute(entry)
		self.sqlCursor.commit()

		if single:
			self.CloseConnection()

	def ArrayEntry(self, tableName, values):
		for row in values:
			entry = """INSERT INTO """ + tableName + """ VALUES""" + str(tuple(row))
			self.sqlCursor.execute(entry)
		self.CloseConnection()

	def GenQuery(self, tableName, queryType = [], final = False):
		if len(queryType) == 0:
			query = """SELECT * FROM """ + tableName
		else:
			query = """SELECT * FROM """ + self.ListToString(queryType)
		self.sqlCursor.execute(query)
		[print(row) for row in self.sqlCursor.fetchall()]

		if final:
			self.CloseConnection()
	def CloseConnection(self):
		self.sqlCursor.close()
		self.conn.close()


	def Array(self, keyList=[]):

		'''Takes a list of keys and builds numpy arrays 
			'''
		arrayList = []
		if len(keyList) > 1: 
			for key in keyList:
				arrayList.append(np.array(list(self.DataFrame[key])))

			return np.dstack(arrayList)

		elif len(keyList) == 1:
			return np.array(list(self.DataFrame[keyList[0]]))

		elif len(keyList) == 0: 
			for header in self.GetHeader():
				arrayList.append(list(np.array(self.DataFrame[header])))

			return np.dstack(arrayList)

	def NullCounter(self, remove = False, col = False, row = True):
		nullCount = 0
		if not remove:
			#count number of collumns with null 
			#return number of collumns with null
			#return dataframe with nulls removed
			for header in self.GetHeader():
				if self.DataFrame[header].isnull().sum() > 0:
					nullCount+=1
			if col:
				self.DataFrame.dropna(axis = 1, how = 'any')
			elif row:
				self.DataFrame.dropna(axis = 0, how = 'any')

			return nullCount, self.DataFrame			
		else: 
			#count number of collumns with null 
			#return number of collumns with null
			for header in self.GetHeader():
				if self.DataFrame[header].isnull().sum() > 0:
					nullCount+=1

			return nullCount
"""

class DBuilder(Pipline):
	'''Docstring for DBuilder'''
	def __init__(self, dbName, tableName, headers, dTypes):
		self.name = name 
		self.table = tableName 
		self.headers = headers 
		self.types = dTypes
	'''Getters'''
	def GetTableList(self):

	def GetTableHeaders(self):

	'''Setters and DB Queries'''
	def Query(self, )
"""

# class DbJoins(Pipeline):
# 	"""docstring for DbJoins"""
# 	def __init__(self, arg):
# 		super(DbJoins, self).__init__()
# 		self.arg = arg

# class Visualizations(Pipeline):
# 	"""docstring for Visualizations"""
# 	def __init__(self, arg):
# 		super(Visualizations, self).__init__()
# 		self.arg = arg

# class Out(object):
# 	"""Takes results of analysis and writes it to CSV/Excel"""
# 	def __init__(self, arg):
# 		super(Out, self).__init__()
# 		self.arg = arg

		





if __name__ == '__main__':
	os.chdir('C:/Users/nhilt/Desktop')
	obj = MachineLearningPrep('^GSPC.csv')
	print(obj.GetHeader())
	print(obj.Array())
