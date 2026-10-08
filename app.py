import streamlit as st
import requests


# -----------------------------------
# Configuration
# -----------------------------------

API_URL = "http://127.0.0.1:8000/api/tasks/"


st.set_page_config(
    page_title="Student To-Do List",
    page_icon="📝",
    layout="centered"
)


# -----------------------------------
# Functions
# -----------------------------------

def get_tasks():
    response = requests.get(API_URL)

    if response.status_code == 200:
        return response.json()

    return []


def add_task(title):
    response = requests.post(
        API_URL,
        json={
            "title": title,
            "completed": False
        }
    )

    return response.status_code == 201


def update_task(task_id, data):
    response = requests.patch(
        f"{API_URL}{task_id}/",
        json=data
    )

    return response.status_code == 200


def delete_task(task_id):
    response = requests.delete(
        f"{API_URL}{task_id}/"
    )

    return response.status_code == 204


# -----------------------------------
# Title
# -----------------------------------

st.title("📝 Student To-Do List")

st.write("Manage your daily college tasks easily.")


# -----------------------------------
# Add Task
# -----------------------------------

st.subheader("➕ Add New Task")

col1, col2 = st.columns(2)


with col1:

    task_title = st.text_input(
        "Task",
        placeholder="Example: Complete DBMS assignment"
    )


with col2:

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )


due_date = st.date_input(
    "Due Date"
)


if st.button(
    "➕ Add Task",
    use_container_width=True
):

    if task_title.strip():

        response = requests.post(
            API_URL,
            json={
                "title": task_title.strip(),
                "priority": priority,
                "due_date": str(due_date),
                "completed": False
            }
        )

        if response.status_code == 201:

            st.success(
                "Task added successfully!"
            )

            st.rerun()

        else:

            st.error(
                "Unable to add task."
            )

    else:

        st.warning(
            "Please enter a task."
        )


# -----------------------------------
# Get Tasks
# -----------------------------------

tasks = get_tasks()


# -----------------------------------
# Statistics
# -----------------------------------

total_tasks = len(tasks)

completed_tasks = sum(
    task["completed"]
    for task in tasks
)

pending_tasks = total_tasks - completed_tasks


st.divider()

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "📋 Total",
        total_tasks
    )


with col2:
    st.metric(
        "✅ Completed",
        completed_tasks
    )


with col3:
    st.metric(
        "⏳ Pending",
        pending_tasks
    )
if total_tasks > 0:

    progress = completed_tasks / total_tasks

    st.progress(
        progress,
        text=f"{int(progress * 100)}% completed"
    )

else:

    st.progress(
        0,
        text="0% completed"
    )

# -----------------------------------
# Filter
# -----------------------------------

st.divider()

st.subheader("📋 My Tasks")


search = st.text_input(
    "🔍 Search Tasks",
    placeholder="Search by task name..."
)




filter_option = st.selectbox(
    "Filter Tasks",
    [
        "All",
        "Pending",
        "Completed"
    ]
)


if filter_option == "Pending":

    filtered_tasks = [
        task for task in tasks
        if not task["completed"]
    ]

elif filter_option == "Completed":

    filtered_tasks = [
        task for task in tasks
        if task["completed"]
    ]

else:

    filtered_tasks = tasks
    if search:

            filtered_tasks = [
                task
                for task in filtered_tasks
                if search.lower() in task["title"].lower()
            ]


# -----------------------------------
# Display Tasks
# -----------------------------------

if not filtered_tasks:

    st.info("No tasks found.")

else:

    for task in filtered_tasks:

        task_id = task["id"]

        completed = task["completed"]

        title = task["title"]

        priority = task["priority"]

        due_date = task["due_date"]


        # --------------------------------
        # Task container
        # --------------------------------

        with st.container(border=True):

            col1, col2, col3 = st.columns(
                [0.55, 0.25, 0.20]
            )


            # --------------------------------
            # Checkbox
            # --------------------------------

            with col1:

                new_status = st.checkbox(
                    title,
                    value=completed,
                    key=f"check_{task_id}"
                )

                st.write(f"**Priority:** {priority}")

                st.write(f"**Due Date:** {due_date}")


                if new_status != completed:

                    if update_task(
                        task_id,
                        {
                            "completed": new_status
                        }
                    ):

                        st.rerun()


            # --------------------------------
            # Edit
            # --------------------------------

            with col2:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{task_id}"
                ):

                    st.session_state[
                        f"editing_{task_id}"
                    ] = True


            # --------------------------------
            # Delete
            # --------------------------------

            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task_id}"
                ):

                    if delete_task(task_id):

                        st.success(
                            "Task deleted!"
                        )

                        st.rerun()


            # --------------------------------
            # Edit form
            # --------------------------------

            if st.session_state.get(
                f"editing_{task_id}",
                False
            ):

                new_title = st.text_input(
                    "Edit task",
                    value=title,
                    key=f"title_{task_id}"
                )


                col_save, col_cancel = st.columns(2)


                with col_save:

                    if st.button(
                        "💾 Save",
                        key=f"save_{task_id}"
                    ):

                        if new_title.strip():

                            if update_task(
                                task_id,
                                {
                                    "title": new_title.strip()
                                }
                            ):

                                st.session_state[
                                    f"editing_{task_id}"
                                ] = False

                                st.success(
                                    "Task updated!"
                                )

                                st.rerun()

                        else:

                            st.warning(
                                "Task cannot be empty."
                            )


                with col_cancel:

                    if st.button(
                        "Cancel",
                        key=f"cancel_{task_id}"
                    ):

                        st.session_state[
                            f"editing_{task_id}"
                        ] = False

                        st.rerun()