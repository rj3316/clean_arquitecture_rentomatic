#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#----------------------------------------------------------------------------
# Created By  : Igor Usunariz
# Created Date: 2022/07/26
# version ='3.0'
# Mail = 'i.usunariz.lopez@gmail.com'
#
# ---------------------------------------------------------------------------
# 
# MYSQL MODULE
#
# Dependencies
# sqlalchemy, pymysql, Module
#
# ---------------------------------------------------------------------------

from sqlite3 import IntegrityError
from sqlalchemy import create_engine, false
from sqlalchemy.pool import NullPool

from inspect import getframeinfo, currentframe
from copy import deepcopy

from dataclasses import dataclass, field
from typing import List, Dict

from .Database import Database

class MySql(Database):
	def _initialization(self):
		super()._initialization()

		self._engine = None
		self._conn   = None

		self.query_builder = dict()

		self._tables = dict()

		self._database_ok = False
		
	def _finish_initialization(self):	
		try   : skip_structure = self.data.config['skip_structure']
		except: skip_structure = False

		if not skip_structure:
			payload = f"Getting MySQL database structure..."
			self._send_info(payload)

			database_ok = self._get_structure()
		else: database_ok = self.check_connection_status()

		self._database_ok = database_ok

	# DECORATORS
	def get_query_builder(fnc):
		def wrapper(self, *args, **kwargs):
			params = None

			if 'params' in kwargs.keys():
				params = kwargs['params']
			else:
				if len(args) > 0:
					params = args[0]

			self.query_builder =  QueryBuilder(params = params, tables = self._tables)			
			ret_val = fnc(self, *args, **kwargs)
			self.query_builder = None

			return ret_val

		return wrapper

	def connection(fnc):
		def wrapper(self, *args, **kwargs):
			ret_val = None

			conn = self.connect()

			if conn:
				try:
					ret_val = fnc(self, *args, **kwargs)
				except Exception as e:
					self._error_handler(f"Error executing connection query: ´{e}")
				finally:
					if isinstance(ret_val, Exception):
						payload = ret_val.args[0]
						self._send_error(payload)
					self.disconnect()
			else:
				pass
			return ret_val

		return wrapper

	# CONNECTION
	def connect(self, check = False):
		ret_val = True

		if (self._engine is None) and (self._conn is None):
			# Create connection string
			user     = self.data.config['database']['user']
			password = self.data.config['database']['password']
			host     = self.data.config['database']['host']
			port     = self.data.config['database']['port']
			database = self.data.config['database']['database']
			
			if 'timeout' in self.data.config['database'].keys(): timeout = self.data.config['database']['timeout']
			else: timeout = 2

			connection_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

			# Connect to database
			try:
				self._engine = create_engine(connection_str, poolclass = NullPool, connect_args = {'connect_timeout': timeout})
				self._conn = self._engine.connect()
			except Exception as e:
				ret_val = False
				if check: self._send_error(f"Connection cannot be stablished: {e.args[0].split(',')[-1]}")
		
		return ret_val

	def disconnect(self):
		try:
			self._conn.close()
		except:
			pass

		self._engine = None
		self._conn = None
		
	def check_connection_status(self):
		ret_val = self.connect(check = True)
		self.disconnect()

		return ret_val

	def _set_schema_database(self):
		self.set_database('information_schema')

	def _restore_default_database(self):
		self.set_database(self.data.config['database']['default_db'])

	def set_database(self, database):
		if isinstance(database, str):
			self.data.config['database']['database'] = database

	# CRUD
	@connection
	def _execute(self, query = None):
		ret_val = False

		if query is not None:
			try:
				ret_val = self._conn.execute(query)
			except Exception as e:
				payload = f"Query failed: {e}"
				self._send_warning(payload)
			finally:
				if self.data.debug:
					payload = f"Query: {query}"
					self._send_debug(payload)
		return ret_val

	@get_query_builder
	def select(self, params, force = False):
		ret_val  = list()

		if force:
			exec = True
		else:
			try: skip_structure = self.data.config['skip_structure']
			except: skip_structure = False

			# Check if table exists
			exec  = self._check_if_table_exists(params) or skip_structure
			
		if exec:
			# SELECT column1, column2, ... FROM table WHERE column1 = value1, column2 = value2, ...;            
			self._last_action = 'SELECT'

			# Agregamos los columns a seleccionar
			# query = f"SELECT {self._get_columns_for_query(params)}"
			query = 'SELECT '

			query += self.query_builder.get_columns(params)
			
			# Combprobamos si hay que agregar INNER JOIN
			query += self.query_builder.get_join(params)

			# Agregamos los filtros
			query += self.query_builder.get_filters(params)

			# Comprobamos si hay más 
			query += ';'

			try:
				# Lanzamos la consulta
				rs = self._execute(query)
				ret_val = self._format_select(rs, params)

				if self.data.debug:
					payload = f"Response: {ret_val}"
					self._send_debug(payload)				
			except Exception as e:
				payload = f"Error in select query: {query} [{e}]"
				self._send_warning(payload)

		return ret_val

	@get_query_builder
	def insert(self, params):
		ret_val = None

		try: skip_structure = self.data.config['skip_structure']
		except: skip_structure = False

		# Check if table exists
		exec = self._check_if_table_exists(params) or skip_structure

		if exec:
			# INSERT INTO table column1, column2, ... VALUES value1, value2, ...;
			self._last_action = 'INSERT'

			table = params.get_param_by_index().table
			n_columns = self.get_values_quantity(params)
			n_records  = len(params.get_params())			

			query = f"INSERT INTO {table} ("

			# Agregamos los columns
			query += f"{self.query_builder.get_columns(params)}"
			
			# Agregamos los values
			query += ") VALUES ("
			query += f"{self.query_builder.get_values(params)}"
			query += ');'

			try:
				# Lanzamos la consulta
				ok = self._execute(query)

				if ok: payload = f"INSERT => Succesfully inserted {n_columns} columns in {n_records} records in table \'{table}\'"
				else:  payload = f"INSERT => Cannot insert data on table \'{table}\': Connection failure"
				self._send_debug(payload)

				payload = f"INSERT => Succesfully inserted {n_columns} columns in {n_records} records in table \'{table}\'"
				self._send_debug(payload)

				ret_val = True
			except Exception as e:
				payload = f"INSERT => Cannot insert {n_columns} columns in {n_records} records in table\'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:
			payload = f"INSERT => Cannot insert records in table \'{table}\', it does not exists"
			self._send_warning(payload)

			ret_val = False
			
		return ret_val

	@get_query_builder
	def update(self, params):
		ret_val = None

		try: skip_structure = self.data.config['skip_structure']
		except: skip_structure = False

		# Check if table exists
		exec = self._check_if_table_exists(params) or skip_structure

		if exec:
			# UPDATE table SET column1 = value1, column2 = value2, ... WHERE column1 = value1, column2 = value2, ...;
			self._last_action = 'UPDATE'

			table = params.get_param_by_index().table
			query = f"UPDATE {table}"

			# Añadimos los updates
			query += f"{self.query_builder.get_updates(params)}"

			# Añadimos los filters
			query += f"{self.query_builder.get_filters(params)}"

			query += ';'

			try:
				# Lanzamos la consulta
				ok = self._execute(query)

				if ok: payload = f"UPDATE => Succesfully updated data from table \'{table}\'"
				else:  payload = f"UPDATE => Cannot update data on table \'{table}\': Connection failure" 
				self._send_debug(payload)

				ret_val = True  
			except Exception as e:
				payload = f"UPDATE => Cannot update data on table \'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:
			payload = f"UPDATE => Cannot update data on table \'{table}\', it does not exists"
			self._send_warning(payload)

			ret_val = False

		return ret_val

	@get_query_builder
	def delete(self, params):
		ret_val = None

		try: skip_structure = self.data.config['skip_structure']
		except: skip_structure = False

		table = params.get_param_by_index().table
		# Check if table exists
		exec = self._check_if_table_exists(params) or skip_structure

		if exec:
			# DELETE FROM table WHERE column1 = value1, column2 = value2, ...;
			self._last_action = 'DELETE'
			
			query = f"DELETE FROM {table}"

			query += f"{self.query_builder.get_filters(params)}"

			query += ';'
			
			try:
				# Lanzamos la consulta
				self._execute(query)
				
				payload = f"DELETE => Succesfully deleted data from table \'{table}\'"
				self._send_debug(payload)

				ret_val = True
			except Exception as e:
				payload = f"DELETE => Cannot delete data from table\'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:
			payload = f"DELETE => Cannot delete data from table \'{table}\', it does not exists"
			self._send_warning(payload)

			ret_val = False

		return ret_val

	@get_query_builder
	def check_if_table_exists(self, table):
		ret_val = False

		query = 'SHOW TABLES;'

		rs = self._execute(query)
		for row in rs:
			if table == row[0]:
				ret_val = True
				break
		
		return ret_val

	def _format_select(self, rs, params):
		try:
			ret_val = {
				'columns': list(),
				'data': list()
			}
			# Guardamos las columnas leidas
			ret_val['columns'] = self._get_params_columns(params)

			for row in enumerate(rs):
				ret_val['data'].append(row[1])

			if (self.data.config['database']['database'] != 'information_schema'):
				tmp = deepcopy(ret_val)
				ret_val = dict()

				for i, column in enumerate(tmp['columns']):
					if not column in ret_val.keys():
						ret_val[column] = list()

					for data in tmp['data']:
						ret_val[column] += [data[i]]
		except:
			ret_val = rs
		
		return ret_val

	def _get_params_columns(self, params):
		ret_val = list()

		for _, param in params.get_params().items():
			for column in param.columns:
				ret_val.append(f"{param.table}.{column}".replace(' ', ''))

			if not ret_val:
				try:
					ret_val = self._tables[param.table].get_column_names()
				except Exception as e:
					print(e)

		return ret_val

	# TABLE MANAGEMENT
	@get_query_builder	
	def create_table(self, params = None, force = False):		
		ret_val = None

		# Si queremos recrearla, primero la eliminamos
		if force:
			self.drop_table(params, force = force)

		table = params.get_param_by_index().table
				
		# Conectamos con la BBDD y si la conexión no ha fallado, hacemos la consulta
		if not self._check_if_table_exists(params):
			# CREATE TABLE table (column1 datatype1, column2 datatype2, ...)
			self._last_action = 'CREATE TABLE'

			# ADD COLUMNS AND DATATYPES
			query = f"{self.query_builder.get_create_table(params)}"
			
			# query += ' Engine=InnoDB DEFAULT CHARACTER SET = utf8;'

			# Lanzamos la consulta
			try:
				_ = self._execute(query)
				
				payload = f"CREATE TABLE => Succesfully created table \'{table}\' with {len(params.get_param_by_index().columns)} columns"
				self._send_info(payload)

				ret_val = True
			except Exception as e:
				payload = f"CREATE TABLE => Cannot create table\'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:			
			payload = f"CREATE TABLE => Cannot create table \'{table}\', it already exists"
			self._send_debug(payload)

			ret_val = False

		# Si no ha habido problemas, actualizamos la estructura (solo esa tabla)
		if ret_val:
			self._get_tables(table = table)
		
		return ret_val
	
	@get_query_builder
	def drop_table(self, params, force = False):
		ret_val = False

		table = params.get_param_by_index().table
		# Comprobamos si existe
		if self._check_if_table_exists(params):
			# Si se quiere forzar el borrado
			if force:
				# Disable foreign key check
				query = "SET FOREIGN_KEY_CHECKS=0;"
				self._execute(query)
				
			# DROP TABLE table
			self._last_action = 'DROP TABLE'

			query = f"DROP TABLE {table};"

			# Lanzamos la consulta
			rs = self._execute(query)

			if force:
				# Enable foreign key check
				query = "SET FOREIGN_KEY_CHECKS=1;"
				self._execute(query)
			
			if not isinstance(rs, Exception):
				payload = f"DROP TABLE => Succesfully dropped table \'{table}\'"
				self._send_info(payload)

				self._tables.pop(table)

				ret_val = True
			else:
				if not isinstance(rs, IntegrityError):
					payload = f"DROP TABLE => Cannot drop table \'{table}\': {rs.args[0]}"
					self._send_debug(payload)
		else:
			payload = f"DROP TABLE => Cannot drop table \'{table}\', it does not exists"
			self.self._debug(payload)
			
		return ret_val
	
	def drop_all_tables(self):
		tables = list(self._tables.keys())
		n_tables = len(tables)

		# Creamos un contador de intentos de borrado
		cont = {}
		for table in tables:
			cont[table] = 0

		# Mientras exista alguna, seguimos iterando
		try_lims = n_tables
		exit = (n_tables == 0) 
		while (n_tables > 0) and (not exit):
			# Recorremos todas las tablas
			for i, table in enumerate(tables):
				if cont[table] >= try_lims:
					exit = True
					break

				params = self.get_param_manager()
				params.set_table(table)
				if self.drop_table(params, force = True):
					# Si lo conseguimos, volvemos a empezar (sino falla por haber cambiado el diccionario en tiempo de ejecución del bucle)
					tables.pop(i)
					break
				else:
					cont[table] += 1
					tables.append(tables.pop(0))

			n_tables = len(tables)

	# COLUMN MANAGEMENT
	@get_query_builder
	def add_columns(self, params = None, force = False):
		ret_val  = True

		# Comprobamos si se quiere forzar el borrado
		if force:
			self.drop_columns(params, force = force)

		param = params.get_param_by_index()
		table = param.table

		self._last_action = 'ADD COLUMN'

		# ALTER TABLE table ADD column datatype REFERENCES table_ref(column_ref);
		query = self.query_builder.get_add_columns()

		if query != '':
			# Lanzamos la consulta
			try:
				self._execute(query)
				
				payload = f"ADD COLUMN => Succesfully added columns \'{param.columns}\' to table \'{table}\'"
				self._send_debug(payload)
				self._get_columns(table = table)
			except Exception as e:
				payload = f"ADD COLUMN => Cannot add columns {param.columns} to table\'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:
			payload = f"ADD COLUMN => Cannot add columns {param.columns} to table\'{table}\', already exists"
			self._send_debug(payload)
			ret_val = False
				
		return ret_val
	
	def add_relational_column(self, params):
		ret_val = None

		table = params.get_param_by_index().table

		# Añadimos el column que usaremos como relación, y la convertimos en caso de que se haya creado ahora
		ret_val = self.add_columns(params)
		
		if ret_val:
			ret_val = self.add_relation(params)
			self._get_foreign_keys(table)

		return ret_val

	@get_query_builder
	def add_relation(self, params):
		param_0 = params.get_param_by_index()
		table = param_0.table
		column = param_0.columns[0]

		param_1 = params.get_param_by_index(1)
		foreign_table  = param_1.table
		foreign_column = param_1.columns[0]

		# ALTER TABLE table ADD CONSTRAIN foreign_key FOREIGN KEY (column) REFERENCES table_ref(column_ref);
		self._last_action = 'ADD RELATIONAL COLUMNS'

		query = self.query_builder.get_foreign_relation(params)		
		
		# Lanzamos la consulta
		try:
			self._execute(query)
			
			payload = f"ADD FOREIGN KEY => Succesfully added foreign key on \'{table}.{column}\' with \'{foreign_table}.{foreign_column}\'"
			self._send_debug(payload)

			ret_val = True
		except Exception as e:
			payload = f"ADD FOREIGN KEY => Cannot add foreign key on \'{table}.{column}\' with \'{foreign_table}.{foreign_column}\': {e.args[0]}"
			self._send_warning(payload)

			ret_val = False
		
		return ret_val

	def drop_columns(self, params, force = False):
		ret_val = True

		table = params.get_param_by_index().table
		
		for column in params.get_param_by_index().columns:
			tmp_val = self._drop_column(params, force = force)
			ret_val = ret_val and tmp_val
				
		# Si no ha habido problemas, actualizamos la estructura
		if ret_val:
			self._tables[table].drop_column(column)

		return ret_val

	def _drop_column(self, params = None, force = False):
		ret_val  = True
		
		table = params.get_param_by_index().table
		column = params.get_param_by_index().columns[0]

		# Comprobamos si existe la columna
		if  self._check_if_column_exists(table, column):
			# Si se quiere forzar el borrado
			if force:
				# Disable foreign key check
				query = "SET FOREIGN_KEY_CHECKS=0;"
				self._execute(query)
				
			# ALTER TABLE table ADD column datatype REFERENCES table_ref(column_ref);
			self._last_action = 'DROP COLUMN'

			# query = f"ALTER TABLE {table}"
			query = self.query_builder.query

			# Añadimos el nuevo column y su datatype
			query += f" DROP COLUMN {column}"
			query += ';'

			# Lanzamos la consulta
			try:
				self._execute(query)

				if force:
					# Enable foreign key check
					query = "SET FOREIGN_KEY_CHECKS=1;"
					self._execute(query) 
					
				payload = f"DROP COLUMN => Succesfully dropped column \'{column}\' from table \'{table}\'"
				self._send_debug(payload)
			except Exception as e:
				payload = f"DROP COLUMN => Cannot drop column {column} from table\'{table}\': {e.args[0]}"
				self._send_warning(payload)

				ret_val = False
		else:
			payload = f"DROP COLUMN => Cannot drop column \'{column}\' from table \'{table}\', it does not exists"
			self._send_warning(payload)

		return ret_val

	# STRUCTURE
	def _get_structure(self):
		ret_val = True

		tmp_val = self._get_tables()
		ret_val = ret_val and tmp_val

		tmp_val = self._get_foreign_keys()
		ret_val = ret_val and tmp_val

		return ret_val

	def _get_tables(self, table = None):
		ret_val = True

		# SHOW TABLES;
		if table is None:
			self._last_action = 'SHOW TABLES'
			query = "SHOW TABLES;"

			rs = self._execute(query)
			tables = list(map(lambda x: x[0], rs))

			# Inicializamos la lista de tablas
			self._tables = dict()			
		else:
			tables = [table]

		try:
			for i, tablename in enumerate(tables):
				config = {		
					'i'    : i,
					'table': tablename,
				}
				table = Table(config)
				self._tables[tablename] = table

				# Leemos la estructura de columnas de la tabla
				self._get_columns(tablename)

		except Exception as e:
			self._tables = None
			ret_val = False

			info = getframeinfo(currentframe()) # frameinfo.lineno, frameinfo.filename
			payload = f"[{info.lineno+1}] Failed getting tables for Foreign Keys"
			self._error_handler(payload)
		
		return ret_val

	def _get_columns(self, table):
		ret_val   = list()

		# Lanzamos la consulta
		try:
			# DESCRIBE table;
			query = f"DESCRIBE {table};"
			rs = self._execute(query)
			
			for row in rs:
				if not self._tables[table].exists_column(row[0]):
					# Obtenemos nombre del column
					config = {
						'table'    : table,
						'column'   : row[0],
						'datatype' : self.__cast_datatypes(row[1]),
						'auto'     : ('auto_increment' in row[5]),
						'key'      : row[3],
					}
					column = Column(config)
					self._tables[table].add_column(column)
		except Exception as e:
			info = getframeinfo(currentframe()) # frameinfo.lineno, frameinfo.filename
			self._error_handler(f"[{info.lineno}] Error getting columns for Foreign Keys")

		return ret_val

	def _get_foreign_keys(self, table = None):
		ret_val  = False
		payloads = list()

		try:		  
			self._set_schema_database()
			try:
				fk_keys    = self._get_fk_keys(table)
				fk_tables  = self._get_fk_tables(table, fk_keys)
				fk_columns = self._get_fk_columns(table, fk_keys)
			except Exception as e:
				self._send_error(f"Error getting foreign keys: {e}")
				fk_keys    = list()
				fk_tables  = list()
				fk_columns = list()
			finally:
				self._restore_default_database()

			for fk_table, fk_column in zip(fk_tables, fk_columns):
				key_table      = fk_table[0]
				key_column     = fk_column[0]

				if key_table == key_column:
					key = key_table.split('/')[-1]

					table          = fk_table[1].split('/')[-1]
					foreign_table  = fk_table[2].split('/')[-1]

					column         = fk_column[1]
					foreign_column = fk_column[2]

					# Guardamos la relación en la tabla principal
					config = {
						'key': key,
						'table': table,
						'column': column,
						'foreign_table': foreign_table,
						'foreign_column': foreign_column,
					}
					fk = Fk(config)
					self._tables[table].add_foreign_key(fk)

					# Guardamos la relación inversa en la tabla relacionada
					fk_foreign = Fk(config)
					fk_foreign.shift_foreign_source()
					self._tables[foreign_table].add_foreign_key(fk_foreign)                    
			ret_val = True
		except KeyError as e:
			info = getframeinfo(currentframe()) # frameinfo.lineno, frameinfo.filename
			payload = f"[{info.lineno+1}] Failed getting foreign keys: Key error - {e.args[0]}"
			payloads.append(payload)
		except Exception as e:
			info = getframeinfo(currentframe()) # frameinfo.lineno, frameinfo.filename
			payload = f"[{info.lineno+1}] Failed getting foreign keys: {e.args[0]}"
			payloads.append(payload)

		return ret_val

	def _get_fk_keys(self, table = None):
		ret_val  = list()

		try:
			db = self.data.config['database']['default_db']

			# Obtenemos las KEYS con FOREIGN KEY CONSTRAINT
			params = self.get_param_manager()
			params.set_table('TABLE_CONSTRAINTS')
			params.set_columns(['TABLE_NAME', 'CONSTRAINT_NAME'])

			# Filter f1
			params.set_filter('TABLE_SCHEMA', '=', db)
			params.set_filter('CONSTRAINT_TYPE', '=', 'FOREIGN KEY')
			params.set_filter('CONSTRAINT_NAME', '<>', 'PRIMARY')

			if not table is None:
				params.set_filter('TABLE_NAME', '=', table)

			ret_val = self.select(params, force = True)

			if isinstance(ret_val, dict):
				ret_val = ret_val['data']
		except Exception as e:
			payload = f"Error getting FK_TABLES: {e}"
			self._send_warning(payload)

			ret_val = None
			
		return ret_val

	def _get_fk_tables(self, table = None, fk_keys = None):
		ret_val  = None

		try:
			db = self.data.config['database']['default_db']

			# Obtenemos las TABLAS desde INNODB_SYS_FOREIGN
			params = self.get_param_manager()
			params.set_table('INNODB_SYS_FOREIGN')
			params.set_columns(['ID', 'FOR_NAME', 'REF_NAME'])

			# Añadimos el filtro de fk_keys, si existe
			if (not table is None) and (not fk_keys is None):
				for fk_key in fk_keys:
					params.set_filter('ID', '=', f'{db}/{fk_key[1]}', 'OR')

			ret_val = self.select(params, force = True)

			if isinstance(ret_val, dict):
				ret_val = ret_val['data']
		except Exception as e:
			payload = f"Error getting FK_TABLES for {fk_keys}: {e}"
			self._send_warning(payload)

			ret_val = None

		return ret_val

	def _get_fk_columns(self, table = None, fk_keys = None):
		ret_val  = None

		try:
			db = self.data.config['database']['default_db']

			# Obtenemos las COLUMNAS RELACIONADAS desde INNODB_SYS_FOREIGN_COLS
			params = self.get_param_manager()
			params.set_table('INNODB_SYS_FOREIGN_COLS')
			params.set_columns(['ID', 'FOR_COL_NAME', 'REF_COL_NAME'])

			# Añadimos el filtro de fk_keys, si existe
			if (not table is None) and (not fk_keys is None):
				for fk_key in fk_keys:
					params.set_filter('ID', '=', f'{db}/{fk_key[1]}', 'OR')

			ret_val = self.select(params, force = True)

			if isinstance(ret_val, dict):
				ret_val = ret_val['data']
		except Exception as e:
			payload = f"Error getting FK_COLUMNS for {fk_keys}: {e}"
			self._send_warning(payload)

			ret_val = None
		
		return ret_val

	# OTHERS
	def is_database_ok(self):
		ret_val = self.check_connection_status()

		return ret_val

	def __cast_datatypes(self, datatype):
		ret_val = 'string'
		if 'int' in datatype:
			ret_val = 'int'
		elif 'float' in datatype:
			ret_val = 'float'
		elif 'varchar' in datatype:
			ret_val = 'string'
		elif 'date' in datatype:
			ret_val = 'date'
			
		return ret_val
	
	def _get_column_datatype(self, table, column):
		try:
			ret_val = self._tables[table].get_column_datatype(column)
		except:
			ret_val = None

		return ret_val
		
	def _check_if_table_exists(self, params):
		ret_val = True

		for _, param in params.get_params().items():
			ret_val = ret_val and (param.table in self._tables.keys())
			if not ret_val: break

		return ret_val
			   
	def _check_if_column_exists(self, table, column):
		try:
			return column in self._tables[table].get_column_names()
		except Exception as e:
			pass
		
	def get_values_quantity(self, params):
		params = params.get_params()

		ret_val = 0
		for _, param in params.items():
			ret_val += len(param.values)
		
		return ret_val

	def get_rs_len(self, rs):
		try:
			ret_val = len(rs[list(rs.keys())[0]])
		except:
			ret_val = 0
		
		return ret_val

	def get_rs_is_empty(self, rs):		
		n = self.get_rs_len(rs)
		ret_val = (n == 0)

		return ret_val

class Table():
	def __init__(self, config):
		self._primary      = None
		self._columns      = dict()
		self._fks          = dict()

		self._i     = config['i']
		self._table = config['table']

		if self._columns:
			self._get_primary()
	
	@property
	def columns(self):
		return self._columns
	
	@columns.setter
	def columns(self, value):
		self._columns = value

	def get_table(self):
		return self._table

	def _get_primary(self):
		for _, column in self._columns.items():
			if column.is_primary():
				self._primary = column.get_column()
				break

	def get_column_names(self):
		return list(self.columns.keys())

	def get_column_datatype(self, column):
		return self._columns[column].get_datatype()
	
	def get_column_auto(self, column):
		return self._columns[column].get_auto()
	
	def drop_column(self, column):
		if column in self._columns.keys():
			self._columns.pop(column)

	def get_foreign_key(self, foreign_table = None):
		ret_val = None
		if not foreign_table is None:
			ret_val = self._fks[foreign_table]
	
		return ret_val

	def exists_column(self, column = None):
		if column is not None:
			if isinstance(column, Column):
				ret_val = column.get_column() in self._columns.keys()
			elif isinstance(column, str):
				ret_val = column in self._columns.keys()
			else:
				ret_val = False
		else:
			ret_val = False
		
		return ret_val

	# ADD / DROP
	def add_column(self, column, replace = False):
		if isinstance(column, Column):
			if not self.exists_column(column):
				self._columns[column.get_column()] = column
			else:
				if replace:
					self._columns[column.get_column()] = column
			ret_val = True
		else:
			ret_val = False
		
		return ret_val 

	def add_foreign_key(self, fk = None, replace = False):
		if isinstance(fk, Fk):
			if not fk.get_foreign_table() in self._fks.keys():
				self._fks[fk.get_foreign_table()] = fk
			else:
				if replace:
					self._fks[fk.get_foreign_table()] = fk
			ret_val = True
		else:
			ret_val = False
		
		return ret_val            

	def drop_column(self, column = None):
		if column is not None:
			if self.exists_column(column):
				if isinstance(column, Column):
					column = column.get_column()

				self._columns.pop(column)

			ret_val = True
		else:
			ret_val = False
		
		return ret_val

	def drop_foreign_key(self, table = None):
		if table is not None:
			self._fks.pop(table)

			ret_val = True
		else:
			ret_val = False
		
		return ret_val

class Column():
	def __init__(self, config):
		self._table    = config['table']
		self._column   = config['column']
		self._datatype = config['datatype']
		self._auto     = config['auto']
		self._key      = config['key']
		
	def is_primary(self):
		return (self._key == 'PRI')
	
	def get_column(self):
		return self._column
	
	def get_datatype(self):
		return self._datatype

	def get_auto(self):
		return self._auto

class Fk():
	def __init__(self, config):
		self._key    = config['key']
		self._table  = config['table']
		self._column = config['column']
		self._foreign_table  = config['foreign_table']
		self._foreign_column = config['foreign_column']
	
	def get_key(self):
		return self._key

	def get_foreign_table(self):
		return self._foreign_table
	
	def get_foreign_column(self):
		return self._foreign_column
	
	def get_table(self):
		return self._table

	def get_column(self):
		return self._column
	
	def get_relational_column(self, table):
		if table == self._table:
			ret_val = self._column
		elif table == self._foreign_table:
			ret_val = self._foreign_column
		
		return ret_val

	def shift_foreign_source(self):
		tmp_table = self._table
		tmp_column = self._column

		self._table  = self._foreign_table
		self._column = self._foreign_column
		self._foreign_table  = tmp_table
		self._foreign_column = tmp_column

@dataclass
class QueryBuilder():
	params: Dict = field(default_factory=dict)
	tables: Dict = field(default_factory=dict)
	query : str = ''

	# AUXILIARS
	def _get_params(self, params = None):
		if params is None:
			ret_val = self.params
		else:
			ret_val = params
		
		return ret_val

	def _get_tables(self, tables = None):
		if tables is None:
			ret_val = self.tables
		else:
			ret_val = tables
		
		return ret_val

	def _filter(self, filter = None):
		ret_val = False
		if filter is not None:
			c0 = filter.column is not None
			c1 = filter.cond is not None
			c2 = filter.value is not None
			ret_val =  c0 and c1 and c2
		
		return ret_val

	def _cast_value_with_datatype(self, table, column, value):
		try:
			# Obtenemos el datatype y si es auto_increment de la columna actual
			auto     = self.tables[table].get_column_auto(column)
			datatype = self.tables[table].get_column_datatype(column)
		except Exception as e:
			auto     = False
			if isinstance(value, str):
				datatype = 'string'
			else:
				datatype = 'int'

		# Adecuamos el formato del string SQL al tipo de dato
		if auto and ((value == '') or (value is None)):
			# Si es AUTO_INCREMENT, lo ponemos a NULL (será MySQL el encargado de poner el que corresponda)
			ret_val = 'NULL'
		else:
			if datatype == 'string':
				# Si es STRING, añadimos comillas simples ('')
				ret_val = f"\'{value}\'"
			elif datatype == 'date':
				# Si es DATE, añadimos almohadillas (##)
				ret_val = f"#{value}#"
			else:
				# Si no, ponemos el valor directamente
				ret_val = f"{value}"
		
		return ret_val

	# EXTERNALS
	def get_create_table(self, params = None):
		params = self._get_params(params)
		ret_val = ''

		if params is not None:
			param = params.get_param_by_index()

			ret_val += f"CREATE TABLE IF NOT EXISTS {param.table} ("

			for i, (column, value) in enumerate(zip(param.columns, param.values)):
				if i > 0: ret_val += ', '

				ret_val += f"{column} {value}" 


			ret_val += ')'
		
		ret_val += ' Engine=InnoDB DEFAULT CHARACTER SET = utf8;'

		return ret_val

	def get_columns(self, params = None):
		params = self._get_params(params).get_params()

		ret_val = ''

		if params is not None:
			for i, (_, param) in enumerate(params.items()):
				for j, column in enumerate(param.columns):
					if (i > 0) or (j > 0): ret_val += ', '

					ret_val += f"{param.table}.{column}"
		
		if ret_val == '': ret_val = '*'

		return ret_val
	
	def get_values(self, params = None):
		params = self._get_params(params).get_params()

		ret_val = ''

		if params is not None:
			for i, (_, param) in enumerate(params.items()):
				for j, (value, column) in enumerate(zip(param.values, param.columns)):
					if (i > 0) or (j > 0): ret_val += ', '
					ret_val += self._cast_value_with_datatype(param.table, column, value)
		
		return ret_val
	
	def get_filters(self, params = None):
		params = self._get_params(params).get_params()

		ret_val = ''

		if params is not None:
			for _, param in params.items():
				for filter in param.filters:
					if self._filter(filter):
						if ret_val == '': ret_val += ' WHERE ('
						if (ret_val != ' WHERE ('): ret_val += f" {filter.logic} "

						value = self._cast_value_with_datatype(param.table, filter.column, filter.value)
						ret_val += f"{param.table}.{filter.column}{filter.cond}{value}"					
					
			if ret_val != '': ret_val += ')'
		
		return ret_val

	def get_updates(self, params = None):
		params = self._get_params(params).get_params()

		ret_val = ' '

		if params is not None:
			ret_val += 'SET '

			# Recorremos los updates
			for _, param in params.items(): 
				for column, value in zip(param.columns, param.values):
					if ret_val != ' SET ': ret_val += ', '

					value = self._cast_value_with_datatype(param.table, column, value)

					ret_val += f"{param.table}.{column}={value}"

		return ret_val		

	def get_join(self, params = None):
		params = self._get_params(params)

		ret_val = ''

		if params is not None:
			table = params.get_param_by_index().table

			# Agregamos la tabla
			ret_val = f" FROM {table}"

			# Recorremos todos las tablas adicionales
			params = params.get_params()
			if len(params) > 1:
				for _, param in params.items():
					if param.table != table:
						# INNER JOIN table2 ON table1.column1 = table2.column2
						ret_val += f" INNER JOIN {param.table}"

						fk = self.tables[table].get_foreign_key(param.table)

						if not fk is None:
							ret_val += f" ON {table}.{fk.get_relational_column(table)} = {param.table}.{fk.get_relational_column(param.table)}"
						else:
							self._send_warning(f"Not relation found between tables {table} and {param.table}")
			
		return ret_val

	def get_add_columns(self, params = None):
		params = self._get_params(params)

		ret_val = ''

		if params is not None:
			param = params.get_param_by_index()

			ret_val = f"ALTER TABLE {param.table} "

			columns = ''
			for i, (column, value) in enumerate(zip(param.columns, param.values)):
				if not self.tables[param.table].exists_column(column):
					if i > 0: columns += ', '
					columns += f"ADD COLUMN {column} {value}"
			
			if columns == '': ret_val = ''
			else: ret_val += f"{columns};"
		
		return ret_val

	def get_foreign_relation(self, params = None):
		ret_val = ''

		if params is not None:
			if params.len() == 2:
				table  = params.get_param_by_index().table
				column = params.get_param_by_index().columns[0]

				foreign_table  = params.get_param_by_index(1).table
				foreign_column = params.get_param_by_index(1).columns[0]

				ret_val += f"ALTER TABLE {table}"
				ret_val += " ADD CONSTRAINT"
				
				ret_val += f" fk_{table}_{foreign_table}"

				ret_val += f" FOREIGN KEY ({column})"
				
				ret_val += ' REFERENCES'

				ret_val += f" {foreign_table} ({foreign_column})"

				ret_val += f" ON DELETE CASCADE"
					
				ret_val += f" ON UPDATE CASCADE"
				ret_val += ';'


		return ret_val

	def delete_parenthesis(self, query):
		if isinstance(query, str): ret_val = query.replace('(', '').replace(')', '')
		else: ret_val = query

		return ret_val

	


