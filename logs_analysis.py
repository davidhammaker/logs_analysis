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
            order by total
            desc limit 3;
        '''
    c.execute(q)
    result = c.fetchall()
    db.close()
    return result

print(first_query())
