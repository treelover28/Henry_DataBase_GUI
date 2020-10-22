from tkinter import *
from tkinter import ttk
from henryDAO import HenryDAO
import time

# GLOBAL DATA ACCESS OBJECT
DAO = None


class HenryBaseComponent():
    # INNER CLASS OF HENRY BASE COMPONENT -----------------------------------------------------------
    class BranchInventory(ttk.Treeview):
        def __init__(self, tab_frame: ttk.Frame):
            # Creates the TreeView to display information about branch's inventory
            self.branch_inventory = ttk.Treeview(tab_frame, columns=(
                "Branch", "Copies Available"), show="headings")
            # Position Treview in top left corner
            self.branch_inventory.grid(row=0, column=0)
            self.branch_inventory.heading("Branch", text="Branch")
            self.branch_inventory.heading(
                "Copies Available", text="Copies Available")

        def clear(self):
            # delete old values in tree list
            for item in self.branch_inventory.get_children():
                self.branch_inventory.delete(item)

        def display(self, inventory_info: [list]):
            # Fill Branch Inventory Treeview wiith info
            for item in inventory_info:
                self.branch_inventory.insert("", END, value=item)
            # Display Headings
            self.branch_inventory.column("Copies Available", anchor="center")
            self.branch_inventory.column("Branch", anchor="center")
    # --------------------------------------------------------------------------------------------

    # Since all Search Type share the same Result TreeView, and the Price Tag Panel
    # I just pulled it up into a parent class
    # and have HenrySBA, SBC, SBP inherit from it
    # Creates the TreeView to display information about branch's inventory
    def __init__(self, tab_frame: ttk.Frame, optional_bg: str = "white"):
        # Create Branch Inventory
        self.branch_inventory = self.BranchInventory(tab_frame)

        # Creates Book Selection ComboBox
        self.book_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")
        # Position the Book Selection next to Category Selection
        self.book_selection.grid(row=2, column=1)

        # Create Label for Book Selection Combobox
        book_label = ttk.Label(
            tab_frame, text="BOOK SELECTION", background="white", relief="groove")
        book_label.grid(row=1, column=1,
                        pady=10, sticky="we")
        book_label.configure(anchor="center")

        # Creates the Price Panel
        self.price_panel = Frame(
            tab_frame, background=optional_bg)
        self.price_label = ttk.Label(
            tab_frame, text="PRICE", background="white", relief="groove")
        self.price_tag = ttk.Label(
            self.price_panel, text="", background=optional_bg, font=("Helvetica", 40))

        # position price label on top of Price Panel
        self.price_label.grid(row=0, column=1, sticky="nwe")
        self.price_label.configure(anchor="center")
        # position price panel in the top right corner
        self.price_panel.grid(row=0, column=1, sticky="nswe")
        # raise panel so it is more visually distinguishable
        self.price_panel.config(relief="raised")

        # position actual price to be right half of Price Panel
        self.price_tag.pack(expand=5)
        self.price_tag.configure(anchor="center")

    def get_books(self, event, search_type: str = "author", default_index=0, return_upon_fetch=False):
        book_list = None
        # allow Programmer to specify index in function call
        # without relying on the GUI ComboBox
        # Easier to do GUI initialization
        index = default_index
        if (event != None):
            # if event is not None, it means
            # the GUI session is active
            # just use index from ComboxBox selection
            index = event.widget.current()
        if (search_type == "author"):
            book_list = DAO.get_author_books(index + 1)
        elif (search_type == "category"):
            category_list = DAO.get_categories()
            book_list = DAO.get_category_books(category_list[index])
        else:
            publisher_list = DAO.get_publishers()
            book_list = DAO.get_publisher_books(
                publisher_list[index].get_publisher_code())

        # used for debuging
        if (return_upon_fetch):
            print(book_list)
            return book_list

        # give only Book's Title to Book Selection combobox
        book_title_list = [book.get_title() for book in book_list]
        default_book = book_list[0]

        # Fill Book Selection with Data and position the widget next to Author Selection
        self.book_selection["values"] = book_title_list
        self.book_selection.current(0)
        self.display_book_price(default_book.get_price())

        # Fill Branch Inventory with info regarding default book
        # When user suddenly switches author, the inventory will update immediately
        branch_inventory = DAO.get_book_inventory(default_book.get_book_code())
        self.branch_inventory.clear()
        self.branch_inventory.display(branch_inventory)

        # bind book selection to callback function to get inventory of new selection
        self.book_selection.bind(
            "<<ComboboxSelected>>", lambda event, book_list=book_list: self.get_book_inventory(event, book_list))

    def get_book_inventory(self, event, book_list):
        book = book_list[event.widget.current()]
        # Call HenryDAO for branch inventory
        branch_inventory = DAO.get_book_inventory(book.get_book_code())
        self.branch_inventory.clear()
        self.branch_inventory.display(branch_inventory)
        self.display_book_price(book.get_price())

    def display_book_price(self, book_price):
        self.price_tag["text"] = "${}".format(book_price)


class HenrySBA(HenryBaseComponent):
    def __init__(self, tab_frame: ttk.Frame):
        # call parent constructor
        super().__init__(tab_frame, optional_bg="#ff8863")
        # Creates the Author Selection Combobox
        self.author_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # get list of authors from DAO function call
        self.author_list = [author.__str__() for author in DAO.get_authors()]

        # Create Label for Author Selection Combobox
        author_label = ttk.Label(
            tab_frame, text="AUTHOR SELECTION", background="white", relief="groove")
        author_label.grid(row=1, column=0,
                          pady=10, sticky="we")
        author_label.configure(anchor="center")

        # Fill Author Selection with Data
        self.author_selection["values"] = self.author_list
        self.author_selection.current(0)
        self.author_selection.bind(
            "<<ComboboxSelected>>", self.get_books)
        # Position the widget in bottom left corner under its Label
        self.author_selection.grid(row=2, column=0)

        # Initialize Book Selection with Data from first author by default
        self.get_books(event=None, search_type="author", default_index=0)


class HenrySBC(HenryBaseComponent):
    def __init__(self, tab_frame: ttk.Frame):
        # call parent constructor
        super().__init__(tab_frame, optional_bg="#98e7ed")
        # Creates the Category Selection Combobox
        self.category_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # get list of categories from DAO function call
        self.category_list = DAO.get_categories()

        # Create Label for Category Selection Combobox
        category_label = ttk.Label(
            tab_frame, text="CATEGORY AUTHORSELECTION", background="white", relief="groove")
        category_label.grid(row=1, column=0,
                            pady=10, sticky="we")
        category_label.configure(anchor="center")

        # Fill Category Selection with Data and Position the widget
        self.category_selection["values"] = self.category_list
        self.category_selection.current(0)
        self.category_selection.bind(
            "<<ComboboxSelected>>", lambda event: self.get_books(event, search_type="category"))
        self.category_selection.grid(row=2, column=0)

        # Initialize Book Selection with Data from first cateogry
        self.get_books(
            event=None, search_type="category", default_index=0)


class HenrySBP(HenryBaseComponent):
    def __init__(self, tab_frame: ttk.Frame):
        # call parent constructor
        super().__init__(tab_frame, optional_bg="#8df0c7")
        # Creates the Publisher Selection Combobox
        self.publisher_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # get list of publisher from DAO function call
        self.publisher_list = [publisher.get_publisher_name()
                               for publisher in DAO.get_publishers()]

        # create Label for Publisher Selection Combobox
        publisher_label = ttk.Label(
            tab_frame, text="PUBLISHER AUTHORSELECTION", background="white", relief="groove")
        publisher_label.grid(row=1, column=0,
                             pady=10, sticky="we")
        publisher_label.configure(anchor="center")

        # Fill Category Selection with Data and Position the widget
        self.publisher_selection["values"] = self.publisher_list
        self.publisher_selection.current(0)
        self.publisher_selection.bind(
            "<<ComboboxSelected>>", lambda event: self.get_books(event, search_type="publisher"))
        self.publisher_selection.grid(row=2, column=0)

        # Initialize Book Selection with Data from first cateogry
        self.get_books(
            event=None, search_type="publisher", default_index=0)


def render_app(root):
    # create Tab Control widget
    tab_ctrl = ttk.Notebook(root)
    # Create "Search By Author", "Categories", "Publisher" tabs
    tab_sba = ttk.Frame(tab_ctrl)
    tab_sbc = ttk.Frame(tab_ctrl)
    tab_sbp = ttk.Frame(tab_ctrl)
    # add the tabs to Tab Control widget
    tab_ctrl.add(tab_sba, text="Search By Author")
    tab_ctrl.add(tab_sbc, text="Search By Categories")
    tab_ctrl.add(tab_sbp, text="Search By Publisher")
    # pack the Tab Control on the screen
    tab_ctrl.pack()
    # Add the frame associated with each tab to screen
    SBA_frame = HenrySBA(tab_sba)
    SBC_frame = HenrySBC(tab_sbc)
    SBP_frame = HenrySBP(tab_sbp)


def exit_app(root, top):
    # destroy everything and end the app
    top.destroy()
    root.destroy()
    sys.exit()


def validate_db_login(root, login_pane, connection_msg, username, password, db_name, host):
    global DAO

    try:
        DAO = HenryDAO(username, password, db_name, host)
        # Render Bookstore App
        render_app(root)
        # Unhide main window
        root.deiconify()
        # Destroy login panel
        login_pane.destroy()

    except ValueError:
        connection_msg["text"] = "Login Credential is INVALID."


def main():
    # GLOBAL DATA ACCESS OBJECT
    global DAO

    main_window = Tk()
    main_window.title("Henry Bookstore by Khai Lai")
    main_window.geometry("800x500")

    login_panel = Toplevel()
    login_panel.title("Sign in to Henry Bookstore's Database")
    login_panel.geometry("300x150")

    # Database Login Form
    username_label = Label(login_panel, text="Username: ")
    username_label.grid(row=0, column=0)
    # username entry form
    username = StringVar()
    username_input = Entry(login_panel, textvariable=username)
    username_input.grid(row=0, column=1)

    # password entry form
    password_label = Label(login_panel, text="Password: ")
    password_label.grid(row=1, column=0)
    password = StringVar()
    password_input = Entry(login_panel, textvariable=password, show="*")
    password_input.grid(row=1, column=1)

    # database name entry form
    database_label = Label(login_panel, text="Database: ")
    database_label.grid(row=2, column=0)
    db_name = StringVar()
    database_input = Entry(login_panel, textvariable=db_name)
    database_input.grid(row=2, column=1)

    # host ip entry form
    host_label = Label(login_panel, text="Host IP: ")
    host_label.grid(row=3, column=0)
    host_name = StringVar()
    host_input = Entry(login_panel, textvariable=host_name)
    # by default, it is local host
    host_input.insert(0, "localhost")
    host_input.grid(row=3, column=1)

    # Login button
    # If Login is successful then it will display the Bookstore app
    login_button = Button(login_panel, text="LOGIN", command=lambda: validate_db_login(
        root=main_window,
        login_pane=login_panel,
        connection_msg=connection_status,
        username=username_input.get().strip(),
        password=password_input.get().strip(),
        db_name=database_input.get().strip(),
        host=host_input.get().strip())
    )
    login_button.grid(row=4, column=0)

    # Exit button
    exit_button = Button(login_panel, text="EXIT",
                         command=lambda: exit_app(main_window, login_panel))
    exit_button.grid(row=4, column=1)

    # To receive connection status from validate_db_login()
    connection_status = Label(login_panel, text="")
    connection_status.grid(row=5, column=0, columnspan=2)

    # hide main window right now
    # only display top level login page
    main_window.withdraw()

    # handles user clicking X while on Login Panel
    # Else, UI would close, but script would not terminate
    login_panel.protocol("WM_DELETE_WINDOW", lambda: exit_app(
        root=main_window, top=login_panel))

    main_window.mainloop()


if __name__ == "__main__":
    main()
