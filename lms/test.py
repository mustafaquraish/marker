import canvas

config = {
    'base_url': "https://q.utoronto.ca",
    'course_id': 160057,
    'assgn_id': 343885,
}

canvas = canvas.Canvas(config)
print(canvas.students())
