# Project: Logs Analysis

This project is the first of three projects in the Udacity Full Stack Web Developer Nanodegree program. The goal of the project is "to build an **internal reporting tool**" for gathering information about user activity from a site database.

## Functionality

The reporting tool answers the following three questions:

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

The reporting tool works inside a Linux-based virtual machine. The tool prints plain text to the console within the virtual machine, answering the three questions based on the data within the provided database, `news`.

The reporting tool does not employ the use of _views_.

## Usage

Follow these steps to set up the database and reporting tool, and then run the reporting tool.

### Prepare the Database

The project works in conjunction with the `news` database which Udacity provides. This project also employs a Linux-based virtual machine by using Vagrant and VirtualBox. If you do not have access to `news`, download `newsdata.sql` from Udacity's "Project: Logs Analysis" and (using the virtual machine) run `$ psql -d news -f newsdata.sql` from the `vagrant` directory.

### Prepare the Reporting Tool

Clone the `logs_analysis` repository to a directory which your virtual machine may access. The best place is within the `vagrant` directory (see _Prepare the Database_). Ensure that the virtual machine may also access `news` from this directory. To test this, `cd` into the cloned `logs_analysis` directory and run `$ psql -d news`. If you successfully access the database (I.e. you see `news=>` in your console), then the reporting tool will function properly. If you are in the `logs_analysis` directory and cannot, check that your `logs_analysis` directory is within the `vagrant` directory, and ensure that you properly followed the steps listed in _Prepare the Database_.

### Run the Reporting Tool

After preparing the database and reporting tool, `cd` into the `logs_analysis` directory and run `$ python 3 logs_analysis.py`. The tool will run three `select` queries and print the answers to the console.

## Design

The reporting tool runs three `select` queries, each of which answers one question.

The first query answers the question, _What are the most popular three articles of all time?_
* The query selects the titles of the articles and the `total` rows for each article title. The query selects this data from the tables `articles` and `log`. These two tables are joined by comparing `log.path` to the concatenation of `/article/` and `articles.slug`, since the only difference between the values of these two columns is the string, `/article/`. This concatenation also excludes any invalid path. The query groups rows by article title and orders rows by `total` in descending order. The query limits the results to 3 rows.

The second query answers the question, _Who are the most popular article authors of all time?_
* The query selects author names and `total` rows for each unique author id number. The query selects this data from all three tables: `log`, `articles`, and `authors`. Like the first query, `articles` and `log` are joined by comparing `log.path` to `articles.slug`. Additionally, `authors` is joined to `articles` by comparing `authors.id` to `articles.author`, both of which are unique integers per author. Rows are grouped by unique author id numbers. Like the first query, this query orders its results by `total` rows in descending order.

The third query answers the question, _On which days did more than 1% of requests lead to errors?_
* The query joins two subqueries. The first subquery selects the date (truncating the timestamp to the day) and the count of all requests errors per each date, grouping rows by truncated date. The second subquery selects the date (also truncating the timestamp) and the count of all requests, also grouping by truncated date. Both subqueries select from the `log` table. The query joins the subqueries by date.
* From the joined subqueries, the query selects the truncated date and the error percentage. The query calculates the error percentage using the following formula:
    1. Multiply the count of all request errors by 1.0 to convert the type from an integer to a float-like type.
    2. Divide the count of all request errors by the total number of requests.
    3. Multiply the quotient of step 2 by 100 to get a percentage.
    4. Round the product of steps 1-3 to 1 decimal place.
* The query only selects error percentages greater than 1. The query orders rows by date.

The Python source code, `logs_analysis.py`, runs each of the three queries in a separate function. The code runs all three functions in sequence, storing the results as separate named references. The code parses the results (answers) and joins the parsed data together in strings. The code the code also creates strings that contain brief titles for each of the answers, then joins the title and answer strings together into one string, which the code prints to the console.

## Copyright

Copyright David J. Hammaker 2018
