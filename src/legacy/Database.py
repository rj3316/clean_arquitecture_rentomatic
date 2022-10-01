#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#----------------------------------------------------------------------------
# Created By  : Igor Usunariz
# Created Date: 2022/08/11
# version ='1.0'
# Mail = 'i.usunariz.lopez@gmail.com'
#
# ---------------------------------------------------------------------------
# 
# DATABASE MODULE
#
# Dependencies
# sqlalchemy, pymysql, Module, IDatabase
#
# ---------------------------------------------------------------------------
from time import time
from dataclasses import dataclass, field
from typing import List

from .Module import Module
from .Interfaces import IDatabase

class Database(Module, IDatabase):
	# INSTANTIATION
	def _initialization(self):
		self.data.config['database'] = {
			'host'    : None,
			'port'    : None,
			'database'  : None,
			'default_db': None,
			'user'       : None,
			'password'   : None,
			'timeout'    : 1,
			'table'      : None,
		}

		self.data.config['connection'] = {
			'counter'    : 0,
			'max_counter': 1,
			'retried'        : False,
			'pandas_imported': False,
			'recreate'       : False,
			'recreate_all'   : True,
			'max_uptime_diff': 2000,
			'extra_verbose'  : False,
		}        

		self._database_ok = False

		self._timing = {
			'uptime'     : time(),
			'last_uptime': None,
		}

		self._last_action = None
		self._last_uptime = None

		self._action = {
			'connect': True,
			'disconnect': True,
		}
		
		# Inicializamos las variables de conexión
		self._conn = None
		self._cursor = None

	def _setting(self):
		self._set_default_database()
		
	def _welcome(self):
		self.data.payloads = (f"Database on socket {self.data.config['database']['host']}:{self.data.config['database']['port']}", 20)
		self.data.payloads = (f"Database:\t\'{self.data.config['database']['database']}\'", 20)
		self.data.payloads = (f"Default database:\t\'{self.data.config['database']['default_db']}\'", 20)
		self.data.payloads = (f"Max connection retries: {self.data.config['connection']['max_counter']}", 20)

	# PARTICULAR
	def get_param_manager(self):
		return ParamManager()

	# AUXILIARS
	def _set_default_database(self, database = None):
		if database is None:
			database = self.data.config['database']['database']
			
		self.data.config['database']['default_db'] = database

	# PUBLIC METHODS
	def connect(self):
		pass

	def disconnect(self):
		pass

	def get_connection_status(self):
		pass
	
	def select(self, **kwargs):
		# Polymorphic method
		pass

	def insert(self, **kwargs):
		# Polymorphic method
		pass

	def update(self, **kwargs):
		# Polymorphic method
		pass

	def delete(self, **kwargs):
		# Polymorphic method
		pass

@dataclass
class Filter:
	column: str = None
	cond  : str = None
	value : str = None
	logic : str = None

@dataclass
class Param:
	table  : str  = '' 
	columns: List = field(default_factory=list)
	values : List = field(default_factory=list)
	filters: List = field(default_factory=list)

class ParamManager():
	def __init__(self):
		self._params = dict()
		self._cache  = None

	# AUXILIARS
	def _get_table(self, table = None):	
		# Hacemos un cast según el datatype de table (int o string)
		if isinstance(table, str): table = table
		elif isinstance(table, int): table = self._get_table_from_index(table)
		elif table is None: 
			table = self._cache

		return self._params[table]

	def _get_table_from_index(self, index):
		return list(self._params.keys())[index]
		
	def _table_exists(self, table):
		return (table in self._params.keys()) 

	def _create_table(self, table):
		param = Param(table = table)
		self._params[table] = param

	def _drop_table(self, table):
		if self._table_exists(table): self._params[table] = None

	# EXTERNALS
	def get_params(self):
		return self._params

	def get_param_by_index(self, n = 0):
		ret_val = None
		if isinstance(n, int):
			table = list(self._params.keys())[n]
			ret_val = self._params[table]

		return ret_val
		
	def len(self):
		return len(self._params.keys())
		
	def set_table(self, table = None):
		if isinstance(table, str):
			if not self._table_exists(table):
				self._create_table(table)

			self._cache = table

	def set_columns(self, value = None, table = None):
		if isinstance(value, list):
			self._get_table(table).columns = value
		elif isinstance(value, str):
			self._get_table(table).columns.append(value)

	def set_values(self, value = None, table = None):
		if isinstance(value, list):
			self._get_table(table).values = value
		else:
			self._get_table(table).values.append(value)

	def set_filter(self, column = None, cond = None, value = None, logic = 'AND', table = None):
		filter = Filter(column, cond, value, logic)
		self._get_table(table).filters.append(filter)

	# def set_filter_columns(self, value = None, table = None):
	# 	if isinstance(value, list):			
	# 		self._get_table(table).filters.columns = value

	# def set_filter_conds(self, value = None, table = None):
	# 	if isinstance(value, list):
	# 		self._get_table(table).filters.conds = value

	# def set_filter_values(self, value = None, table = None):
	# 	if isinstance(value, list):
	# 		self._get_table(table).filters.values = value
