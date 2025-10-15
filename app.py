# ============================================================
# Streamlit CRUD App with SQLite
# Created by: MARTINEZ, GIELOME M. | 2023109014
# Theme: Pastel Blue
# ============================================================

import streamlit as st
import sqlite3
import pandas as pd
from create_db import create_table

# Ensure database and table exist
create_table()

# ---------------- DATABASE FUNCTIONS ---------------- #

def add_user(name, email, age):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(name, email, age) VALUES (?, ?, ?)', (name, email, age))
    conn.commit()
    conn.close()

def view_users():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    data = c.fetchall()
    conn.close()
    return data

def delete_user(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    conn.close()

# ---------------- STREAMLIT UI ---------------- #

st.set_page_config(
    page_title="User Management Web App 💙",
    page_icon="👤",
    layout="centered"
)

# For pastel blue - CSS
st.markdown(
    """
    <style>
    :root {
        --primary-color: #ADD8E6;
        --bg-color: #E6F7FF;
        --text-color: #333333;
        --accent-color: #87CEEB;
    }
    [data-testid="stAppViewContainer"] {
        background-color: var(--bg-color);
        color: var(--text-color);
        font-family: 'Trebuchet MS', sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #D0E8F5;
    }
    .stButton>button {
        background-color: var(--accent-color);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.6em 1.2em;
        font-weight: bold;
        transition: 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #AEC6CF;
        transform: scale(1.05);
    }
    h1, h2, h3, .stSubheader {
        color: #1E90FF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.title("👥 User Management System")
st.caption("Created by MARTINEZ, GIELOME M. | 2023109014")

menu = ["Add User 📝", "View Users 👤", "Delete User ❌"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------- UI SECTIONS ---------------- #

if choice == "Add User 📝":
    st.subheader("➕ Add New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", 0, 120)
    
    if st.button("Submit 💙"):
        if name and email:
            add_user(name, email, age)
            st.success(f"{name} added successfully! 🎉")
        else:
            st.warning("Please fill in all fields before submitting ⚠️")

elif choice == "View Users 👤":
    st.subheader("👤 View All Users")
    users = view_users()
    if users:
        df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Age"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No users found in the database 💭")

elif choice == "Delete User ❌":
    st.subheader("❌ Delete a User")
    users = view_users()
    if users:
        df = pd.DataFrame(users, columns=["ID", "Name", "Email", "Age"])
        st.dataframe(df, use_container_width=True)

        user_id = st.number_input("Enter ID to delete", min_value=1, step=1)
        if st.button("Delete 💔"):
            delete_user(user_id)
            st.warning(f"User {user_id} deleted 💨")
    else:
        st.info("No users available to delete 💬")
