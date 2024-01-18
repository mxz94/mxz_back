import win32com.taskscheduler
import datetime

def create_task(task_name, task_description, trigger_time, program_path,
                working_directory):
    scheduler = win32com.taskscheduler.GetScheduler()
    task_definition = win32com.taskscheduler.Definition()

    task_definition.name = task_name
    task_definition.description = task_description

    # Set the task trigger to daily at the specified time
    trigger = win32com.taskscheduler.triggers.DailyTrigger()
    trigger.days_of_week = win32com.taskscheduler.days.MONDAY, win32com.taskscheduler.days.TUESDAY, win32com.taskscheduler.days.WEDNESDAY, win32com.taskscheduler.days.THURSDAY, win32com.taskscheduler.days.FRIDAY, win32com.taskscheduler.days.SATURDAY, win32com.taskscheduler.days.SUNDAY
    trigger.start_boundary = datetime.datetime.now().replace(hour=trigger_time, minute=0, second=0)
    trigger.enabled = True
    task_definition.triggers.add(trigger)

    # Set the task action to run the specified program
    action = win32com.taskscheduler.actions.ExecAction()
    action.path = program_path
    action.working_directory = working_directory
    task_definition.actions.add(action)

    # Register the task with the scheduler
    scheduler.RegisterTaskDefinition(task_name, task_definition)

if __name__ == "__main__":
    # Set the task parameters
    task_name = "My Daily Task"
    task_description = "This task runs every day at 7:00 PM."
    trigger_time = 19  # 7 PM in 24-hour format
    program_path = "C:\\path\\to\\my_program.exe"
    working_directory = "C:\\path\\to\\working_directory"

    # Create the task
    create_task(task_name, task_description, trigger_time, program_path,
                working_directory)

    print("Task created successfully!")