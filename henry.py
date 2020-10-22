from tkinter import *
from tkinter import ttk
from henryDAO import HenryDAO
import random


# GLOBAL DATA ACCESS OBJECT
DAO = HenryDAO()


class BranchInventory(ttk.Treeview):
    def __init__(self, tab_frame: ttk.Frame):
        # Creates the TreeView to display information about branch's inventory
        self.branch_inventory = ttk.Treeview(tab_frame, columns=(
            "Branch", "Copies Available"), show="headings")
        self.branch_inventory.heading("Branch", text="Branch")
        self.branch_inventory.heading(
            "Copies Available", text="Copies Available")
        self.branch_inventory.grid(row=0, column=0)

    def clear(self):
        # delete old values in tree list
        for item in self.branch_inventory.get_children():
            self.branch_inventory.delete(item)

    def display(self, inventory_info: [list]):
        # Fill Branch Inventory Treeview wiith info
        for item in inventory_info:
            self.branch_inventory.insert("", END, value=item)
        self.branch_inventory.column("Copies Available", anchor="center")
        self.branch_inventory.column("Branch", anchor="center")


class HenryResultPrice():
    # since all Search Type share the same Result TreeView, and the Price Tag Panel
    # I just pulled it up into a parent class
    # and have HenrySBA, SBC, SBP inherit from it
    # Creates the TreeView to display information about branch's inventory
    def __init__(self, tab_frame: ttk.Frame, optional_bg: str = "white"):
        self.branch_inventory = BranchInventory(tab_frame)
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

    def get_books(self, event, search_type: str = "author"):
        book_list = None
        if (search_type == "author"):
            book_list = DAO.get_author_books(event.widget.current() + 1)
        elif (search_type == "category"):
            book_list = DAO.get_category_books(event.widget.current() + 1)
        else:
            book_list = DAO.get_publisher_books(event.widget.current() + 1)
        book_title_list = [book.get_title()
                           for book in book_list]
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
        # TODO: Call HenryDAO for branch inventory
        branch_inventory = DAO.get_book_inventory(book.get_book_code())
        self.branch_inventory.clear()
        self.branch_inventory.display(branch_inventory)
        self.display_book_price(book.get_price())

    def display_book_price(self, book_price):
        self.price_tag["text"] = "${}".format(book_price)


class HenrySBA(HenryResultPrice):
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

        # Creates Book Selection ComboBox
        self.book_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # Create Label for Author Selection Combobox
        book_label = ttk.Label(
            tab_frame, text="BOOK SELECTION", background="white", relief="groove")
        book_label.grid(row=1, column=1,
                        pady=10, sticky="we")
        book_label.configure(anchor="center")

        # Fill Author Selection with Data and Position the widget
        self.author_selection["values"] = self.author_list
        self.author_selection.current(0)
        self.author_selection.bind(
            "<<ComboboxSelected>>", self.get_books)
        self.author_selection.grid(row=2, column=0)

        # Position the Book Selection next to Author Selection
        self.book_selection.grid(row=2, column=1)

        # Initialize Book Selection with Data from first author
        book_list = DAO.get_author_books(1)
        book_title_list = [book.get_title() for book in book_list]
        self.book_selection["values"] = book_title_list
        self.book_selection.current(0)

        # set default book to immediate display information about it
        default_book = book_list[0]
        self.display_book_price(default_book.get_price())
        self.book_selection.bind(
            "<<ComboboxSelected>>", lambda event, book_list=book_list: self.get_book_inventory(event, book_list))

        # Initialize Branch Inventory TreeView with first book's result
        branch_inventory = DAO.get_book_inventory(default_book.get_book_code())
        self.branch_inventory.clear()
        self.branch_inventory.display(branch_inventory)
        self.display_book_price(default_book.get_price())


class HenrySBC(HenryResultPrice):
    def __init__(self, tab_frame: ttk.Frame):
        # call parent constructor
        super().__init__(tab_frame, optional_bg="#98e7ed")
        # Creates the Genre Selection Combobox
        self.categories_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")
        # Create Label for Author Selection Combobox
        categories_label = ttk.Label(
            tab_frame, text="CATEGORIES SELECTION", background="white", relief="groove")
        categories_label.grid(row=1, column=0,
                              pady=10, sticky="we")
        categories_label.configure(anchor="center")

        # Creates Book Selection ComboBox
        self.book_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # Create Label for Author Selection Combobox
        book_label = ttk.Label(
            tab_frame, text="BOOK SELECTION", background="white", relief="groove")
        book_label.grid(row=1, column=1,
                        pady=10, sticky="we")
        book_label.configure(anchor="center")

        # TODO :Populate widgets with information using database calls
        # TODO Fill Categories Selection with Data and Position the widget
        self.categories_selection["values"] = [
            "Genre A", "Genre B", "Genre C", "Genre D"]
        self.categories_selection.current(0)
        self.categories_selection.bind(
            "<<ComboboxSelected>>", lambda event, search_type="category": self.get_books(event, search_type))
        self.categories_selection.grid(row=2, column=0)

        # Fill Book Selection with Data and position the widget next to Author Selection
        self.book_selection["values"] = ["PLEASE CHOOSE AN CATEGORY"]
        self.book_selection.grid(row=2, column=1)
        self.book_selection.current(0)


class HenrySBP(HenryResultPrice):
    def __init__(self, tab_frame: ttk.Frame):
        # call parent constructor
        super().__init__(tab_frame, optional_bg="#bce3d7")
        # Creates the Genre Selection Combobox
        self.publisher_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")
        # Create Label for Author Selection Combobox
        publisher_label = ttk.Label(
            tab_frame, text="CATEGORIES SELECTION", background="white", relief="groove")
        publisher_label.grid(row=1, column=0,
                             pady=10, sticky="we")
        publisher_label.configure(anchor="center")

        # Creates Book Selection ComboBox
        self.book_selection = ttk.Combobox(
            tab_frame, width=50, state="readonly", justify="center")

        # Create Label for Author Selection Combobox
        book_label = ttk.Label(
            tab_frame, text="BOOK SELECTION", background="white", relief="groove")
        book_label.grid(row=1, column=1,
                        pady=10, sticky="we")
        book_label.configure(anchor="center")

        # TODO :Populate widgets with information using database calls
        # TODO Fill Categories Selection with Data and Position the widget
        self.publisher_selection["values"] = [
            "Publisher A", "Publisher B", "Publisher C", "Publisher D"]
        self.publisher_selection.current(0)
        self.publisher_selection.bind(
            "<<ComboboxSelected>>", lambda event, search_type="publisher": self.get_books(event, search_type))
        self.publisher_selection.grid(row=2, column=0)

        # Fill Book Selection with Data and position the widget next to Author Selection
        self.book_selection["values"] = ["PLEASE CHOOSE AN PUBLISHER"]
        self.book_selection.grid(row=2, column=1)
        self.book_selection.current(0)

    def get_category_books(self, event):
        # TODO call HenryDAO function for data
        print("Category chosen is {}".format(event.widget.current()))
        # TODO implement as function call to HenryDAO
        book_list = ["Book A", "Book B", "Book C", "Book D"]
        # Fill Book Selection with Data and position the widget next to Author Selection
        self.book_selection["values"] = book_list
        self.book_selection.current(0)
        self.book_selection.bind(
            "<<ComboboxSelected>>", lambda event, book_list=book_list: self.get_book_inventory(event, book_list))


def main():
    main_window = Tk()
    main_window.title("Henry Bookstore")
    main_window.geometry("800x500")

    # create Tab Control widget
    tab_ctrl = ttk.Notebook(main_window)
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

    main_window.mainloop()


if __name__ == "__main__":
    main()
