"""Test custom django management commands"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
# Mocking this method (check) in BaseCommand class
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])
        #  Make sure Check method is called from wait_for_db.py and db is ready

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        # The parameters depends on levels of patch used
        # ex:last patch stands for first parameter
        # second last becomes second parameter etc
        """Test waiting for database if database is not ready"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # patch should raise psycop error 2 times
        # and OperationalError 3 times when db is not ready

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        #  Mock check method was called 6 times 2*3 until True is returned
        patched_check.assert_called_once_with(databases=['default'])

