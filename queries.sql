select articles.title, count(*) as total from log, articles where log.path = concat('/article/', articles.slug) group by articles.title order by total desc limit 3;
