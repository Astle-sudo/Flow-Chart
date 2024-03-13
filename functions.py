def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + word + ' '
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + ' '
    lines.append(current_line)
    return lines


def generate_list(N, stepsize):
    return [i * stepsize for i in range(N)]

def bounds(points, width, height): 
    for point in points :
       point[0] = (point[0] + width) % width
       point[1] = (point[1] + height) % height
    return points




