CREATE DATABASE IF NOT EXISTS author_db;
USE author_db;
CREATE TABLE IF NOT EXISTS Author(
    authorID INT AUTO_INCREMENT PRIMARY KEY,
    authorName VARCHAR(100)
);
INSERT INTO Author (authorName) VALUES ('a'), ('b'), ('c');

CREATE DATABASE IF NOT EXISTS book_db;
USE book_db;
CREATE TABLE IF NOT EXISTS Book(
    bookID INT AUTO_INCREMENT PRIMARY KEY,
    bookName VARCHAR(100)
);
INSERT INTO Book (bookName) VALUES ('A'), ('B'), ('C');

