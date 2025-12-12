import streamlit as st
import json
import os
from datetime import datetime
import hashlib

# Configuration
PROJECTS_FILE = "projects_data.json"
ATTACHMENTS_FOLDER = "project_attachments"
PASSWORD_HASH = hashlib.sha256("admin123".encode()).hexdigest()  # Default password: admin123
PROFILE_IMAGE = "profile.jpeg"  # Place your profile image in the same folder

# Create attachments folder if it doesn't exist
if not os.path.exists(ATTACHMENTS_FOLDER):
    os.makedirs(ATTACHMENTS_FOLDER)

# Initialize session state
if 'view_authenticated' not in st.session_state:
    st.session_state.view_authenticated = False
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_project' not in st.session_state:
    st.session_state.current_project = None
if 'edit_mode' not in st.session_state:
    st.session_state.edit_mode = False
if 'last_saved_state' not in st.session_state:
    st.session_state.last_saved_state = None

# Load projects from file
def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Save projects to file
def save_projects(projects):
    with open(PROJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(projects, indent=4, fp=f, ensure_ascii=False)

# Check if project has changes
def has_changes(current_data):
    if st.session_state.last_saved_state is None:
        return True
    return current_data != st.session_state.last_saved_state

# Generate unique project ID
def generate_project_id():
    return datetime.now().strftime("%Y%m%d%H%M%S")

# Sidebar Navigation
st.sidebar.title(" Project Manager")
menu = st.sidebar.radio("Navigation", ["Add Project", "View Projects", "About Me"])

# Main Application
if menu == "Add Project":
    # Add background image CSS for Add Project page
    if os.path.exists("image.png"):
        import base64
        with open("image.png", "rb") as img_file:
            img_data = base64.b64encode(img_file.read()).decode()
        
        st.markdown(f"""
        <style>
            .stApp {{
                background-image: url("data:image/png;base64,{img_data}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stForm {{
                background-color: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 10px;
            }}
            h1, h2, h3 {{
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }}
        </style>
        """, unsafe_allow_html=True)
    
    st.title(" Add New Project to kailash Database !!")
    
    with st.form("project_form", clear_on_submit=False):
        st.subheader("Project Details")
        
        title = st.text_input(" Project Title", placeholder="Enter project title...")
        writer = st.text_input(" Writer/Author", placeholder="Enter writer name...")
        
        st.markdown("###  Description")
        description = st.text_area(
            "Write your project description here...",
            height=400,
            placeholder="Start writing your project description here..."
        )
        
        st.markdown("### 📎 Attach Files (Optional)")
        uploaded_files = st.file_uploader(
            "Upload files (PDF, DOC, DOCX, TXT, Images)",
            type=["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Maximum file size: 200MB per file"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            submit = st.form_submit_button(" Save Project", use_container_width=True)
    
    if submit:
        if title and writer and description:
            projects = load_projects()
            project_id = generate_project_id()
            
            # Handle file uploads
            attached_files = []
            if uploaded_files:
                project_folder = os.path.join(ATTACHMENTS_FOLDER, project_id)
                os.makedirs(project_folder, exist_ok=True)
                
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(project_folder, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    attached_files.append({
                        "name": uploaded_file.name,
                        "size": uploaded_file.size,
                        "type": uploaded_file.type
                    })
            
            # Create project data
            project_data = {
                "id": project_id,
                "title": title,
                "writer": writer,
                "description": description,
                "attachments": attached_files,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Check if changes exist
            if has_changes(project_data):
                projects.append(project_data)
                save_projects(projects)
                st.session_state.last_saved_state = project_data.copy()
                st.success(" Project saved successfully!")
                if attached_files:
                    st.info(f"📎 {len(attached_files)} file(s) attached successfully!")
                st.balloons()
            else:
                st.info("ℹ No changes detected. Project already saved.")
        else:
            st.error(" Please fill in all fields before saving!")

elif menu == "View Projects":
    st.title(" View Projects")
    
    # Password protection for viewing projects
    if not st.session_state.view_authenticated:
        st.warning(" Password required to view projects")
        password = st.text_input("Enter password to view projects:", type="password", key="view_password")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Unlock", use_container_width=True):
                if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
                    st.session_state.view_authenticated = True
                    st.rerun()
                else:
                    st.error(" Incorrect password!")
        st.stop()
    
    projects = load_projects()
    
    if not projects:
        st.info("No projects found. Add a new project to get started!")
    else:
        # Lock button to logout
        if st.button(" Lock View", type="secondary"):
            st.session_state.view_authenticated = False
            st.session_state.authenticated = False
            st.session_state.edit_mode = False
            st.rerun()
        
        # Project selector
        project_titles = [f"{p['title']} (by {p['writer']})" for p in projects]
        selected_index = st.selectbox("Select a project to view:", range(len(projects)), 
                                      format_func=lambda x: project_titles[x])
        
        selected_project = projects[selected_index]
        
        st.divider()
        
        # Display/Edit mode toggle
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            if st.button(" Edit Project", use_container_width=True):
                # Password protection
                st.session_state.edit_mode = True
        with col2:
            if st.button(" Delete Project", use_container_width=True, type="secondary"):
                st.session_state.delete_confirm = True
        
        # Password protection for editing
        if st.session_state.edit_mode and not st.session_state.authenticated:
            st.warning(" Password required to edit projects")
            password = st.text_input("Enter password:", type="password", key="edit_password")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Unlock", use_container_width=True):
                    if hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
                        st.session_state.authenticated = True
                        st.rerun()
                    else:
                        st.error(" Incorrect password!")
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.edit_mode = False
                    st.rerun()
        
        # Delete confirmation
        if hasattr(st.session_state, 'delete_confirm') and st.session_state.delete_confirm:
            st.error(" Are you sure you want to delete this project?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Delete", type="primary", use_container_width=True):
                    # Delete project files if any
                    project_folder = os.path.join(ATTACHMENTS_FOLDER, selected_project['id'])
                    if os.path.exists(project_folder):
                        import shutil
                        shutil.rmtree(project_folder)
                    
                    projects.pop(selected_index)
                    save_projects(projects)
                    st.session_state.delete_confirm = False
                    st.success("Project deleted successfully!")
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.delete_confirm = False
                    st.rerun()
        
        # Edit mode (authenticated)
        if st.session_state.edit_mode and st.session_state.authenticated:
            st.subheader(" Edit Mode")
            
            with st.form("edit_form"):
                new_title = st.text_input(" Project Title", value=selected_project['title'])
                new_writer = st.text_input(" Writer/Author", value=selected_project['writer'])
                
                st.markdown("###  Description")
                new_description = st.text_area(
                    "Edit your project description...",
                    value=selected_project['description'],
                    height=400
                )
                
                st.markdown("### 📎 Add More Files (Optional)")
                new_uploaded_files = st.file_uploader(
                    "Upload additional files",
                    type=["pdf", "doc", "docx", "txt", "png", "jpg", "jpeg"],
                    accept_multiple_files=True,
                    key="edit_file_upload"
                )
                
                col1, col2 = st.columns([1, 5])
                with col1:
                    save_changes = st.form_submit_button("Save Changes", use_container_width=True)
                with col2:
                    cancel_edit = st.form_submit_button("Cancel", use_container_width=True)
            
            if save_changes:
                # Handle new file uploads
                existing_attachments = selected_project.get('attachments', [])
                if new_uploaded_files:
                    project_folder = os.path.join(ATTACHMENTS_FOLDER, selected_project['id'])
                    os.makedirs(project_folder, exist_ok=True)
                    
                    for uploaded_file in new_uploaded_files:
                        file_path = os.path.join(project_folder, uploaded_file.name)
                        with open(file_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        
                        existing_attachments.append({
                            "name": uploaded_file.name,
                            "size": uploaded_file.size,
                            "type": uploaded_file.type
                        })
                
                updated_project = {
                    "id": selected_project['id'],
                    "title": new_title,
                    "writer": new_writer,
                    "description": new_description,
                    "attachments": existing_attachments,
                    "created_at": selected_project['created_at'],
                    "last_modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Check if there are actual changes
                if (new_title != selected_project['title'] or 
                    new_writer != selected_project['writer'] or 
                    new_description != selected_project['description'] or
                    new_uploaded_files):
                    
                    projects[selected_index] = updated_project
                    save_projects(projects)
                    st.success(" Changes saved successfully!")
                    if new_uploaded_files:
                        st.info(f"📎 {len(new_uploaded_files)} new file(s) added!")
                    st.session_state.edit_mode = False
                    st.session_state.authenticated = False
                    st.rerun()
                else:
                    st.info(" No changes detected.")
            
            if cancel_edit:
                st.session_state.edit_mode = False
                st.session_state.authenticated = False
                st.rerun()
        
        # View mode (default)
        elif not st.session_state.edit_mode:
            st.subheader(" View Mode")
            st.markdown(f"** Title:** {selected_project['title']}")
            st.markdown(f"** Writer:** {selected_project['writer']}")
            st.markdown(f"** Created:** {selected_project['created_at']}")
            st.markdown(f"** Last Modified:** {selected_project['last_modified']}")
            
            st.divider()
            st.markdown("###  Description")
            st.text_area("Description Content", value=selected_project['description'], height=400, disabled=True, label_visibility="collapsed")
            
            # Display attachments if any
            if 'attachments' in selected_project and selected_project['attachments']:
                st.divider()
                st.markdown("### 📎 Attached Files")
                for attachment in selected_project['attachments']:
                    file_path = os.path.join(ATTACHMENTS_FOLDER, selected_project['id'], attachment['name'])
                    if os.path.exists(file_path):
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.markdown(f" **{attachment['name']}**")
                            st.caption(f"Size: {attachment['size'] / 1024:.2f} KB")
                        with col2:
                            with open(file_path, "rb") as file:
                                st.download_button(
                                    label="Download",
                                    data=file,
                                    file_name=attachment['name'],
                                    mime=attachment['type'],
                                    use_container_width=True
                                )
                    else:
                        st.warning(f"⚠️ File not found: {attachment['name']}")

elif menu == "About Me":
    st.title("👤 About Me")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if os.path.exists(PROFILE_IMAGE):
            st.image(PROFILE_IMAGE, width=200)
        else:
            st.info(" My profile picture as 'profile.jpg' in the project folder")
    
    with col2:
        st.markdown("""
        ### Kailash
        **Project Manager & Developer**
        
        Welcome to my Project Management System! This application helps you:
        
        -  Create and manage projects
        -  Edit project details easily
        -  Secure your projects with password protection
        -  Smart save feature (no duplicate saves)
        -  Delete projects when needed
        
        ---
        
        **Contact Information:**
        -  Email: electrokailash@gmail.com
        -  Website: https://electrokailash.streamlit.app/
        -  GitHub: https://github.com/electrokailash123chy
        
        ---
        Thank you for using my Project Management System! Feel free to reach out for any queries or feedback.
        """)
    
   
