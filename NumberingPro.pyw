# Written by Jean-Pierre van der Poel @ 12 Sept 2023

# Use this code to generate numbers for use in CorelDRAW's mail merge function, similar to number-pro.com

import csv, math, datetime
import tkinter as tk
from tkinter import ttk
import re

# Bash-style brace expansion as input string
def expand_braces(input_string):
    parts = re.split(r'(\s+)', input_string)  # Split input_string by whitespace
    expanded_parts = []
    for part in parts:
        if '{' in part:  # Only expand part if it contains a brace expression
            while '{' in part:
                m = re.search(r'(\w*){([a-zA-Z0-9]+)..([a-zA-Z0-9]+)}(\w*)', part)
                if m:
                    prefix, start, end, suffix = m.groups()
                    if start.isdigit():
                        expansion = ' '.join(f'{prefix}{i}{suffix}' for i in range(int(start), int(end)+1))
                    else:
                        expansion = ' '.join(f'{prefix}{chr(i)}{suffix}' for i in range(ord(start), ord(end)+1))
                    part = part.replace(m.group(), expansion)
        expanded_parts.append(part)
    return ' '.join(expanded_parts).split()



def has_fraction(number):
    # Check if the number is not equal to its integer part
    return number != int(number)

def rows_to_columns(matrix):
    # Use list comprehension to transpose the matrix.
    transposed_matrix = [[row[i] for row in matrix] for i in range(len(matrix[0]))]
    return transposed_matrix

def generate_csv(starting_number, ending_number, padding, document_repeats, prefix, stackable, brace_str):
    data = []
    row = []
    column = []
    columns = []
    header = []
    array_2d = []
    numbers = []
    reverse = False

    # Create header
    for repeat in range(1, document_repeats + 1):
        header.append(f"No.{repeat}")
    data.append(header)

    # Create list of numbers
    if brace_str == '':
        if starting_number > ending_number:
            reverse = True
            tmp_start = starting_number
            tmp_end = ending_number
            ending_number = tmp_start
            starting_number = tmp_end
        for number in range(starting_number, ending_number+1):
            if padding > 0:
                number_str = str(number).zfill(padding)
            else:
                number_str = str(number)
            numbers.append(f"{prefix}{number_str}")
        if reverse:
            numbers.reverse()
    else:
        try:
            numbers = expand_braces(brace_str)
        except:
            return "Brace expansion failed!"

    if not stackable:
        while len(numbers):
            row = numbers[:document_repeats]
            numbers = numbers[document_repeats:]
            if len(row) < document_repeats:
                for counter in range(0, document_repeats - len(row)):
                    row.append('')
                    numbers = []
            data.append(row)
    else:
        if has_fraction(len(numbers) / document_repeats):
            column_length = int(math.ceil(len(numbers) / document_repeats))
        else:
            column_length = int(len(numbers) / document_repeats)
        while len(numbers):
            column = numbers[:column_length]
            numbers = numbers[column_length:]
            if len(column) < column_length:
                for counter in range(0, column_length - len(column)):
                    column.append('')
                    numbers = []
            columns.append(column)
        columns = rows_to_columns(columns)
        data.extend(columns)

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as a safe file name
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    with open('output_' + formatted_datetime + '.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    return 'output_' + formatted_datetime + '.csv'


starting_number = 0
ending_number = 0
padding = 0
document_repeats = 0
prefix = ''
stackable = False
brace_str = ''


def get_user_input():
    global starting_number, ending_number, padding, document_repeats, prefix, stackable, brace_str

    # Get input values from the entry widgets
    try:
        starting_number = int(starting_number_entry.get())
    except:
        starting_number = 1

    try:
        ending_number = int(ending_number_entry.get())
    except:
        ending_number = 100

    try:
        padding = int(padding_entry.get())
    except:
        padding = 0

    try:
        document_repeats = int(document_repeats_entry.get())
    except:
        document_repeats = 1

    prefix = prefix_entry.get()
    stackable = stackable_var.get()
    brace_str = brace_entry.get()

    result_file = generate_csv(starting_number, ending_number, padding, document_repeats, prefix, stackable, brace_str)
    result_label.config(text="Output saved to : " + result_file)

# Create the main window
root = tk.Tk()
root.title("Numbering Pro")

# Create labels and entry widgets for input fields
starting_number_label = ttk.Label(root, text="Starting Number:")
starting_number_label.grid(row=0, column=0, padx=10, pady=5)
starting_number_entry = ttk.Entry(root)
starting_number_entry.grid(row=0, column=1, padx=10, pady=5)

ending_number_label = ttk.Label(root, text="Ending Number:")
ending_number_label.grid(row=1, column=0, padx=10, pady=5)
ending_number_entry = ttk.Entry(root)
ending_number_entry.grid(row=1, column=1, padx=10, pady=5)

# Create a label and entry widget for the Brace Expansion
brace_label = ttk.Label(root, text="Brace Expansion:")
brace_label.grid(row=2, column=0, padx=10, pady=5)
brace_entry = ttk.Entry(root)
brace_entry.grid(row=2, column=1, padx=10, pady=5)
# Function to disable starting and ending number textboxes
def disable_start_end(event):
    if brace_entry.get() != "":
        starting_number_entry.config(state="disabled")
        ending_number_entry.config(state="disabled")
        padding_entry.config(state="disabled")
        prefix_entry.config(state="disabled")
    else:
        starting_number_entry.config(state="enabled")
        ending_number_entry.config(state="enabled")
        padding_entry.config(state="enabled")
        prefix_entry.config(state="enabled")
brace_entry.bind("<KeyRelease>", disable_start_end)

padding_label = ttk.Label(root, text="Padding:")
padding_label.grid(row=3, column=0, padx=10, pady=5)
padding_entry = ttk.Entry(root)
padding_entry.grid(row=3, column=1, padx=10, pady=5)

document_repeats_label = ttk.Label(root, text="Document Repeats:")
document_repeats_label.grid(row=4, column=0, padx=10, pady=5)
document_repeats_entry = ttk.Entry(root)
document_repeats_entry.grid(row=4, column=1, padx=10, pady=5)

prefix_label = ttk.Label(root, text="Prefix:")
prefix_label.grid(row=5, column=0, padx=10, pady=5)
prefix_entry = ttk.Entry(root)
prefix_entry.grid(row=5, column=1, padx=10, pady=5)

stackable_var = tk.BooleanVar()
stackable_checkbox = ttk.Checkbutton(root, text="Stackable", variable=stackable_var)
stackable_checkbox.invoke()
stackable_checkbox.grid(row=6, column=0, padx=10, pady=5)

# Create a button to get user input
get_input_button = ttk.Button(root, text="Generate", command=get_user_input)
get_input_button.grid(row=7, column=0, columnspan=2, pady=10)

# Create a label to display the result
result_label = ttk.Label(root, text="")
result_label.grid(row=8, column=0, columnspan=2)

# Start the tkinter main loop
root.mainloop()


if __name__ == '__main__':
    #generate_csv(starting_number, ending_number, padding, document_repeats, prefix, stackable)
    try:
        get_user_input()
    except:
        pass


