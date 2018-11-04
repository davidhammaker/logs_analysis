#!/usr/bin/env python3
"""

"""

import psycopg2


def first_query():
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