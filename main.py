"""
Course Number: ENGR 13300
Semester: Fall 2025

Description:
    Separate module for authentication and validation functions

Assignment Information:
    Assignment:     18.3 Individual Project
    Team ID:        LC2 - 18
    Author:         Elliott Sato, satoe@purdue.edu
    Date:           12/11/2025

Contributors:
    Copilot for new concepts

    My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor here as well.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

# Import Statements
import tkinter as tk  # GUI (New Concept?)
from tkinter import messagebox, ttk  # popups and widgets
import pandas as pd  # reading/writing Excel files
import openpyxl  # For appending to Excel
from datetime import datetime  # timestamp generation
import os  # For file existence checking
import auth_module  # UDF for authentication

# global variables
DATABASE_FILE = "keycard_database.xlsx"  # Excel file for data storage
current_user = None  # Stores currently logged-in user data


def initialize_database(): # Create Excel database if it doesn't exist
    # Check if database file already exists
    if not os.path.exists(DATABASE_FILE): 
        # Dictionary of lists for sample data
        data = {
            'Keycard_ID': ['DOC001', 'NUR042', 'ADM100', 'DOC002'],  # List of IDs
            'Name': ['Dr. Smith', 'Jane Doe', 'Admin User', 'Dr. Johnson'],  # List of names
            'Role': ['Doctor', 'Nurse', 'Admin', 'Doctor'],  # List of roles
            'Tool1': ['Scalpel', 'Thermometer', 'Master_Key', 'Ultrasound'],  # List of tools
            'Tool2': ['X-Ray', 'BP_Monitor', 'Database_Access', 'Stethoscope'],  # List of tools
            'Tool3': ['ECG', 'Stethoscope', 'User_Management', 'ECG'],  # List of tools
            'Layout': ['Advanced', 'Standard', 'Admin', 'Advanced'],  # List of layouts
            'Last_Login': ['Never', 'Never', 'Never', 'Never']  # List of timestamps
        }
        df = pd.DataFrame(data)  # Create DataFrame from dictionary
        df.to_excel(DATABASE_FILE, index=False)  # Write to Excel file
        print(f"Database created: {DATABASE_FILE}")  # Write to terminal
        # ERROR CHECK: Verify file was created successfully
        if not os.path.exists(DATABASE_FILE):  # Check if file exists after creation
            # Error Message
            messagebox.showerror("Database Error", "Failed to create database file!")
            return False  # Return failure status but don't exit
        else:  # File created successfully
            return True  # Return success status
    else:
        print(f"Database found: {DATABASE_FILE}")  # Write to terminal
        return True  # Database already exists

def save_new_user(keycard_id, name, role, tool1, tool2, tool3, layout): #writes data to excel (input: data from form)
    workbook = openpyxl.load_workbook(DATABASE_FILE)  # Load existing workbook
    sheet = workbook.active  # Get active worksheet
    new_row = [keycard_id, name, role, tool1, tool2, tool3, layout, 'Never']  # LIST
    sheet.append(new_row)  # Append new row to Excel sheet
    workbook.save(DATABASE_FILE)  # Save workbook back to file
    workbook.close()  # Close file handle
    return True  # Return success

def update_last_login(keycard_id): # Updates Excel data
    df = pd.read_excel(DATABASE_FILE)  # Read Excel database═
    for index, row in df.iterrows():  # Iterate through rows
        if row['Keycard_ID'] == keycard_id: # searched for users
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get timestamp
            df.at[index, 'Last_Login'] = current_time  # Update timestamp
            break  # Exit loop once found
    df.to_excel(DATABASE_FILE, index=False)  # Save updated DataFrame

def display_dashboard(user_data): # Displays dashboard based on user data
    global current_user  # Access global variable
    current_user = user_data  # Store current user data
    dashboard = tk.Toplevel(root)  # Create new GUI window (new concept)
    dashboard.title(f"Dashboard - {user_data['Name']}")  # Set window title
    dashboard.geometry("600x500")  # Set window size
    dashboard.configure(bg='#2C3E50')  # Set background color
    header_frame = tk.Frame(dashboard, bg='#34495E', pady=20)  # Create header frame
    header_frame.pack(fill='x')  # Pack into window
    # Display welcome message with user's name
    tk.Label(header_frame, text=f"Welcome, {user_data['Name']}", 
             font=('Arial', 18, 'bold'), bg='#34495E', fg='white').pack()
    # Display user role and keycard ID
    tk.Label(header_frame, text=f"Role: {user_data['Role']} | Keycard: {user_data['Keycard_ID']}", 
             font=('Arial', 11), bg='#34495E', fg='#BDC3C7').pack()
    # Display last login time
    tk.Label(header_frame, text=f"Last Login: {user_data['Last_Login']}", 
             font=('Arial', 9), bg='#34495E', fg='#95A5A6').pack()
    # Customize dashboard colors based on user role (diff colors for each type of role)
    if user_data['Role'] == 'Doctor':  # Check if Doctor
        bg_color = '#3498DB'  # Blue for doctors
        tool_color = '#2980B9'  # Darker blue for tools
    elif user_data['Role'] == 'Nurse':  # Check if Nurse
        bg_color = '#2ECC71'  # Green for nurses
        tool_color = '#27AE60'  # Darker green for tools
    elif user_data['Role'] == 'Admin':  # Check if Admin
        bg_color = '#E74C3C'  # Red for admin
        tool_color = '#C0392B'  # Darker red for tools
    else:  # Default for any other role
        bg_color = '#95A5A6'  # Gray for others
        tool_color = '#7F8C8D'  # Darker gray for tools
    tools_frame = tk.Frame(dashboard, bg='#2C3E50', pady=20)  # Create tools frame
    tools_frame.pack(fill='both', expand=True)  # Pack frame
    # Display section header
    tk.Label(tools_frame, text="Your Configured Tools:", 
             font=('Arial', 14, 'bold'), bg='#2C3E50', fg='white').pack(pady=10)
    # Create list of user's configured tools
    tools = [user_data['Tool1'], user_data['Tool2'], user_data['Tool3']]

    # Dictionary mapping tools to emoji icons
    tool_icons = {
        'Scalpel': '🔪', 'X-Ray': '🩻', 'ECG': '📈', 'Ultrasound': '🔊',
        'Thermometer': '🌡️', 'BP_Monitor': '💉', 'Stethoscope': '🩺',
        'Master_Key': '🔑', 'Database_Access': '💾', 'User_Management': '👥',
        'Microscope': '🔬', 'Calculator': '🧮', 'Ruler': '📏'
    }
    # Display all user tools as interactive buttons
    for i, tool in enumerate(tools, 1):  # Iterate with index
        # Get icon for tool, use default if not found
        icon = tool_icons.get(tool, '🔧')  # Default to wrench icon
        # Create clickable tool button with icon
        tool_btn = tk.Button(tools_frame, text=f"{icon} {i}. {tool}", 
                            font=('Arial', 12), bg=tool_color, fg='white',
                            width=30, height=2, relief='raised', bd=3,
                            command=lambda t=tool, ic=icon: use_tool(t, ic))  # Lambda with icon
        tool_btn.pack(pady=5)  # Add button to window
    layout_frame = tk.Frame(dashboard, bg='#34495E', pady=15)  # Create layout frame
    layout_frame.pack(fill='x')  # Pack frame
    # how user's layout preference
    tk.Label(layout_frame, text=f"Layout: {user_data['Layout']} Mode", 
             font=('Arial', 11), bg='#34495E', fg='white').pack()
    # Create logout button
    tk.Button(dashboard, text="Logout", font=('Arial', 12), 
              bg='#E74C3C', fg='white', command=dashboard.destroy).pack(pady=10)

def use_tool(tool_name, icon='🔧'): # Simulates tool usage with visual window
    current_time = datetime.now().strftime('%H:%M:%S')  # Get current time
    
    # Create new window for tool activation
    tool_window = tk.Toplevel(root)  # Create popup window
    tool_window.title(f"Tool Active: {tool_name}")  # Set window title
    tool_window.geometry("500x400")  # Set window size
    tool_window.configure(bg='#2C3E50')  # Set background color
    
    # Create main frame with border effect
    main_frame = tk.Frame(tool_window, bg='#34495E', padx=30, pady=30)
    main_frame.pack(fill='both', expand=True, padx=20, pady=20)
    
    # Display large tool icon
    tk.Label(main_frame, text=icon, font=('Arial', 80), 
             bg='#34495E', fg='white').pack(pady=20)
    
    # Display tool name
    tk.Label(main_frame, text=tool_name, font=('Arial', 24, 'bold'), 
             bg='#34495E', fg='#3498DB').pack(pady=10)
    
    # Display status message
    tk.Label(main_frame, text="✅ TOOL ACTIVE", font=('Arial', 16, 'bold'), 
             bg='#34495E', fg='#2ECC71').pack(pady=10)
    
    # Create info frame
    info_frame = tk.Frame(main_frame, bg='#2C3E50', padx=20, pady=15)
    info_frame.pack(pady=20, fill='x')
    
    # Display user information
    tk.Label(info_frame, text=f"User: {current_user['Name']}", 
             font=('Arial', 12), bg='#2C3E50', fg='white').pack(pady=5)
    
    tk.Label(info_frame, text=f"Role: {current_user['Role']}", 
             font=('Arial', 12), bg='#2C3E50', fg='white').pack(pady=5)
    
    tk.Label(info_frame, text=f"Keycard: {current_user['Keycard_ID']}", 
             font=('Arial', 12), bg='#2C3E50', fg='white').pack(pady=5)
    
    tk.Label(info_frame, text=f"Time: {current_time}", 
             font=('Arial', 12), bg='#2C3E50', fg='#95A5A6').pack(pady=5)
    
    # Create close button
    tk.Button(main_frame, text="Close", font=('Arial', 12, 'bold'), 
              bg='#E74C3C', fg='white', command=tool_window.destroy,
              width=15, height=2).pack(pady=15)


def login_window(): #Create login interface for existing users.
    login = tk.Toplevel(root)  # Create login window (new concept)
    login.title("Keycard Login")  # Set window title
    login.geometry("400x250")  # Set window size
    login.configure(bg='#34495E')  # Set background color
    # Display login header
    tk.Label(login, text="Keycard Access Login", font=('Arial', 16, 'bold'), 
             bg='#34495E', fg='white').pack(pady=20)
    # Display input prompt
    tk.Label(login, text="Enter Keycard ID:", font=('Arial', 11), 
             bg='#34495E', fg='white').pack()
    keycard_entry = tk.Entry(login, font=('Arial', 12), width=20)  # Create entry field
    keycard_entry.pack(pady=10)  # Pack entry field
    
    def attempt_login(): #Validate and authenticate user 
        keycard_id = keycard_entry.get().strip().upper()  # Get keycard ID
        # ERROR CHECK: Validate keycard format using separate module
        is_valid, error_msg = auth_module.validate_keycard_format(keycard_id)  # UDF
        if not is_valid:  # Check if validation failed
            # Display error message (does not exit program)
            messagebox.showerror("Invalid Format", error_msg)
            keycard_entry.delete(0, tk.END)  # Clear entry field for retry
            return  # Return to allow user to try again (wo exiting)
        user_data = auth_module.authenticate_user(keycard_id, DATABASE_FILE)  # Authenticate
        if user_data:  # User found
            update_last_login(keycard_id)  # Update timestamp
            login.destroy()  # Close login window
            display_dashboard(user_data)  # Show dashboard
        else:  # User not found
            # Display error (does NOT exit program)
            messagebox.showerror("Access Denied", 
                               "Keycard ID not found.\nPlease check your ID or register.")
            keycard_entry.delete(0, tk.END)  # Clear for retry (no exit)
    # Create login button
    tk.Button(login, text="Login", font=('Arial', 12), bg='#3498DB', 
              fg='white', command=attempt_login, width=15).pack(pady=10)
    # Create cancel button
    tk.Button(login, text="Cancel", font=('Arial', 12), bg='#95A5A6', 
              fg='white', command=login.destroy, width=15).pack()

def registration_window(): #Create registration interface for new users.
    register = tk.Toplevel(root)  # Create registration window
    register.title("New User Registration")  # Set title
    register.geometry("450x550")  # Set size
    register.configure(bg='#34495E')  # Set color
    # Display registration header
    tk.Label(register, text="Register New Keycard", font=('Arial', 16, 'bold'), 
             bg='#34495E', fg='white').pack(pady=20)
    fields = {}  # Dictionary to store input fields
    field_names = ['Keycard ID', 'Full Name', 'Tool 1', 'Tool 2', 'Tool 3']  # list
    # inputfield for each entry
    for field in field_names:  # Iterate through field names
        tk.Label(register, text=f"{field}:", font=('Arial', 10), 
                bg='#34495E', fg='white').pack()  # Create label
        entry = tk.Entry(register, font=('Arial', 11), width=30)  # Create entry
        entry.pack(pady=5)  # Pack entry
        fields[field] = entry  # Store in dictionary
    # Create role selection label
    tk.Label(register, text="Role:", font=('Arial', 10), 
            bg='#34495E', fg='white').pack()
    role_var = tk.StringVar(value="Doctor")  # Default value
    role_dropdown = ttk.Combobox(register, textvariable=role_var, 
                                 values=['Doctor', 'Nurse', 'Admin', 'Technician'],
                                 state='readonly', font=('Arial', 11), width=28)  # INPUT 
    role_dropdown.pack(pady=5)  # Pack dropdown
    # Create layout preference label
    tk.Label(register, text="Layout Preference:", font=('Arial', 10), 
            bg='#34495E', fg='white').pack()
    layout_var = tk.StringVar(value="Standard")  # Default value
    layout_dropdown = ttk.Combobox(register, textvariable=layout_var, 
                                   values=['Standard', 'Advanced', 'Custom'],
                                   state='readonly', font=('Arial', 11), width=28)  # INPUT
    layout_dropdown.pack(pady=5)  # Pack dropdown
   
    # Validate and process registration data
    def submit_registration():
        keycard_id = fields['Keycard ID'].get().strip().upper()  # Get keycard
        name = fields['Full Name'].get().strip()  # Get name
        tool1 = fields['Tool 1'].get().strip()  # Get tool 1
        tool2 = fields['Tool 2'].get().strip()  # Get tool 2
        tool3 = fields['Tool 3'].get().strip()  # Get tool 3
        role = role_var.get()  # Get role
        layout = layout_var.get()  # Get layout
        # Validate all fields filled (wo exiting)
        if not all([keycard_id, name, tool1, tool2, tool3]):  # NESTED IF
            # Display error (does NOT exit program)
            messagebox.showerror("Incomplete Form", "Please fill in all required fields.")
            return  # Return for completion
        # Validate keycard format
        # ERROR CHECK: Using function from separate file
        is_valid, error_msg = auth_module.validate_keycard_format(keycard_id)  # UDF from separate file
        if not is_valid: 
            # Display error
            messagebox.showerror("Invalid Keycard", error_msg)
            return  # Return to allow retry
        # Check for duplicate keycard
        if auth_module.keycard_exists(keycard_id, DATABASE_FILE): 
            # Display error 
            messagebox.showerror("Duplicate Keycard", 
                               "This Keycard ID already exists.\nPlease choose a different ID.")
            return  # Return to allow retry
        # Writes to Excel file
        if save_new_user(keycard_id, name, role, tool1, tool2, tool3, layout):  
            # Display success message
            messagebox.showinfo("Success", 
                              f"Registration successful!\n\nName: {name}\n"
                              f"Keycard ID: {keycard_id}\nRole: {role}\n\n"
                              f"You can now login with your keycard.")
            register.destroy()  # Close window
    # Create register button
    tk.Button(register, text="Register", font=('Arial', 12), bg='#2ECC71', 
              fg='white', command=submit_registration, width=15).pack(pady=15)
    # Create cancel button
    tk.Button(register, text="Cancel", font=('Arial', 12), bg='#95A5A6', 
              fg='white', command=register.destroy, width=15).pack()

# Show complete list of registered users
def view_all_users():
    """Display all registered users."""
    df = pd.read_excel(DATABASE_FILE)  # Read Excel database
    users_window = tk.Toplevel(root)  # Create window 
    users_window.title("All Registered Users")  # Set title
    users_window.geometry("700x400")  # Set size
    users_window.configure(bg='#2C3E50')  # Set color
    # Display header
    tk.Label(users_window, text="Registered Users Database", 
            font=('Arial', 14, 'bold'), bg='#2C3E50', fg='white').pack(pady=10)
    text_frame = tk.Frame(users_window)  # Create frame for text
    text_frame.pack(fill='both', expand=True, padx=10, pady=10)  # Pack frame
    scrollbar = tk.Scrollbar(text_frame)  # Create scrollbar
    scrollbar.pack(side='right', fill='y')  # Pack scrollbar
    text_widget = tk.Text(text_frame, font=('Courier', 10), 
                         yscrollcommand=scrollbar.set, bg='white')  # Create text widget
    text_widget.pack(side='left', fill='both', expand=True)  # Pack text widget
    scrollbar.config(command=text_widget.yview)  # Connect scrollbar
    # Display column headers
    header = f"{'ID':<10} {'Name':<20} {'Role':<12} {'Layout':<12} {'Last Login':<20}\n"
    text_widget.insert('1.0', header)  # Insert header
    text_widget.insert('2.0', "="*85 + "\n")  # Insert separator
    # Display each user's information
    for index, row in df.iterrows():  # Iterate through users
        # Format each user's data into a line
        line = f"{row['Keycard_ID']:<10} {row['Name']:<20} {row['Role']:<12} "
        line = line + f"{row['Layout']:<12} {row['Last_Login']:<20}\n"
        text_widget.insert(tk.END, line)  # Insert line into text widget
    text_widget.config(state='disabled')  # Make read-only
    # Create close button
    tk.Button(users_window, text="Close", font=('Arial', 11), 
             bg='#95A5A6', fg='white', command=users_window.destroy).pack(pady=10)

# GUI SETUP (main)
root = tk.Tk()  # Create main window 
root.title("Personalized Keycard Access System")  # Set title
root.geometry("500x400")  # Set window size
root.configure(bg='#2C3E50')  # Set background color

# Initialize database on startup
database_ready = initialize_database()  # Call initialization function
if database_ready:  # Check if database is ready
    # Create header frame
    header = tk.Frame(root, bg='#34495E', pady=20)
    header.pack(fill='x')
    # Display main title
    tk.Label(header, text="Medical Facility Access System", 
             font=('Arial', 18, 'bold'), bg='#34495E', fg='white').pack()
    # Display subtitle
    tk.Label(header, text="Secure Keycard Authentication", 
             font=('Arial', 11), bg='#34495E', fg='#BDC3C7').pack()
    # Create menu frame for buttons
    menu_frame = tk.Frame(root, bg='#2C3E50', pady=30)
    menu_frame.pack(expand=True)
    # Create login button
    tk.Button(menu_frame, text="🔐 Login with Keycard", font=('Arial', 13), 
              bg='#3498DB', fg='white', command=login_window, 
              width=25, height=2).pack(pady=10)
    # Create register button
    tk.Button(menu_frame, text="📝 Register New User", font=('Arial', 13), 
              bg='#2ECC71', fg='white', command=registration_window, 
              width=25, height=2).pack(pady=10)
    # Create view all users button
    tk.Button(menu_frame, text="👥 View All Users", font=('Arial', 13), 
              bg='#9B59B6', fg='white', command=view_all_users, 
              width=25, height=2).pack(pady=10)
    # Create exit button
    tk.Button(menu_frame, text="❌ Exit System", font=('Arial', 13), 
              bg='#E74C3C', fg='white', command=root.quit, 
              width=25, height=2).pack(pady=10)
    # Create footer
    footer = tk.Frame(root, bg='#34495E', pady=10)
    footer.pack(fill='x', side='bottom')
    # Display footer text
    tk.Label(footer, text="ENGR 13300 - Individual Project", 
             font=('Arial', 9), bg='#34495E', fg='#95A5A6').pack()

root.mainloop()  # Start GUI event loop