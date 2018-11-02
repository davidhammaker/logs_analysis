select articles.title, count(*) as total
    from log, articles
    where log.path = concat('/article/', articles.slug)
    group by articles.title
    order by total
    desc limit 3;

select authors.name, count(*) as total
    from authors, log, articles
    where log.path = concat('/article/', articles.slug)
    and authors.id = articles.author
    group by authors.id
    order by total desc
    limit 3;
