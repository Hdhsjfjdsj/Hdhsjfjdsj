import heapq
import json
from datetime import datetime, timedelta

class StudyPlanner:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, name, hours_needed, difficulty, deadline):
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
        heapq.heappush(self.tasks, (deadline_date, difficulty, name, hours_needed))
    
    def generate_schedule(self, available_hours_per_day):
        schedule = []
        current_day = datetime.now()
        available_hours = available_hours_per_day
        
        while self.tasks:
            task = heapq.heappop(self.tasks)
            deadline, difficulty, name, hours_needed = task
            
            # If there's not enough time in the day, move to the next day
            while hours_needed > available_hours:
                schedule.append((current_day.date(), name, available_hours))
                hours_needed -= available_hours
                available_hours = available_hours_per_day
                current_day += timedelta(days=1)
            
            schedule.append((current_day.date(), name, hours_needed))
            available_hours -= hours_needed

        return schedule
    
    def save_tasks(self, filename="tasks.json"):
        with open(filename, "w") as file:
            json.dump(self.tasks, file, default=str)
    
    def load_tasks(self, filename="tasks.json"):
        with open(filename, "r") as file:
            self.tasks = json.load(file)

# CLI Interface
def text_based_interface():
    planner = StudyPlanner()
    while True:
        print("\n1. Add a task")
        print("2. Generate schedule")
        print("3. Save tasks")
        print("4. Load tasks")
        print("5. Quit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            name = input("Task name: ")
            hours_needed = int(input("Hours needed: "))
            difficulty = int(input("Difficulty (1-10): "))
            deadline = input("Deadline (YYYY-MM-DD): ")
            planner.add_task(name, hours_needed, difficulty, deadline)
        
        elif choice == '2':
            available_hours_per_day = int(input("Available hours per day: "))
            schedule = planner.generate_schedule(available_hours_per_day)
            print("\nGenerated Schedule:")
            for day, task, hours in schedule:
                print(f"{day}: Work on {task} for {hours} hour(s)")
        
        elif choice == '3':
            planner.save_tasks()
            print("Tasks saved.")
        
        elif choice == '4':
            planner.load_tasks()
            print("Tasks loaded.")
        
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Run the text-based version
if __name__ == "__main__":
    text_based_interface()
