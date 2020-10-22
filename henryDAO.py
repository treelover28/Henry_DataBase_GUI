import mysql.connector


class HenryDAO:
    # INNER CLASSES -----------------------------------------------------------------------------------------
    class Author:
        def __init__(self, author_num, author_last, author_first):
            self.author_num = author_num
            self.author_last = author_last
            self.author_first = author_first

        def get_author_num(self):
            return self.author_num

        def get_author_last(self):
            return self.author_last

        def get_author_first(self):
            return self.author_first

        def __str__(self):
            return ("{}, {}".format(self.get_author_first(), self.get_author_last()))

    class Book:
        def __init__(self, book_code, title, price):
            self.book_code = book_code
            self.title = title
            self.price = price

        def get_book_code(self):
            return self.book_code

        def get_title(self):
            return self.title

        def get_price(self):
            return self.price

    class Branch_Inventory:
        def __init__(self, branch_name, inventory):
            self.branch_name = branch_name
            self.inventory = inventory

        def get_branch_name(self):
            return self.branch_name

        def get_inventory(self):
            return self.inventory

    # ---------------------------------------------------------------------------------------------------------

    def __init__(self):
        # initialize connection object
        self.db = mysql.connector.connect(
            # When grading, please replace with your user credentials
            user="root",
            passwd="V9n5csjf!",
            database="henryDB",
            host="localhost"
        )
        self.cursor = self.db.cursor()

    def close(self):
        # atomic transaction
        self.db.commit()
        self.db.close()

    def execute_query(self, query: str, print_result: bool = True):
        self.cursor.execute(query)
        if self.cursor == None:
            print("Error: query is malformed. Please fix and try again")
            return
        if (print_result):
            for row in self.cursor:
                i = 0
                while(i < len(row)):
                    print("{:4^}".format(row[i]), end=" ")
                    i += 1
                print()

    def get_authors(self):
        # only return authors whose books are carried by Henry
        sql_query = """
        select *from HENRY_AUTHOR where AUTHOR_NUM in
        (
            select AUTHOR_NUM
            from HENRY_BOOK book join
                 HENRY_WROTE wrote
                 on book.BOOK_CODE = wrote.BOOK_CODE
        );"""
        self.execute_query(sql_query, print_result=False)
        authors = []
        for row in self.cursor:
            author = self.Author(
                author_num=row[0],
                author_last=row[1],
                author_first=row[2]
            )
            authors.append(author)
        return authors

    def get_author_books(self, author_num):
        sql_query = """
            select wrote.BOOK_CODE,TITLE,PRICE
            from HENRY_BOOK book join HENRY_WROTE wrote 
            on book.BOOK_CODE = wrote.BOOK_CODE
            where wrote.AUTHOR_NUM = {};
            """.format(author_num)

        self.execute_query(sql_query, print_result=False)
        books = []
        for row in self.cursor:
            book = self.Book(
                book_code=row[0],
                title=row[1],
                price=row[2]
            )
            books.append(book)
        return books

    def get_category_books(self, category_num):
        # TODO Fill in SQL
        sql_query = """
            select stuff {};
            """.format(category_num)

        self.execute_query(sql_query, print_result=False)
        books = []
        for row in self.cursor:
            book = self.Book(
                book_code=row[0],
                title=row[1],
                price=row[2]
            )
            books.append(book)
        return books

    def get_publisher_books(self, publisher_id):
        # TODO Fill in SQL
        sql_query = """
            select stuff {};
            """.format(publisher_id)

        self.execute_query(sql_query, print_result=False)
        books = []
        for row in self.cursor:
            book = self.Book(
                book_code=row[0],
                title=row[1],
                price=row[2]
            )
            books.append(book)
        return books

    def get_book_inventory(self, book_code):
        sql_query = """
            select BRANCH_NAME, ON_HAND
            from HENRY_BRANCH branch join HENRY_INVENTORY inventory 
            on branch.BRANCH_NUM = inventory.BRANCH_NUM
            where inventory.BOOK_CODE = '{}';
        """.format(book_code)
        self.execute_query(sql_query, print_result=False)
        branch_inventory_info = []
        for row in self.cursor:
            name_onhand = [row[0], row[1]]
            branch_inventory_info.append(name_onhand)
        return branch_inventory_info


# henry = HenryDAO()
# henry.get_authors()
