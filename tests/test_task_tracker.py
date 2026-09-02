import tempfile
import unittest
from pathlib import Path

from task_tracker import TaskTracker


class TaskTrackerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.tasks_file = Path(self.temp_dir.name) / "tasks.json"
        self.tracker = TaskTracker(str(self.tasks_file))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_add_task_uses_default_status(self) -> None:
        task = self.tracker.add_task("Write tests")

        self.assertEqual(task["id"], 1)
        self.assertEqual(task["status"], "Not complete")
        self.assertEqual(len(self.tracker.list_tasks()), 1)

    def test_update_task_description_and_status(self) -> None:
        task = self.tracker.add_task("Initial")

        updated = self.tracker.update_task(task["id"], description="Updated", status="Done")

        self.assertEqual(updated["description"], "Updated")
        self.assertEqual(updated["status"], "Done")

    def test_delete_task_removes_task(self) -> None:
        task = self.tracker.add_task("Delete me")

        self.tracker.delete_task(task["id"])

        self.assertEqual(self.tracker.list_tasks(), [])

    def test_list_tasks_filters_by_status(self) -> None:
        self.tracker.add_task("A", status="Done")
        self.tracker.add_task("B", status="In progress")
        self.tracker.add_task("C", status="Not complete")

        done_tasks = self.tracker.list_tasks("done")
        in_progress_tasks = self.tracker.list_tasks("in progress")
        not_complete_tasks = self.tracker.list_tasks("not complete")

        self.assertEqual([task["description"] for task in done_tasks], ["A"])
        self.assertEqual([task["description"] for task in in_progress_tasks], ["B"])
        self.assertEqual([task["description"] for task in not_complete_tasks], ["C"])


if __name__ == "__main__":
    unittest.main()
