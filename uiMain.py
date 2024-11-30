import os
import streamlit as st
import datetime

# File to store tasks
filename = "list.txt"

# Global list to store tasks
currTask = []

# Priority levels
priorityList = ["high", "medium", "low"]

# Variable to track last updated task
lastTaskUpdated = None  # Can be None when no task is marked as done

# Function to load tasks from the .txt file
def loadTasks():
    global currTask
    if os.path.exists(filename):  
        with open(filename, "r") as file:
            lines = file.readlines()
            currTask = []
            for line in lines:
                task = line.strip().split(" | ")  # Split by delimiter
                if task[0] == "O":
                    task[0] = ""  # Represent uncompleted tasks as empty string
                currTask.append(task)

# Function to save tasks to the .txt file
def saveTasks():
    with open(filename, "w") as file:
        for task in currTask:
            if task[0] == "":  # If task is not completed, mark it as "O"
                task[0] = "O"
            file.write(" | ".join(task) + "\n")  

# Function to display the current tasks
def display_tasks(array):
    for index, task in enumerate(array, start=1):
        status, description, priority, due_date = task
        st.write(f"{index}. [{status}] {description} (Priority: {priority}, Due: {due_date})")

# Function to add a new task
def add_task():
    itemName = st.text_input("Task Name", key="task_name")
    itemPriority = st.selectbox("Priority", ["High", "Medium", "Low"], key="task_priority")
    itemCompletionDate = st.date_input("Due Date", key="task_due_date", min_value=datetime.date.today())
    
    if st.button("Add Task"):
        new_task = ["", itemName, itemPriority.capitalize(), itemCompletionDate.strftime('%m-%d-%Y')]
        currTask.append(new_task)  # Add new task to the list
        saveTasks()  # Save to file
        st.success(f"Task '{itemName}' added!")


# Function to mark a task as done
def mark_task():
    index = st.slider("Enter task index to mark as done", min_value=1, max_value=len(currTask), step=1, key="mark_index")
    if st.button("Mark Task as Done"):
        if currTask[index - 1][0] == "X":
            st.warning("This task is already marked as done!")
        else:
            currTask[index - 1][0] = "X"  # Mark task as done
            saveTasks()  # Save updated list
            st.success(f"Task '{currTask[index - 1][1]}' marked as done!")


# Function to unmark a task
def unmark_task():
    index = st.slider("Enter task index to mark as done", min_value=1, max_value=len(currTask), step=1, key="mark_index")
    if st.button("Undo Completed Task"):
        if currTask[index - 1][0] == "":
            st.warning("This task is already unmarked!")
        else:
            currTask[index - 1][0] = ""  
            saveTasks()  
            st.success(f"Task '{currTask[index - 1][1]}' has been umarked!")

# Function to remove a task
def remove_task():
    index = st.slider("Enter task index to mark as done", min_value=1, max_value=len(currTask), step=1, key="mark_index")    
    if st.button("Remove Task"):
        currTask.pop(index - 1)  
        saveTasks()
        st.success(f"Task at index {index} removed!")
    loadTasks()

# Function to sort tasks by priority
def sort_tasks():
    sorted_tasks = sorted(currTask, key=lambda x: ["High", "Medium", "Low"].index(x[2]))
    st.write("Sorted Tasks:")
    display_tasks(sorted_tasks)

# Streamlit app UI
st.title("To-Do List App")
st.header("Manage your tasks effectively!")

# Load tasks at the beginning
loadTasks()

# Sidebar menu for actions
user_action = st.sidebar.selectbox("Choose an action", ["Add Task", "Mark Task As Done", "Undo Completed Task", "Remove Task", "Sort Tasks"])

# Execute corresponding action based on user selection
if user_action == "Add Task":
    add_task()
elif user_action == "Mark Task As Done":
    mark_task()
elif user_action == "Undo Completed Task":
    unmark_task()
elif user_action == "Remove Task":
    remove_task()
elif user_action == "Sort Tasks":
    sort_tasks()

# Display the current list of tasks
st.write("### Current Tasks")
display_tasks(currTask)

# Save the tasks at the end (if needed)
saveTasks()