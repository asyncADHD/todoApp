from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Define the filename for storing tasks
JSON_FILE = 'tasks.json'

# Function to load tasks from the file
def load_tasks():
    try:
        with open(JSON_FILE, 'r') as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = {'active_tasks': [], 'completed_tasks': []}
    return tasks['active_tasks'], tasks['completed_tasks']



# Save tasks to JSON file
def save_tasks(active_tasks, completed_tasks):
    tasks = {'active_tasks': active_tasks, 'completed_tasks': completed_tasks}
    with open(JSON_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def add_todo():
    active_tasks, completed_tasks = load_tasks()
    return render_template('todo.html', active_tasks=active_tasks, completed_tasks=completed_tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    task_data = request.json
    if task_data and 'task' in task_data:
        task_text = task_data['task']
        active_tasks, completed_tasks = load_tasks()  # Load both active and completed tasks
        active_tasks.append(task_text)  # Add the new task to active tasks
        save_tasks(active_tasks, completed_tasks)  # Save the updated tasks
        return jsonify({'success': True, 'message': 'Task added successfully'})
    else:
        return jsonify({'success': False, 'message': 'Invalid task data'})


@app.route('/complete_task', methods=['POST'])
def complete_task():
    task_data = request.json
    if task_data and 'index' in task_data:
        try:
            task_index = int(task_data['index'])
            active_tasks, completed_tasks = load_tasks()
            if 0 <= task_index < len(active_tasks):
                completed_task = active_tasks.pop(task_index)
                completed_tasks.append(completed_task)
                save_tasks(active_tasks, completed_tasks)  # Save the updated tasks
                return jsonify({'success': True, 'message': 'Task completed successfully'})
            else:
                return jsonify({'success': False, 'message': 'Invalid task index'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})  # Return error message
    else:
        return jsonify({'success': False, 'message': 'Invalid JSON data'})


@app.route('/delete_task', methods=['POST'])
def delete_task():
    task_data = request.json
    if task_data and 'index' in task_data:
        try:
            task_index = int(task_data['index'])
            active_tasks, completed_tasks = load_tasks()

            # Check if the index corresponds to an active task
            if 0 <= task_index < len(active_tasks):
                del active_tasks[task_index]
            # Check if the index corresponds to a completed task
            elif 0 <= task_index < len(completed_tasks):
                del completed_tasks[task_index]
            else:
                return jsonify({'success': False, 'message': 'Invalid task index'})

            # Save the updated tasks
            save_tasks(active_tasks, completed_tasks)

            return jsonify({'success': True, 'message': 'Task deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})  # Return error message
    else:
        return jsonify({'success': False, 'message': 'Invalid JSON data'})


@app.route('/update_tasks', methods=['POST'])
def update_tasks():
    # Handle the logic to update tasks data here
    return jsonify({'success': True, 'message': 'Tasks updated successfully'})

@app.route('/uncomplete_task', methods=['POST'])
def uncomplete_task():
    task_data = request.json
    if task_data and 'index' in task_data:
        task_index = int(task_data['index'])
        active_tasks, completed_tasks = load_tasks()
        if 0 <= task_index < len(completed_tasks):
            uncompleted_task = completed_tasks.pop(task_index)
            active_tasks.append(uncompleted_task)
            save_tasks(active_tasks, completed_tasks)
            return jsonify({'success': True, 'message': 'Task uncompleted successfully'})
    return jsonify({'success': False, 'message': 'Invalid task index'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)