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

import pandas as pd  # For reading Excel database files
import re  # For regular expression pattern matching (string validation)

def validate_keycard_format(keycard_id): #Validate keycard ID format (3 Letters + 3 Numbers)
    if not keycard_id:  # Check if empty string
        # error message
        error_message = "Keycard ID cannot be empty."
        return False, error_message  # Returns tuple (bool, string)
    
    # Check keycard length
    if len(keycard_id) != 6:  # Check if not exactly 6 characters
        # Return validation failure with format hint
        error_message = "Keycard ID must be exactly 6 characters.\nFormat: ABC123 (3 letters + 3 numbers)"
        return False, error_message
    
    # Check keycard format using regex
    pattern = r'^[A-Z]{3}[0-9]{3}$'  # Define required format pattern (copilot help)
    if not re.match(pattern, keycard_id):  # Check if doesn't match pattern
        # Return validation failure with example format
        error_message = "Invalid format.\nRequired: 3 uppercase letters + 3 numbers\nExample: DOC001, NUR042, ADM100"
        return False, error_message
    
    # If all checks passed = keycard format is valid
    return True, None  # Return with no error message (None)

# User authentication function / searches database for keycard id
def authenticate_user(keycard_id, database_file):
    # Read Excel file into pandas DataFrame
    df = pd.read_excel(database_file)
    
    for index, row in df.iterrows():  #  Loop throuh database rows
        # Check if current row's keycard matches search ID
        if row['Keycard_ID'] == keycard_id:
            # Create dictionary with user's data
            user_data = {
                'Keycard_ID': row['Keycard_ID'],  # Store keycard ID
                'Name': row['Name'],  # Store full name
                'Role': row['Role'],  # Store role (Doctor, Nurse, etc.)
                'Tool1': row['Tool1'],  # Store first configured tool
                'Tool2': row['Tool2'],  # Store second configured tool
                'Tool3': row['Tool3'],  # Store third configured tool
                'Layout': row['Layout'],  # Store layout preference
                'Last_Login': row['Last_Login']  # Store last login timestamp
            }
            # Return user data dictionary
            return user_data
    
    # If loop completes without finding match
    return None  # Return None to indicate authentication failed

# Verify if keycard ID already exists in database
def keycard_exists(keycard_id, database_file):
    # Read Excel file into DataFrame
    df = pd.read_excel(database_file)
    
    # Check if keycard_id exists in the 'Keycard_ID' column ('in' operator checks if value is present in pandas Series)
    return keycard_id in df['Keycard_ID'].values  # Returns True or False

# Read complete database into memory for processing
def load_database(database_file):
    # Read Excel file and return as DataFrame
    df = pd.read_excel(database_file)
    return df  # Return DataFrame containing all database records

# Get all users with a specific role (Doctor, Nurse, etc.)
def get_users_by_role(role, database_file):
    # Read Excel database
    df = pd.read_excel(database_file)
    
    # Filter DataFrame to only rows where Role column matches parameter
    filtered = df[df['Role'] == role]
    
    # Create empty list to store user dictionaries
    users = []
    
    # Convert each row to a dictionary and add to list
    for index, row in filtered.iterrows():  # Loop through filtered rows
        # Create dictionary for this user
        user_data = {
            'Keycard_ID': row['Keycard_ID'],  # Store keycard
            'Name': row['Name'],  # Store name
            'Role': row['Role'],  # Store role
            'Tool1': row['Tool1'],  # Store tool 1
            'Tool2': row['Tool2'],  # Store tool 2
            'Tool3': row['Tool3'],  # Store tool 3
            'Layout': row['Layout']  # Store layout preference
        }
        users.append(user_data)  # Add dictionary to list
    
    # Return list of user dictionaries
    return users

# Get statistics on how many users have each role
def count_users_by_role(database_file):
    # Read Excel database
    df = pd.read_excel(database_file)
    
    # Create empty dictionary to store counts
    role_counts = {}
    
    # Get list of unique roles in database
    roles = df['Role'].unique()  # Returns array of unique role values
    
    # Calculate how many users have each role
    for role in roles:  # Iterate through each unique role
        # Count how many rows have this role
        count = len(df[df['Role'] == role])
        # Store count in dictionary with role as key
        role_counts[role] = count
    
    # Return dictionary of role counts
    return role_counts  # Ex: {'Doctor': 2, 'Nurse': 1, 'Admin': 1}

# Ensure tool names are valid and appropriate
def validate_tool_name(tool_name):
    # Check if tool name is empty
    if not tool_name or tool_name.strip() == "":  # Check if empty
        return False, "Tool name cannot be empty."
    # Check minimum length
    if len(tool_name.strip()) < 3:  # Check if too short
        return False, "Tool name must be at least 3 characters long."
    
    # Check for invalid characters using regex
    if not re.match(r'^[A-Za-z0-9_\- ]+$', tool_name):  # Check characters (regex help w copilot)
        return False, "Tool name can only contain letters, numbers, spaces, hyphens, and underscores."
    
    # All validation checks passed
    return True, None  # Return success