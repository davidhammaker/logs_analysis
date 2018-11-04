#!/usr/bin/env python3
"""
This code performs an analysis on a database of HTTP request logs on from a
news website. The code uses psycopg2 as its PostgreSQL adapter. The code
contains three functions, each of which performs a single SQL query. The
results of these queries are printed to the console and to a text file.
"""

import psycopg2


def first_query():
    """
    Answer the following question:
        "What are the most popular three articles of all time?"

    Return:
        A list of three tuples, each of which contains the name of an article
        and its total number of views, listed in descending order.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    q = '''
        select articles.title, count(*) as total
            from log, articles
            where log.path = concat('/article/', articles.slug)
            group by articles.id
            order by total desc
            limit 3;
        '''
    c.execute(q)
    result = c.fetchall()
    db.close()
    return result


def second_query():
    """
    Answer the following question:
        "Who are the most popular article authors of all time?"

    Return:
        A list of tuples, each of which contains the name of an author and
        his/her total number of views, listed in descending order.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    q = '''
        select authors.name, count(*) as total
            from authors, log, articles
            where log.path = concat('/article/', articles.slug)
            and authors.id = articles.author
            group by authors.id
            order by total desc;
        '''
    c.execute(q)
    result = c.fetchall()
    db.close()
    return result


def third_query():
    """
    Answer the following question:
        "On which days did more than 1% of requests lead to errors?"

    Return:
        A list of tuples, each of which contains a timestamp with time zone
        (truncated to the day) and a number (class 'decimal.Decimal')
        representing the percentage (rounded to the nearest 10th's place),
        listed in descending order.
    """
    db = psycopg2.connect("dbname=news")
    c = db.cursor()
    q = '''
        select total_log.date,
            round(1.0*error_log.errors/total_log.total*100, 1)
            from
            (select date_trunc('day', time) as date,
                    count(*) as errors
                from log
                where status = '404 NOT FOUND'
                group by date) as error_log
            join
            (select date_trunc('day', time) as date,
                    count(*) as total
                from log
                group by date) as total_log
            on error_log.date = total_log.date
            where round(1.0*error_log.errors/total_log.total*100, 1) > 1
            order by round(1.0*error_log.errors/total_log.total*100, 1) desc;
        '''
    c.execute(q)
    result = c.fetchall()
    db.close()
    return result


if __name__ == '__main__':
    q1 = first_query()
    q2 = second_query()
    q3 = third_query()

    # Answer question 1

    # Set up a list which will contain lines for answer 1
    answer_1_list = ['Answer 1:']

    # Define lengths to use in sizing the table of results
    max_article_length = 0
    max_view_length = 0
    for row in q1:
        if max_article_length < len(row[0]):
            max_article_length = len(row[0])
        if max_view_length < (len(str(row[1]))):
            max_view_length = (len(str(row[1])))

    # Format the title line and line break
    answer_1_list.append('   Article' +
                         ' ' * (max_article_length - 4) +
                         '|   Views')
    answer_1_list.append('-' * (max_article_length + 6) +
                         '+' +
                         '-' * (max_view_length + 6))

    # Format line data
    for row in q1:
        line = ('   ' +
                row[0] +
                ' ' * (max_article_length - len(row[0])) +
                '   |   ' +
                str(row[1]))
        answer_1_list.append(line)

    # Join and print final answer 1 table
    answer_1 = '\n'.join(answer_1_list)
    print(answer_1)

    # Answer question 2

    # Set up a list which will contain lines for answer 2
    answer_2_list = ['Answer 2:']

    # Define lengths to use in sizing the table of results
    max_author_length = 0
    max_view2_length = 0
    for row in q2:
        if max_author_length < len(row[0]):
            max_author_length = len(row[0])
        if max_view2_length < (len(str(row[1]))):
            max_view2_length = (len(str(row[1])))

    # Format the title line and line break
    answer_2_list.append('   Author' +
                         ' ' * (max_author_length - 3) +
                         '|   Views')
    answer_2_list.append('-' * (max_author_length + 6) +
                         '+' +
                         '-' * (max_view2_length + 6))

    # Format line data
    for row in q2:
        line = ('   ' +
                row[0] +
                ' ' * (max_author_length - len(row[0])) +
                '   |   ' +
                str(row[1]))
        answer_2_list.append(line)

    # Join and print final answer 2 table
    answer_2 = '\n'.join(answer_2_list)
    print(answer_2)

    # Answer question 3

    # Set up a list which will contain lines for answer 3
    answer_3_list = ['Answer 3:']

    # Define list for holding dates and percentages
    dates_and_percentages = []

    # Parse dates and percentages
    for row in q3:

        # Parse date
        date_num = str(row[0])
        year = date_num[:4]
        month_num = int(date_num[5:7])
        month = ('January',
                 'February',
                 'March',
                 'April',
                 'May',
                 'June',
                 'July',
                 'August',
                 'September',
                 'October',
                 'November',
                 'December')[month_num - 1]
        day = int(date_num[8:10])
        date = month + ' ' + str(day) + ', ' + year

        # Convert percentage to string type
        percentage = str(row[1])

        dates_and_percentages.append((date, percentage))

    # Define length to use in sizing the table of results
    max_date_length = 0
    for pair in dates_and_percentages:
        if max_date_length < len(pair[0]):
            max_date_length = len(pair[0])

    # Construct lines for Answer 3
    answer_3_list.append('   Date' +
                         ' ' * (max_date_length - 1) +
                         '|   Percentage')
    answer_3_list.append('-' * (max_date_length + 6) +
                         '+' +
                         '-' * 16)
    for pair in dates_and_percentages:
        line = ('   ' +
                pair[0] +
                ' ' * (max_date_length - len(pair[0])) +
                '   |   ' +
                pair[1])
        answer_3_list.append(line)

    # Join and print final answer 3 table
    answer_3 = '\n'.join(answer_3_list)
    print(answer_3)
