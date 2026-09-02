# To-Do-List

Консольное приложение (CLI) на Python для управления задачами. Данные сохраняются в локальный файл `tasks.json`.

## Возможности
- Добавление задачи
- Обновление описания и/или статуса (`In progress`, `Done`, `Not complete`)
- Удаление задачи
- Просмотр всех задач
- Фильтрация задач по статусу (`all`, `in progress`, `done`, `not complete`)

## Использование
```bash
python task_tracker.py add "Купить молоко"
python task_tracker.py update 1 --description "Купить молоко и хлеб" --status "In progress"
python task_tracker.py list
python task_tracker.py list --status done
python task_tracker.py delete 1
```
