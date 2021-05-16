"""
tools for creating bezier curves
"""


def bezier(*coords, precision=100):
    """creates a bezier using recursive calculations"""

    def get_coord(delta, *lerp_from):
        """brute-forces a coordinate by lerping each set of lines until none are left"""
        lerped = []
        for i in range(len(lerp_from) - 1):
            p_0, p_1 = lerp_from[i], lerp_from[i + 1]
            lerped.append((p_0 + (p_1 - p_0) * delta).round(int_cast=True))
        return lerped[0] if len(lerped) == 1 else get_coord(delta, *lerped)

    return [get_coord(step / precision, *coords) for step in range(1, precision)]
