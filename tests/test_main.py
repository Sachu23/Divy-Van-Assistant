import unittest


class TestMain(unittest.TestCase):
    def test_imports(self):
        """
        Tests whether the files are imported correctly or not
        """

        import PySimpleGUI as sg

        import src.gui.login_page
        self.assertTrue(hasattr(src.gui.login_page, 'Login'))

        import src.dashboard
        self.assertTrue(hasattr(src.dashboard, 'Dashboard'))

        import src.reports.reports
        self.assertTrue(hasattr(src.reports.reports, 'Report'))

        import src.gui.login_page
        self.assertTrue(hasattr(src.gui.login_page, 'Login'))

        # from databases.stations.database_creation import get_collection
        # from databases.stations.emulate_real_world import start_background_process


if __name__ == "__main__":
    unittest.main()
