import time

from django.db import connections
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError



class Command(BaseCommand):
	"""Stops the execution till the database is available"""

	def handle(self, *args, **options):
		"""It handles our command"""
		self.stdout.write('Database is starting.....')
		db_conn = None

		while not db_conn:
			try:
				db_conn = connections['default']
			except OperationalError:
				self.stdout.write('Database will be starting in one second....')
				time.sleep(1)


		self.stdout.write(self.style.SUCCESS('Database has started successfully!'))
			