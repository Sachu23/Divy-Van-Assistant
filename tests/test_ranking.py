import unittest
import pymongo
import random
import pandas as pd

import sys
import os
sys.path.append(os.path.dirname(os.getcwd()))

from src.ranking.transportation.create_operation import Operations
from src.ranking.transportation.create_station import Station
from src.ranking.transportation.create_task import Tasks
from src.ranking.transportation.optimal_route_generation import get_converted_dist, get_directions


class TestEmulator(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.obj = Operations(radius=0.5, logins=1)

    def test_dataset_import(self):
        self.assertIsNotNone(self.obj.dataset)
        self.assertIsInstance(self.obj.dataset, pd.DataFrame)

    def test_subset(self):
        sub = self.obj.generate_subset_dataset()
        self.assertLessEqual(max(sub[' Distance from Base (TBH)']), self.obj.select_radius)

    def test_stations_list(self):
        sub = self.obj.generate_subset_dataset()
        esl, dsl = self.obj.generate_stations_list(sub)

        self.assertIsNotNone(esl)
        self.assertIsNotNone(dsl)
        self.assertNotEqual(esl, [])
        self.assertNotEqual(dsl, [])

        for each in esl:
            self.assertEqual(each.status, 'Excess')
        for each in dsl:
            self.assertEqual(each.status, 'Deficit')

    def test_station_generation(self):
        sub = self.obj.generate_subset_dataset()
        row_no = random.randint(0, len(sub))
        row = sub.iloc[row_no]

        self.assertIsNotNone(row)
        self.obj2 = Station(row)

        self.assertEqual(self.obj2.name, row['Station Name'])
        self.assertEqual(self.obj2.address, row['Address'])
        self.assertEqual(self.obj2.docks, row['Total Docks'])
        self.assertEqual(self.obj2.bikes_available, row['Bikes Available'])
        self.assertEqual(self.obj2.status, row['Station Status'])
        self.assertEqual(self.obj2.distance_ref, row[' Distance from Base (TBH)'])
        self.assertEqual(self.obj2.zipcode, row['Zipcode'])
        self.assertEqual(self.obj2.pluscode, row['Station Plus-Codes'])

    def test_task_generation(self):
        self.obj3 = Tasks()
        sub = self.obj.generate_subset_dataset()
        esl, dsl = self.obj.generate_stations_list(sub)

        esl_no = random.randint(0, len(esl)-1)
        e_s = esl[esl_no]

        dsl_no = random.randint(0, len(dsl)-1)
        d_s = dsl[dsl_no]

        self.assertIsNotNone(e_s)
        self.assertIsNotNone(d_s)

        self.obj3.initialize_required_params(d_s)

        self.obj3.update_end_station()
        self.assertEqual(self.obj3.end_name, d_s.name)
        self.assertEqual(self.obj3.end_address, d_s.address)
        self.assertEqual(self.obj3.end_pluscode, d_s.pluscode)

        self.obj3.update_bikes_required()

        _ = self.obj3.update_start_station([e_s], [])
        self.obj3.update_optimal_route()

    def test_optimal_route(self):
        sub = self.obj.generate_subset_dataset()
        esl, dsl = self.obj.generate_stations_list(sub)

        esl_no = random.randint(0, len(esl)-1)
        e_s = esl[esl_no]

        dsl_no = random.randint(0, len(dsl)-1)
        d_s = dsl[dsl_no]

        start = e_s.pluscode
        end = d_s.pluscode

        route, dist = get_directions(start, end)

        self.assertIsNotNone(route)
        self.assertNotEqual(route, [])

    def test_task_ranking(self):
        sub = self.obj.generate_subset_dataset()
        esl, dsl = self.obj.generate_stations_list(sub)
        gtl = self.obj.generate_tasks_list(esl, dsl)

        self.assertIsNotNone(gtl)
        self.assertNotEqual(gtl, [])


if __name__ == "__main__":
    unittest.main()
