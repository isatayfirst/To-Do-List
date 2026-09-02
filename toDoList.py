#Добавление, обновление и удаление задач
#Отметьте задачу как «в процессе» или «выполнено».
#Перечислите все задачи
#Перечислите все выполненные задачи.
#Перечислите все невыполненные задачи.
#Перечислите все задачи, которые находятся в процессе выполнения.
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = os.path.join(BASE_DIR, "todo.json")
todolist = {}
crnt_id = 1

def load_tasks():
    global todolist, crnt_id
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as f:
                todolist = json.load(f)
                if todolist:
                    max_id = max(int(k) for k in todolist.keys())
                    crnt_id = max_id + 1
        except json.JSONDecodeError:
            todolist = {}

def save_tasks():
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(todolist, f, ensure_ascii=False, indent=4)

load_tasks()

def checkID(ID, todolist):
    return str(ID) in todolist

def create_task():
    global crnt_id
    print("-----")
    write = input("Type here: ")
    status = "In progress"
    todolist[str(crnt_id)] = [status, write]
    crnt_id += 1
    save_tasks()
    print("Operation is done")
    print("-----")

def update_task():
    print("-----")
    print(todolist)
    if not todolist:
        print("No tasks available to update.")
        print("-----")
        return
        
    numberTask = input("What task would you like to update? Choose its ID: ")
    
    if checkID(numberTask, todolist):
        operationTask = input("What would you like to do? New text(1), status(2) or both(3)? ")
        if operationTask.lower() == "new text" or operationTask == "1" or operationTask.lower() == "text":
            write = input("Type here: ")
            todolist[numberTask][1] = write
        elif operationTask == "2" or operationTask.lower() == "status":
            check_status = input("Is this task in progress(1), done(2) or not complete(3)? ")
            todolist[numberTask][0] = "In progress" if check_status == "1" else "Done" if check_status == "2" else "Not complete"
        else:
            write = input("Type here: ")
            todolist[numberTask][1] = write
            check_status = input("Is this task in progress(1), done(2) or not complete(3)? ")
            todolist[numberTask][0] = "In progress" if check_status == "1" else "Done" if check_status == "2" else "Not complete"
        save_tasks()
        print("Operation is done")
    else:
        print("You wrote wrong ID")
    print("-----")
        
def delete_task():
    print("-----")
    print(todolist)
    if not todolist:
        print("No tasks available to delete.")
        print("-----")
        return
        
    number = input("Choose your task by its ID: ")
    
    if checkID(number, todolist):
        todolist.pop(number)
        save_tasks()
        print("Operation is done")
    else:
        print("You wrote wrong ID")
    print("-----")
        
def see_all_tasks():
    print("-----")
    print(todolist)
    print("-----")

def see_current():
    print("-----")
    for key, value in todolist.items():
        if "in progress" in value[0].lower():
            print(key, value)
    print("-----")

def see_done():
    print("-----")
    for key, value in todolist.items():
        if "done" in value[0].lower():
            print(key, value)
    print("-----")

def see_notComplete():
    print("-----")
    for key, value in todolist.items():
        if "not complete" in value[0].lower():
            print(key, value)
    print("-----")

system = True
while system:
    taskOperation = input("Hi, what do you want to do? add(1), update(2), delete(3), see(4), lists of tasks(5) or stop(6): ")
    
    if taskOperation.lower() == "add" or taskOperation == "1":
        create_task()
    elif taskOperation.lower() == "update" or taskOperation == "2":
        update_task()
    elif taskOperation.lower() == "delete" or taskOperation == "3":
        delete_task()
    elif taskOperation.lower() == "see" or taskOperation == "4":
        see_all_tasks()
    elif taskOperation.lower() == "lists of tasks" or taskOperation == "5":
        listOperation = int(input("All list(1), in progress list(2), done list(3) or not complete list(4): "))
        if listOperation == 1:
            see_all_tasks()
        elif listOperation == 2:
            see_current()
        elif listOperation == 3:
            see_done()
        elif listOperation == 4:
            see_notComplete()
    elif taskOperation.lower() == "stop" or taskOperation == "6":
        system = False
    else:
        print("Invalid option, please try again.")
