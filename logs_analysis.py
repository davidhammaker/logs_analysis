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
        (truncated to the day) and a number representing the percentage
        (rounded to the nearest 10th's place), listed in descending order.
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
