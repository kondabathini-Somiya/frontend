# app.py

import gradio as gr
import requests

BASE_URL = "https://flaskuser-1q4s.onrender.com"

# --- Backend interaction functions ---

def fetch_data():
    res = requests.get(f"{BASE_URL}/get_data")
    return res.json() if res.status_code == 200 else []

def add_user(name, email):
    res = requests.post(f"{BASE_URL}/add_data", json={"name": name, "email": email})
    return "✅ User added successfully!" if res.ok else "❌ Failed to add user."

def update_user(user_id, name, email):
    res = requests.put(f"{BASE_URL}/update_data/{user_id}", json={"name": name, "email": email})
    return "✅ User updated!" if res.ok else "❌ Update failed."

def delete_user(user_id):
    res = requests.delete(f"{BASE_URL}/delete_data/{user_id}")
    return "✅ User deleted!" if res.ok else "❌ Delete failed."


# --- Gradio UI functions ---

def add_user_interface(name, email):
    return add_user(name, email)

def list_users_interface():
    data = fetch_data()
    if not data:
        return "No users found."

    output = ""
    for user in data:
        output += f"### ID: {user['id']}\n"
        output += f"- Name: {user['name']}\n"
        output += f"- Email: {user['email']}\n"
        output += f"---\n"
    return output


def update_user_interface(user_id, name, email):
    return update_user(user_id, name, email)

def delete_user_interface(user_id):
    return delete_user(user_id)


# --- Gradio Blocks layout ---

with gr.Blocks() as demo:
    gr.Markdown("## 📋 User Management Dashboard")

    with gr.Tab("View Users"):
        view_output = gr.Markdown()
        refresh_btn = gr.Button("🔄 Refresh List")
        refresh_btn.click(fn=list_users_interface, outputs=view_output)

    with gr.Tab("Add User"):
        name_input = gr.Textbox(label="Name")
        email_input = gr.Textbox(label="Email")
        add_btn = gr.Button("➕ Add User")
        add_output = gr.Textbox(label="Status", interactive=False)
        add_btn.click(fn=add_user_interface, inputs=[name_input, email_input], outputs=add_output)

    with gr.Tab("Update User"):
        uid_input = gr.Number(label="User ID")
        name_update = gr.Textbox(label="New Name")
        email_update = gr.Textbox(label="New Email")
        update_btn = gr.Button("✏️ Update User")
        update_output = gr.Textbox(label="Status", interactive=False)
        update_btn.click(fn=update_user_interface, inputs=[uid_input, name_update, email_update], outputs=update_output)

    with gr.Tab("Delete User"):
        del_id_input = gr.Number(label="User ID")
        delete_btn = gr.Button("🗑️ Delete User")
        delete_output = gr.Textbox(label="Status", interactive=False)
        delete_btn.click(fn=delete_user_interface, inputs=del_id_input, outputs=delete_output)


demo.launch()
