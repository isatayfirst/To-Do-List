import argparse
import json
from pathlib import Path
from typing import Any

DEFAULT_STATUS = "Not complete"
ALLOWED_STATUSES = {"in progress": "In progress", "done": "Done", "not complete": "Not complete"}


class TaskTracker:
    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = Path(file_path)

    def _load_tasks(self) -> list[dict[str, Any]]:
        if not self.file_path.exists():
            return []
        with self.file_path.open("r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return []
        return data if isinstance(data, list) else []

    def _save_tasks(self, tasks: list[dict[str, Any]]) -> None:
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)

    def add_task(self, description: str, status: str = DEFAULT_STATUS) -> dict[str, Any]:
        tasks = self._load_tasks()
        next_id = max((task["id"] for task in tasks), default=0) + 1
        task = {"id": next_id, "description": description, "status": self.normalize_status(status)}
        tasks.append(task)
        self._save_tasks(tasks)
        return task

    def update_task(self, task_id: int, description: str | None = None, status: str | None = None) -> dict[str, Any]:
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                if description is not None:
                    task["description"] = description
                if status is not None:
                    task["status"] = self.normalize_status(status)
                self._save_tasks(tasks)
                return task
        raise ValueError(f"Task with id {task_id} not found")

    def delete_task(self, task_id: int) -> None:
        tasks = self._load_tasks()
        filtered_tasks = [task for task in tasks if task["id"] != task_id]
        if len(filtered_tasks) == len(tasks):
            raise ValueError(f"Task with id {task_id} not found")
        self._save_tasks(filtered_tasks)

    def list_tasks(self, status: str = "all") -> list[dict[str, Any]]:
        tasks = self._load_tasks()
        if status.lower() == "all":
            return tasks
        normalized_status = self.normalize_status(status)
        return [task for task in tasks if task.get("status") == normalized_status]

    @staticmethod
    def normalize_status(status: str) -> str:
        key = status.strip().lower()
        if key not in ALLOWED_STATUSES:
            allowed = ", ".join(ALLOWED_STATUSES.values())
            raise ValueError(f"Invalid status '{status}'. Allowed statuses: {allowed}")
        return ALLOWED_STATUSES[key]


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI task tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", help="Task description")
    add_parser.add_argument("--status", default=DEFAULT_STATUS, help="Task status")

    update_parser = subparsers.add_parser("update", help="Update an existing task")
    update_parser.add_argument("id", type=int, help="Task ID")
    update_parser.add_argument("--description", help="New task description")
    update_parser.add_argument("--status", help="New task status")

    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("id", type=int, help="Task ID")

    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", default="all", help="Filter by status")

    return parser


def _print_tasks(tasks: list[dict[str, Any]]) -> None:
    if not tasks:
        print("No tasks found")
        return
    for task in tasks:
        print(f"{task['id']}. [{task['status']}] {task['description']}")


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    tracker = TaskTracker()

    try:
        if args.command == "add":
            task = tracker.add_task(args.description, args.status)
            print(f"Task added: {task['id']}. [{task['status']}] {task['description']}")
        elif args.command == "update":
            if args.description is None and args.status is None:
                parser.error("update requires --description and/or --status")
            task = tracker.update_task(args.id, args.description, args.status)
            print(f"Task updated: {task['id']}. [{task['status']}] {task['description']}")
        elif args.command == "delete":
            tracker.delete_task(args.id)
            print(f"Task {args.id} deleted")
        elif args.command == "list":
            _print_tasks(tracker.list_tasks(args.status))
    except ValueError as error:
        parser.exit(status=1, message=f"Error: {error}\n")


if __name__ == "__main__":
    main()
