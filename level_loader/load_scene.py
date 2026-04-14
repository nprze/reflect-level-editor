def extract_rectangles(scene_text: str):
    rectangles = []

    lines = scene_text.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if line.startswith("Rect:"):
            # Parse color
            color_line = lines[i + 1].strip()
            color = color_line.split(":")[1].strip()

            # Parse min
            min_line = lines[i + 2].strip()
            min_vals = min_line.split("(")[1].split(")")[0]
            min_x, min_y = map(int, min_vals.split(","))

            # Parse max
            max_line = lines[i + 3].strip()
            max_vals = max_line.split("(")[1].split(")")[0]
            max_x, max_y = map(int, max_vals.split(","))

            # Compute extent
            width = max_x - min_x
            height = max_y - min_y

            rectangles.append({
                "color": color,
                "min": (min_x, min_y),
                "extent": (width, height)
            })

            i += 4  # skip parsed block
        else:
            i += 1

    return rectangles