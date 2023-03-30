import tkinter as tk

root = tk.Tk()

# Define button properties
button_width = 10
button_height = 2
button_bg = "white"
button_fg = "black"
button_font = ("Arial", 12)

# Define button names and corresponding output messages
button_info = {
    "Button 1": "You clicked Button 1!",
    "Button 2": "You clicked Button 2!",
    "Button 3": "You clicked Button 3!",
    "Button 4": "You clicked Button 4!"
}

# Function to display output message
def display_output(message):
    output_label.config(text=message)

# Function to generate button commands
def generate_button_command(button_name):
    return lambda message=button_info[button_name]: display_output(message)

# Loop to create buttons
for i, button_name in enumerate(button_info.keys()):
    button = tk.Button(root, text=button_name, width=button_width, height=button_height, bg=button_bg, fg=button_fg, font=button_font, command=generate_button_command(button_name))
    button.grid(row=i, column=0, padx=5, pady=5)

# Label to display output message
output_label = tk.Label(root, text="")
output_label.grid(row=len(button_info), column=0, padx=5, pady=5)

root.mainloop()