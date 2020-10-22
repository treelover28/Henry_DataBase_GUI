select *
from HENRY_AUTHOR;

select *
from HENRY_WROTE;

select *
from HENRY_BOOK;

-- return authors who actually has a book carried by Henry
select *
from HENRY_AUTHOR
where AUTHOR_NUM in (
                select AUTHOR_NUM
                from HENRY_BOOK book
                        join HENRY_WROTE wrote on book.BOOK_CODE = wrote.BOOK_CODE
        );

select wrote.BOOK_CODE,
        TITLE,
        PRICE
from HENRY_BOOK book
        join HENRY_WROTE wrote on book.BOOK_CODE = wrote.BOOK_CODE
where wrote.AUTHOR_NUM = 1;

select BRANCH_NAME,
        ON_HAND
from HENRY_BRANCH branch
        join HENRY_INVENTORY inventory on branch.BRANCH_NUM = inventory.BRANCH_NUM
where inventory.BOOK_CODE = "0808";

select *
from HENRY_BOOK;

select TYPE
from HENRY_BOOK
group by TYPE;

select BOOK_CODE,
        TITLE,
        PRICE
from HENRY_BOOK
where TYPE = "TRA";

select
select BOOK_CODE,
        TITLE,
        PRICE,
        PUBLISHER_CODE
from HENRY_BOOK
where PUBLISHER_CODE = "JP";

select book.PUBLISHER_CODE,
        PUBLISHER_NAME
from HENRY_PUBLISHER publisher
        join HENRY_BOOK book on publisher.PUBLISHER_CODE = book.PUBLISHER_CODE;