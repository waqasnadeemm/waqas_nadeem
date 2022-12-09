"""Implements a MySQL Persistence Wrapper"""

from persistence_wrapper_interface import PersistenceWrapperInterface
from mysql import connector


class MySQLPersistenceWrapper(PersistenceWrapperInterface):
	"""Implements MySQL Persistence Wrapper"""

	def __init__(self):
		"""Initializes """
		# Constants
		self.SELECT_ALL_INVENTORIES = 'SELECT id, name, description, date_created FROM inventories;'
		self.INSERT = 'INSERT INTO items (inventory_id, item, count) VALUES(%s, %s, %s);'
		self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID = 'SELECT id, inventory_id, item, count FROM items WHERE inventory_id = %s;'
		self.INSERT_INV = 'INSERT INTO INVENTORIES (name, description, date_created) VALUES(%s, %s, %s);'
		self.SEARCH_BY_ID = 'SELECT * FROM ITEMS WHERE id = %s'
		self.SEARCH_BY_NAME = 'SELECT * FROM ITEMS WHERE item = %s'
		# Database Configuration Constants
		self.DB_CONFIG = {}
		self.DB_CONFIG['database'] = 'home_inventory'
		self.DB_CONFIG['user'] = 'home_inventory_user'
		self.DB_CONFIG['host'] = '127.0.0.1'
		self.DB_CONFIG['port'] = 8889
		self.DB_CONFIG['autocommit'] = True

		# Database Connection
		self._db_connection = self._initialize_database_connection(self.DB_CONFIG)

	def get_all_inventories(self):
		"""Returns a list of all rows in the inventories table"""
		cursor = None
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SELECT_ALL_INVENTORIES)
			results = cursor.fetchall()
			print(results)
		except Exception as e:
			print(f'Exception in persistence wrapper: {e}')
		return results

	def get_items_for_inventory(self, inventory_id):
		"""Returns a list of all items for given inventory id"""
		cursor = None
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SELECT_ALL_ITEMS_FOR_INVENTORY_ID, ([inventory_id]))
			results = cursor.fetchall()
		except Exception as e:
			print(f'Exception in persistence wrapper: {e}')
		return results

	def create_inventory(self, name: str, description: str, date_created: str):
		"""Insert new row into inventories table."""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.INSERT_INV, (name, description, date_created))

		except Exception as e:
			print(f'Exception in persistence wrapper: {e}')

	def create_item(self, inventory_id: int, item: str, count: int):
		"""Insert new row into items table for given inventory id"""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.INSERT, (inventory_id, item, count))
		except Exception as e:
			print(f'Exception in persistence wrapper: {e}')

	def search_by_id(self, item_id: int):
		"""Search item from items tables using item id."""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SEARCH_BY_ID, [item_id])
			search = cursor.fetchall()
		except Exception as e:
			print(f'Exception in persistence wrapper1: {e}')
		return search

	def search_by_name(self, item_name: str):
		"""Search item from items tables using item name."""
		try:
			cursor = self._db_connection.cursor()
			cursor.execute(self.SEARCH_BY_NAME, [item_name])
			search = cursor.fetchall()
		except Exception as e:
			print(f'Exception in persistence wrapper: {e}')
		return search

	def _initialize_database_connection(self, config):
		"""Initializes and returns database connection pool."""
		cnx = None
		try:
			cnx = connector.connect(pool_name='dbpool', pool_size=10, **config)
		except Exception as e:
			print(e)
		return cnx



