import customtkinter
import string
import random

customtkinter.set_appearance_mode("Dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
customtkinter.set_window_scaling 
app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("800x400")  # Increase width and height to accommodate wider text box and input fields
app.title = app.title("Password Generator")

def generate_random_password(min_length, max_length):
    # Define characters to use in the password
    characters = string.ascii_letters + string.digits + string.punctuation
    # Generate a random password of random length within the specified range
    length = random.randint(min_length, max_length)
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_custom_password(words):
    # Shuffle the input words to create variation
    random.shuffle(words)
    # Join the shuffled words together without adding extra characters
    password = ''.join(words)
    return password

def open_input_window():
    # Create a new CTk window for inputting preferred words
    input_window = customtkinter.CTk()
    input_window.title("Enter Preferred Words")
    input_window.geometry("400x300")

    words_label = customtkinter.CTkLabel(input_window, text="Enter your preferred words separated by spaces:")
    words_label.pack(pady=10)

    words_entry = customtkinter.CTkEntry(input_window, width=550)
    words_entry.pack(pady=20)

    def generate_custom_password_from_input():
        words_input = words_entry.get().strip()
        if words_input:
            words = words_input.split()  # Split input into a list of words
            password = generate_custom_password(words)
            update_password_textbox(password)
            input_window.destroy()  # Close the input window after generating the password
        else:
            customtkinter.messagebox.showerror("Error", "No words provided. Please try again.")

    generate_button = customtkinter.CTkButton(input_window, text="Generate Password", command=generate_custom_password_from_input)
    generate_button.pack(pady=10)

    input_window.mainloop()

def generate_random_button_function():
    # Generate a random length for the password within a specific range
    min_length = 15
    max_length = 70
    password = generate_random_password(min_length, max_length)
    update_password_textbox(password)

def update_password_textbox(password):
    # Update the text box with the generated password
    textbox.delete(1.0, customtkinter.END)  # Clear existing text
    textbox.insert(customtkinter.END, password)  # Insert generated password

# Use CTkTextbox to display the generated password
textbox = customtkinter.CTkTextbox(master=app, width=500, height=20, font=("Arial", 12))
textbox.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

# Create buttons for random password generation and custom password generation
random_button = customtkinter.CTkButton(master=app, text="Generate Random Password", command=generate_random_button_function)
random_button.place(relx=0.3, rely=0.8, anchor=customtkinter.CENTER)

custom_button = customtkinter.CTkButton(master=app, text="Generate Custom Password", command=open_input_window)
custom_button.place(relx=0.7, rely=0.8, anchor=customtkinter.CENTER)

app.mainloop()
