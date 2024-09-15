import random
import pyperclip

from utils.handler import create_db, get_data

from utils.create_vault import CreateVault

from utils.vault_del_option import VaultDelete

from utils.vault_opener import GivePswEntry


import customtkinter as ct
import tkinter.messagebox

#hide the db with . on start!
DB_FILE = ".vaults.db"    
DEFAULT_WINDOW_WIDTH = 1100
DEFAULT_WINDOW_HEIGHT = 580
ct.set_appearance_mode("Dark")
ct.set_default_color_theme("green")


class Vaultronite(ct.CTk):
    """The main class, representing the application itself."""

    # Used later to detect whether these dialogs exist already or not.
    del_vault_dialog = create_vault = enter_pwd_dialog = None

    def __init__(self) -> None:
        """Initializes the app and its components."""

        super().__init__()  # call base constructor

        # Set default window props
        self.sidebar_frame = ct.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.title("Vaultronite")  # title
        self.geometry(f"{DEFAULT_WINDOW_WIDTH}x{DEFAULT_WINDOW_HEIGHT}")  # dimensions
        self.configure(fg_color="#141212")  # bg color
        self.rowconfigure(1, weight=1)  # enable easy horizontal scaling on resize
        self.columnconfigure(0, weight=1)  # enable easy vertical scaling on resize
        self.appearance_mode_optionemenu = ct.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        # create database
        create_db(DB_FILE)

        # setup app userint
        self.build_ui(DB_FILE)
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)

   ######### RANDOMLY PASSWORD GENERATOR CONFIGURATION ###################################    
    def generate_random_password(self) -> str:
        """Generate a random password."""
        import string as str
        # Define the minimum and maximum length for the password
        min_length = 15
        max_length = 65
        
        # Define characters to use in generating the password
        characters = str.ascii_letters + str.digits + str.punctuation
        
        # Generate the random password
        password_length = random.randint(min_length, max_length)
        password = ''.join(random.choice(characters) for _ in range(password_length))
        
        return password


    def init_passw_generator(self) -> None:


        """Initialize the password generator window."""
        
        # Create a customtkinter window for displaying the generated password
        window = ct.CTk()
        window.title("Random Password Generator")
        window.geometry("500x250")
        
        # Label to display the generated password
        password_label = ct.CTkLabel(window, text="Your Password:", pady=20)
        password_label.pack()
        
        password_box = ct.CTkEntry(window)
        password_box.pack()

        def copy_password(event=None):
            password_box.clipboard_clear()
            password_box.clipboard_append(password_box.get())
        
        copy_button = ct.CTkButton(window, text="Copy", command=copy_password)
        copy_button.pack(padx=5, pady=10)
        
        # Function to generate and display the password in the label
        def display_password():
            password = self.generate_random_password()
            password_box.insert(0, password)
        
        # Button to generate and display the password
        generate_button = ct.CTkButton(window, text="Generate Password", command=display_password)
        generate_button.pack(pady=10)

        
        


# Run the customtkinter main loop
        window.mainloop()

####################        ####################           #############################
    def build_ui(self, db_file: str) -> None:
        """Creates the necessary widgets for the app UI.

        Args:
         - db_file: filename of the database to use.

        Returns: None
        """

        # HEADER CONFIG
        # header main frame
        self.header = ct.CTkFrame(self, fg_color="#212121", corner_radius=0)
        self.header.grid(row=0, column=0, sticky="new")

        # Created Vault's shown label
        self.header.label = ct.CTkLabel(self.header, text="Your Created Vaults")
        self.header.label.cget("font").configure(size=20, weight="bold")
        self.header.label.pack(side="bottom", padx=30, pady=10)

        # header 'add vaults' button
        self.header.button_add_vaults = ct.CTkButton(
            self.header,
            text="Add New Vault",
            command=lambda db=db_file: self.init_create_vault(db_file),
        )
        self.header.button_add_vaults.pack(side="right", padx=0, pady=10)

        # header 'password generator' button
        self.header.button_passw_genert = ct.CTkButton(
            self.header,
            text="Password Generator",
            command=self.init_passw_generator
        )
        self.header.button_passw_genert.pack(side="right", padx=30, pady=10)


        # header 'delete vaults' button
        self.header.button_del_vaults = ct.CTkButton(
            self.header,
            text="Delete Vault",
            command=lambda: self.init_vault_del_option(db_file),
        )
        self.header.button_del_vaults.pack(
            side="right", padx=20, pady=10, before=self.header.button_add_vaults
        )

        # VAULT UI
        VAULTS_PER_ROW = 5
        available_vaults = get_data(db_file, "SELECT * FROM vaults;")

        # vault container
        self.vault_container = ct.CTkScrollableFrame(self, fg_color="transparent")
        self.vault_container.grid(row=1, column=0, sticky="nsew")

        # setup vault container's grid
        rows = (len(available_vaults) // VAULTS_PER_ROW) + 1
        for i in range(rows):
            self.vault_container.rowconfigure(i, weight=1)
        for i in range(VAULTS_PER_ROW):
            self.vault_container.columnconfigure(i, weight=1)

        for i, vault in enumerate(available_vaults):
            # Temporary vault frame
            tmpv_frame = ct.CTkFrame(
                self.vault_container, fg_color="#212121", corner_radius=15
            )
            r = (i) // VAULTS_PER_ROW
            c = (i) % VAULTS_PER_ROW
            tmpv_frame.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")

            

            # temporary vault label
            tmpv_label = ct.CTkLabel(tmpv_frame, text=vault[1], justify="center")
            tmpv_label.cget("font").configure(size=18, weight="bold")
            tmpv_label.pack(expand=True, padx=20)

            # temporary vault button
            tmpv_button = ct.CTkButton(
                tmpv_frame,
                text="Enter Vault",
                command=lambda vid=vault[0]: self.init_enter_pwd_dialog(vid, db_file),
            )
            tmpv_button.pack(expand=True, pady=15, padx=20)

    def init_create_vault(self, db_file: str) -> None:
        """Initializes the Add Vault Dialog if it does not already exist.

        Args:
            db_file (str): The filename of the database to use.

        Returns:
            None
        """

        # Check if the AddVaultDialog has already been created and exists on the screen
        if self.create_vault is not None and self.create_vault.winfo_exists():
            # If it does, give focus to the dialog and return
            self.create_vault.focus()
            return

        # If the dialog does not exist, create a new instance of AddVaultDialog
        # and kill any instances of other dialogs if they exist
        self.del_vault_dialog.destroy() if self.del_vault_dialog else None
        self.enter_pwd_dialog.destroy() if self.enter_pwd_dialog else None
        self.create_vault = CreateVault(db_file, self)

    def init_vault_del_option(self, db_file: str) -> None:
        """Initializes the Delete Vault Dialog if it does not already exist.

        Args:
            db_file (str): The filename of the database to use.

        Returns:
            None
        """

        # Check if the DeleteVaultDialog has already been created and exists on the screen
        if self.del_vault_dialog is not None and self.del_vault_dialog.winfo_exists():
            # If it does, give focus to the dialog and return
            self.del_vault_dialog.focus()
            return

        # If the dialog does not exist, create a new instance of DeleteVaultDialog
        # and kill any instances of other dialogs if they exist
        self.create_vault.destroy() if self.create_vault else None
        self.enter_pwd_dialog.destroy() if self.enter_pwd_dialog else None
        self.del_vault_dialog = VaultDelete(db_file, self)

    ###############################################################   
    



    ################################################

    def init_enter_pwd_dialog(self, vid: int, db_file: str) -> None:
        """Initializes the Enter Password Dialog if it does not already exist.

        Args:
         - vid (int): The ID of the vault to open.
         - db_file (str): The filename of the database to use.

        Returns: None
        """

        # Get the available vaults from the database
        available_vaults = get_data(db_file, "SELECT * FROM vaults;")

        # Find the vault with the specified ID
        for vault in available_vaults:
            if vid == vault[0]:
                selected_vault = vault
                break
        else:
            raise ValueError(f"No vault found with ID {vid}")

        
        # Check if the GivePswEntry has already been created and exists on the screen
        if self.enter_pwd_dialog is not None and self.enter_pwd_dialog.winfo_exists():
            # If it does, give focus to the dialog and return
            self.enter_pwd_dialog.focus()
            return

        # If the dialog does not exist, create a new instance of GivePswEntry
        # and kill any instances of other dialogs if they exist
        self.create_vault.destroy() if self.create_vault else None
        self.del_vault_dialog.destroy() if self.del_vault_dialog else None
        self.enter_pwd_dialog = GivePswEntry(db_file, selected_vault)


def main():
    app = Vaultronite()
    app.mainloop()


main()
