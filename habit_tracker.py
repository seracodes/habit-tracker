import json
import os
from datetime import datetime

DATA_FILE = "habits.json"


# ---------- STORAGE LAYER ----------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ Data file corrupted. Starting fresh.")
        return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ---------- UI DOODLES ----------

def doodle_success():
    print("""
  (＾◡＾)っ 🌱
  Habit planted!
""")


def doodle_complete():
    print("""
   \o/
    |
   / \   🌟
  Habit completed!
""")


def doodle_list():
    print("""
  📒 Your Habit Garden
  -------------------
""")


def doodle_error():
    print("""
  (╯︵╰,)
  Something went wrong.
""")


# ---------- HABIT ENGINE ----------

def add_habit(data, name):
    if name in data:
        print("⚠️ Habit already exists.")
        return

    data[name] = {
        "created": datetime.today().strftime("%Y-%m-%d"),
        "completed_dates": [],
        "streak": 0,
        "last_completed": None
    }
    save_data(data)
    doodle_success()


def complete_habit(data, name):
    if name not in data:
        print("❌ Habit not found.")
        return

    today = datetime.today().strftime("%Y-%m-%d")
    habit = data[name]

    if habit["last_completed"] == today:
        print("✅ Already completed today!")
        return

    # streak logic
    if habit["last_completed"]:
        last = datetime.strptime(habit["last_completed"], "%Y-%m-%d")
        diff = (datetime.today() - last).days
        if diff == 1:
            habit["streak"] += 1
        else:
            habit["streak"] = 1
    else:
        habit["streak"] = 1

    habit["last_completed"] = today
    habit["completed_dates"].append(today)
    save_data(data)
    doodle_complete()


def list_habits(data):
    if not data:
        print("🌱 No habits yet. Add one!")
        return

    doodle_list()
    for i, (habit, info) in enumerate(data.items(), 1):
        streak = info["streak"]
        last = info["last_completed"] or "Never"
        print(f"{i}. {habit}  | 🔥 Streak: {streak} | Last: {last}")


def delete_habit(data, name):
    if name not in data:
        print("❌ Habit not found.")
        return
    del data[name]
    save_data(data)
    print("🗑 Habit deleted.")


# ---------- COMMAND PARSER ----------

def show_help():
    print("""
📌 Habit Tracker Commands:

add <habit>        → Add a new habit
done <habit>       → Mark habit complete
list               → Show all habits
delete <habit>     → Delete a habit
help               → Show commands
exit               → Quit program
""")


def main():
    print("""
🌿 Welcome to Habit Garden 🌿
Type 'help' to see commands.
""")

    data = load_data()

    while True:
        try:
            command = input("🌱 > ").strip()
            if not command:
                continue

            parts = command.split(" ", 1)
            action = parts[0].lower()
            argument = parts[1] if len(parts) > 1 else None

            if action == "add" and argument:
                add_habit(data, argument)

            elif action == "done" and argument:
                complete_habit(data, argument)

            elif action == "list":
                list_habits(data)

            elif action == "delete" and argument:
                delete_habit(data, argument)

            elif action == "help":
                show_help()

            elif action == "exit":
                print("🌸 See you tomorrow!")
                break

            else:
                print("❓ Unknown command. Type 'help'.")

        except KeyboardInterrupt:
            print("\n👋 Exiting safely.")
            break

        except Exception:
            doodle_error()


if __name__ == "__main__":
    main()
