import tkinter as tk

def validate_input():
    # get user input from Entry widget
    input_text = entry.get()
    
    # check if input is valid
    if input_text.isdigit():
        # input is valid, do something with it
        print(f"Valid input: {input_text}")
    else:
        # input is not valid, show error label
        error_label.config(text="Invalid input!")
        
# create the main window
root = tk.Tk()

# create the input Entry widget
entry = tk.Entry(root)
entry.pack()

# create the error Label widget (hidden by default)
error_label = tk.Label(root, text="", fg="red")
error_label.pack()

# create the submit button
submit_button = tk.Button(root, text="Submit", command=validate_input)
submit_button.pack()

# start the main event loop
root.mainloop()