import unittest
import pymongo
import threading

import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from src.databases.stations.database_creation import get_collection
from src.databases.stations.emulate_real_world import start_background_process
from src.databases.stations.update_stations import random_update_availability


class TestEmulator(unittest.TestCase):
    def test_creation(self):
        table = get_collection()
        self.assertIsInstance(table, pymongo.collection.Collection)
        self.assertIsNotNone(table)

    def test_random_update(self):
        table = get_collection()
        query = {"Station Name": "Burnham Harbor"}
        init_station1 = table.find_one(query)

        random_update_availability(table)

        udt_station1 = table.find_one(query)

        self.assertNotEqual(init_station1['Bikes Available'], udt_station1['Bikes Available'])

    def test_thread(self):
        table = get_collection()
        start_background_process(table)
        current_threads = threading.enumerate()
        thread_name = "Thread-1 (emulate_real_world)"

        self.assertEqual(thread_name, current_threads[-1].name)


if __name__ == "__main__":
    unittest.main()
