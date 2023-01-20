def generate_filled_circle_points(radius=5):
    """returns list of points of filled circle (centered at 0,0) for given radius"""
    def belongs_to_circle(x, y):
        return x**2 + y**2 <= radius**2 + 1

    points = []

    for y in range(-radius, radius + 1):
        for x in range(-radius, radius + 1):
            if belongs_to_circle(x, y):
                points.append((x, y))

    return points
