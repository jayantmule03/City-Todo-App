from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://mongodb:27017/todo_database"
)

client = MongoClient(MONGO_URI)
db = client["todo_database"]
tasks_collection = db["tasks"]

# Home route - Display all tasks
@app.route('/')
def index():
    try:
        tasks = list(tasks_collection.find())
        return render_template('index.html', tasks=tasks)
    except Exception as e:
        print(f"Error in index: {e}")
        return f"Error loading tasks: {str(e)}", 500

# Create a new task
@app.route('/create', methods=['POST'])
def create_task():
    try:
        task_title = request.form.get('title')
        task_description = request.form.get('description', '')
        custom_city = request.form.get('customCity', '')
        
        # If "Other" is selected and customCity is provided, use custom city
        if task_description == 'Other' and custom_city:
            task_description = custom_city.strip()
        
        if task_title:
            new_task = {
                'title': task_title,
                'description': task_description,
                'completed': False,
                'created_at': datetime.now()
            }
            tasks_collection.insert_one(new_task)
        
        return redirect(url_for('index'))
    except Exception as e:
        print(f"Error creating task: {e}")
        return f"Error creating task: {str(e)}", 500

# Read/Get a single task (API endpoint)
@app.route('/task/<task_id>')
def get_task(task_id):
    try:
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        if task:
            task['_id'] = str(task['_id'])
            return jsonify(task)
        return jsonify({'error': 'Task not found'}), 404
    except InvalidId:
        return jsonify({'error': 'Invalid task ID'}), 400
    except Exception as e:
        print(f"Error getting task: {e}")
        return jsonify({'error': str(e)}), 500

# Update a task
@app.route('/update/<task_id>', methods=['POST'])
def update_task(task_id):
    try:
        task_title = request.form.get('title')
        task_description = request.form.get('description', '')
        custom_city = request.form.get('customCity', '')
        completed = request.form.get('completed') == 'on'
        
        # If "Other" is selected and customCity is provided, use custom city
        if task_description == 'Other' and custom_city:
            task_description = custom_city.strip()
        
        # Convert task_id to ObjectId
        result = tasks_collection.update_one(
            {'_id': ObjectId(task_id)},
            {'$set': {
                'title': task_title,
                'description': task_description,
                'completed': completed
            }}
        )
        
        if result.matched_count == 0:
            print(f"No task found with ID: {task_id}")
        
        return redirect(url_for('index'))
    except InvalidId:
        print(f"Invalid ObjectId: {task_id}")
        return "Invalid task ID", 400
    except Exception as e:
        print(f"Error updating task: {e}")
        return f"Error updating task: {str(e)}", 500

# Toggle task completion status
@app.route('/toggle/<task_id>')
def toggle_task(task_id):
    try:
        task = tasks_collection.find_one({'_id': ObjectId(task_id)})
        if task:
            tasks_collection.update_one(
                {'_id': ObjectId(task_id)},
                {'$set': {'completed': not task.get('completed', False)}}
            )
        else:
            print(f"Task not found: {task_id}")
        
        return redirect(url_for('index'))
    except InvalidId:
        print(f"Invalid ObjectId: {task_id}")
        return "Invalid task ID", 400
    except Exception as e:
        print(f"Error toggling task: {e}")
        return f"Error toggling task: {str(e)}", 500

# Delete a task
@app.route('/delete/<task_id>')
def delete_task(task_id):
    try:
        result = tasks_collection.delete_one({'_id': ObjectId(task_id)})
        
        if result.deleted_count == 0:
            print(f"No task found to delete with ID: {task_id}")
        
        return redirect(url_for('index'))
    except InvalidId:
        print(f"Invalid ObjectId: {task_id}")
        return "Invalid task ID", 400
    except Exception as e:
        print(f"Error deleting task: {e}")
        return f"Error deleting task: {str(e)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)