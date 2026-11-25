import tempfile
import unittest
import gc
from pathlib import Path
from unittest.mock import patch

from src.dao import improvement_dao


class ImprovementDaoTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "test.db"
        self.db_patch = patch.object(improvement_dao, "DB_FILE", self.db_file)
        self.db_patch.start()
        improvement_dao.init_db()

    def tearDown(self):
        self.db_patch.stop()
        gc.collect()
        self.temp_dir.cleanup()

    def test_save_and_load_successful_result(self):
        saved = improvement_dao.save_results(
            {"input": "Improve this text", "output": "Improve this text clearly."}
        )

        self.assertEqual(saved, 1)
        self.assertEqual(
            improvement_dao.load_history(),
            [("Improve this text", "Improve this text clearly.")],
        )

    def test_error_result_is_not_saved(self):
        saved = improvement_dao.save_results(
            {"input": "Improve this text", "output": "error"}
        )

        self.assertEqual(saved, 0)
        self.assertEqual(improvement_dao.load_history(), [])


if __name__ == "__main__":
    unittest.main()
