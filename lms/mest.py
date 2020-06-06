import markus

config = {
    'base_url': "https://markus.utsc.utoronto.ca/cscb09s20/",
    # 'course_id': "L03",
    'assgn_id': "L03",
}

markus = markus.Markus(config)
print(markus.get_groups())
