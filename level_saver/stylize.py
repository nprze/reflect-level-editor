import numpy as np
from PIL import Image
import svgwrite
import math
import matplotlib.pyplot as plt
import random
from shapely.geometry import Polygon, Point, polygon
from scipy.spatial import Delaunay
from shapely.ops import nearest_points
import cv2
import os
import re


def plot_point_list(point_list, lines=True):
    x_coords, y_coords = zip(*point_list)
    if lines:
        plt.plot(x_coords, y_coords, marker='o')
    else:
        plt.scatter(x_coords, y_coords, marker='o')

def plot_triangulation(points, delaunay):
    points_array = np.array(points)
    plt.triplot(points_array[:, 0], points_array[:, 1], delaunay.simplices, color='blue')
    plt.scatter(points_array[:, 0], points_array[:, 1], color='red')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Delaunay Triangulation')
    plt.show()

def plot_triangles(triangle_list):
    """Plot a list of triangles."""
    fig, ax = plt.subplots()
    for triangle in triangle_list:
        x_coords = [pt[0] for pt in triangle] + [triangle[0][0]]
        y_coords = [pt[1] for pt in triangle] + [triangle[0][1]]
        ax.plot(x_coords, y_coords, marker='o')
    ax.set_aspect('equal')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)
    plt.show()

def plot_triangles_and_quadrangles(triangles, quadrangles):
    """Plot both triangles and quadrangles on the same figure."""
    fig, ax = plt.subplots()
    for triangle in triangles:
        x_coords = [pt[0] for pt in triangle] + [triangle[0][0]]
        y_coords = [pt[1] for pt in triangle] + [triangle[0][1]]
        ax.plot(x_coords, y_coords, color='blue')
    for quad in quadrangles:
        x_coords = [pt[0] for pt in quad] + [quad[0][0]]
        y_coords = [pt[1] for pt in quad] + [quad[0][1]]
        ax.plot(x_coords, y_coords, color='green')
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.set_title('Triangles and Merged Quadrangles')
    plt.show()

def generate_circumference_points(image, generate_corner = True):
    """Generate ordered boundary and corner points from an image's alpha channel."""
    def generate_corner_points(image):
        alpha_channel = image[:, :, 3]
        _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return []
        contour = max(contours, key=cv2.contourArea)
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        return [tuple(pt[0]) for pt in approx]

    def sort_points_clockwise(points):
        center = np.mean(points, axis=0)
        return sorted(points, key=lambda pt: np.arctan2(pt[1] - center[1], pt[0] - center[0]))

    alpha_channel = image[:, :, 3]
    _, binary = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if not contours:
        return []
    contour = max(contours, key=cv2.contourArea)[:, 0, :]
    total_points = len(contour)
    if total_points == 0:
        return []
    num_points = total_points // 40
    step = max(1, total_points // num_points)
    selected_points = [tuple(contour[i]) for i in range(0, total_points, step)][:num_points]
    if (generate_corner):
        corner_points = generate_corner_points(image)
        all_points = list(set(selected_points + corner_points))
    else:
        all_points = selected_points
    return sort_points_clockwise(all_points)

def generate_rectangle_perimeter_points(width, height, n, fluctuate = 10):
    # Perimeter length of the rectangle
    perimeter = 2 * (width + height)

    # Compute number of points, including corners
    num_points = max(4, math.floor(perimeter / n))
    actual_spacing = perimeter / num_points  # Adjusted spacing to distribute evenly

    points = []
    edges = [
        ((0, 0), (width, 0)),         # Bottom edge
        ((width, 0), (width, height)), # Right edge
        ((width, height), (0, height)), # Top edge
        ((0, height), (0, 0))          # Left edge
    ]

    remaining = actual_spacing
    current_point = [0.0, 0.0]

    for start, end in edges:
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)

        direction = (dx / length if length != 0 else 0, dy / length if length != 0 else 0)

        edge_pos = 0
        while edge_pos + remaining <= length:
            px = start[0] + direction[0] * (edge_pos + remaining) + (direction[0] * (random.randint(-(fluctuate//2), fluctuate//2)))
            py = start[1] + direction[1] * (edge_pos + remaining) + (direction[1] * (random.randint(-(fluctuate//2), fluctuate//2)))
            if not (px * py < 0):
                points.append((round(px, 6), round(py, 6)))
            edge_pos += remaining
            remaining = actual_spacing
        remaining -= (length - edge_pos)

    # Ensure all 4 corners are present
    corners = [(0, 0), (width, 0), (width, height), (0, height)]
    for corner in corners:
        if corner not in points:
            points.insert(0, corner)

    def sort_points_clockwise(points):
        center = np.mean(points, axis=0)
        return sorted(points, key=lambda pt: np.arctan2(pt[1] - center[1], pt[0] - center[0]))
    points = sort_points_clockwise(list(set(points)))
    return points

def add_edge_points_to_polygon(polygon, points_per_segment):
    """Add evenly spaced points between polygon vertices."""
    points_per_segment = int(points_per_segment)
    if points_per_segment < 0:
        raise ValueError("The number of points per segment must be non-negative.")

    new_points = []
    for i in range(len(polygon)):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % len(polygon)]
        new_points.append((x1, y1))
        for j in range(1, points_per_segment + 1):
            t = j / (points_per_segment + 1)
            x_new = x1 + t * (x2 - x1)
            y_new = y1 + t * (y2 - y1)
            new_points.append((x_new, y_new))
    return new_points

def generate_random_points_in_polygon(vertices, num_points_multiplier=3, min_distance=10):
    polygon = Polygon(vertices)
    num_points = num_points_multiplier * len(vertices)
    generated_points = []

    def is_valid_point(point, existing_points, min_dist, polygon):
        point_obj = Point(point)

        # Check distance from existing points
        for p in existing_points:
            if Point(p).distance(point_obj) < min_dist:
                return False

        # Check distance from polygon edges
        nearest_point_on_edge = nearest_points(polygon.exterior, point_obj)[0]
        if point_obj.distance(nearest_point_on_edge) < min_dist:
            return False

        # Check distance from polygon vertices
        for vertex in polygon.exterior.coords:
            if point_obj.distance(Point(vertex)) < min_dist:
                return False

        return True

    attempts = 0
    max_attempts = num_points * 100

    while len(generated_points) < num_points and attempts < max_attempts:
        attempts += 1
        min_x, min_y, max_x, max_y = polygon.bounds
        random_point = (random.uniform(min_x, max_x), random.uniform(min_y, max_y))
        point_obj = Point(random_point)

        if polygon.contains(point_obj) and is_valid_point(random_point, generated_points, min_distance, polygon):
            generated_points.append(random_point)

    return generated_points

def triangulate_points(points):
    points_array = np.array(points)

    # Perform Delaunay triangulation
    delaunay = Delaunay(points_array)

    # Extract the triangles as a list of point tuples
    triangles = []
    for simplex in delaunay.simplices:
        triangles.append(tuple(points_array[simplex]))

    return triangles, delaunay

def combine_triangles_to_quadrangles(x, triangles):
    def shared_edge(triangle1, triangle2):
        triangle1 = np.array(triangle1)
        triangle2 = np.array(triangle2)

        def sort_edge(edge):
            return tuple(sorted([tuple(edge[0]), tuple(edge[1])]))

        edges1 = [
            sort_edge([triangle1[0], triangle1[1]]),
            sort_edge([triangle1[1], triangle1[2]]),
            sort_edge([triangle1[2], triangle1[0]])
        ]
        edges2 = [
            sort_edge([triangle2[0], triangle2[1]]),
            sort_edge([triangle2[1], triangle2[2]]),
            sort_edge([triangle2[2], triangle2[0]])
        ]

        for edge1 in edges1:
            if edge1 in edges2:
                return edge1
        return None

    def is_colinear(p1, p2, p3, tol=1e-8):
        # Check if three points are colinear using the area of triangle method
        return abs(0.5 * ((p1[0]*(p2[1]-p3[1]) +
                           p2[0]*(p3[1]-p1[1]) +
                           p3[0]*(p1[1]-p2[1])))) < tol

    quadrangles = []
    remaining_triangles = triangles[:]

    for _ in range(x):
        if not remaining_triangles:
            break

        tri1 = random.choice(remaining_triangles)
        remaining_triangles = [tri for tri in remaining_triangles if not np.array_equal(tri, tri1)]

        found = False
        for i in range(3):
            edge = (tuple(tri1[i]), tuple(tri1[(i + 1) % 3]))

            for tri2 in remaining_triangles:
                if shared_edge(tri1, tri2) == tuple(sorted(edge)):
                    # Combine and get unique points
                    points = list(set(tuple(pt) for pt in (tri1 + tri2)))
                    if len(points) != 4:
                        continue  # Not a quadrilateral

                    # Check for colinearity in all combinations of 3 points
                    is_degenerate = any(
                        is_colinear(p1, p2, p3)
                        for idx1, p1 in enumerate(points)
                        for idx2, p2 in enumerate(points)
                        for idx3, p3 in enumerate(points)
                        if len({idx1, idx2, idx3}) == 3
                    )
                    if is_degenerate:
                        continue

                    # Sort the quadrilateral points by angle around the centroid
                    centroid_x = sum(x for x, y in points) / 4
                    centroid_y = sum(y for x, y in points) / 4

                    def angle_from_centroid(point):
                        x, y = point
                        return math.atan2(y - centroid_y, x - centroid_x)

                    sorted_points = sorted(points, key=angle_from_centroid)
                    quadrangles.append(sorted_points)
                    remaining_triangles = [tri for tri in remaining_triangles if not np.array_equal(tri, tri2)]
                    found = True
                    break
            if found:
                break
        if not found:
            remaining_triangles.append(tri1)

    return quadrangles, remaining_triangles


def scale_shapes(triangles, quadrangles, x):
    def centroid(points):
        """Calculate the centroid of a list of points."""
        return np.mean(points, axis=0)

    def scale_shape(shape, x):
        """Scale the vertices of a shape (triangle or quadrangle) inward by x."""
        shape_centroid = centroid(shape)
        scaled_shape = []

        for vertex in shape:
            direction = shape_centroid - vertex
            distance = np.linalg.norm(direction)

            if distance > 0:  # Avoid division by zero
                scaled_vertex = vertex + (x / distance) * direction
            else:
                scaled_vertex = vertex  # No scaling needed for zero-distance

            scaled_shape.append(scaled_vertex)

        return tuple(scaled_shape)

    scaled_triangles = [scale_shape(triangle, x) for triangle in triangles]
    scaled_quadrangles = [scale_shape(quadrangle, x) for quadrangle in quadrangles]

    return scaled_triangles, scaled_quadrangles

def separate_shapes(quads, triangles, spacing):
    def get_centroid(points):
        """Calculate the centroid (center of mass) of the points."""
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        return (sum(x_coords) / len(points), sum(y_coords) / len(points))

    def angle_from_centroid(point, centroid):
        """Calculate the angle of the point relative to the centroid."""
        dx = point[0] - centroid[0]
        dy = point[1] - centroid[1]
        return math.atan2(dy, dx)

    def get_edges(points):
        if len(points) != 4:
            raise ValueError("Exactly 4 points are required")

        # Step 1: Find the centroid of the points
        centroid = get_centroid(points)

        # Step 2: Sort points based on their angle relative to the centroid
        sorted_points = sorted(points, key=lambda p: angle_from_centroid(p, centroid))

        # Step 3: Create edges by pairing adjacent points
        edges = []
        for i in range(4):
            edge = (sorted_points[i], sorted_points[(i + 1) % 4])
            edges.append(edge)

        return edges

    def get_line_intersection(p1, p2, q1, q2):
        # Unpack points
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = q1
        x4, y4 = q2

        # Calculate the denominator (determinant of the system)
        denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # If denominator is 0, lines are parallel and do not intersect
        if denom == 0:
            return None

        # Calculate the intersection point using Cramer's rule
        t_num = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        u_num = (x1 - x3) * (y1 - y2) - (y1 - y3) * (x1 - x2)

        t = t_num / denom
        u = u_num / denom

        # Compute the intersection point
        intersect_x = x1 + t * (x2 - x1)
        intersect_y = y1 + t * (y2 - y1)

        # Return the intersection point, whether it lies on the segments or extensions
        return (intersect_x, intersect_y)

    def move_edge_inward_triangle(triangle, edge_indices, x):
        # Extract vertices
        P1 = np.array(triangle[edge_indices[0]])  # One point of the edge
        P2 = np.array(triangle[edge_indices[1]])  # Other point of the edge
        fixed_vertex = np.array(triangle[3 - sum(edge_indices)])  # Vertex not in the edge

        # Compute the inward direction (unit vector perpendicular to the edge)
        edge_vector = P2 - P1
        edge_length = np.linalg.norm(edge_vector)
        unit_edge_vector = edge_vector / edge_length
        perp_vector = np.array([-unit_edge_vector[1], unit_edge_vector[0]])

        # Move the edge inward by distance x along the perpendicular direction
        P1_new = P1 + x * perp_vector
        P2_new = P2 + x * perp_vector

        # Get the intersection points of the inwardly moved edge with lines through the fixed vertex
        i_P1 = get_line_intersection(fixed_vertex, P1, P1_new, P2_new)
        i_P2 = get_line_intersection(fixed_vertex, P2, P1_new, P2_new)

        # Rebuild the new triangle while maintaining the input order
        if edge_indices == [0, 1]:
            new_triangle = [i_P1, i_P2, fixed_vertex]
        elif edge_indices == [1, 2]:
            new_triangle = [fixed_vertex, i_P1 , i_P2]
        else:  # edge_indices == [0, 2]
            new_triangle = [i_P1, fixed_vertex, i_P2]

        return new_triangle


    def move_all_triange_edges_inward(triangle, x):
        mod_triangle = triangle
        for i in range(3):
            index0 = i
            index1 = (i + 1)%3
            mod_triangle = move_edge_inward_triangle(mod_triangle, [index0, index1], x)
        return mod_triangle

    def compare_points (p1,p2):
        return p1[0] == p2[0] and p1[1] == p2[1]
    def move_edge_inward_quad(quad_points, edge_indices, x):
        edges = get_edges(quad_points)
        # Extract the quadrilateral vertices
        P1 = np.array(quad_points[edge_indices[0]])  # One point of the edge
        P2 = np.array(quad_points[edge_indices[1]])  # Other point of the edge
        fixed_vertices = []
        first_fixed_point = []
        second_fixed_point = []
        for edge in edges:
            if  (compare_points(edge[0], P1) and not compare_points(edge[1],P2)):
                first_fixed_point = edge[1]
            else:
                if (compare_points(edge[1], P1) and not compare_points(edge[0],P2)):
                    first_fixed_point = edge[0]
            if  (compare_points(edge[0], P2) and not compare_points(edge[1],P1)) :
                second_fixed_point = edge[1]
            else:
                if (compare_points(edge[1], P2) and not compare_points(edge[0], P1)):
                    second_fixed_point = edge[0]
        fixed_vertices = [first_fixed_point, second_fixed_point]

        # Compute the inward direction (unit vector perpendicular to the edge)
        edge_vector = P2 - P1
        edge_length = np.linalg.norm(edge_vector)
        unit_edge_vector = edge_vector / edge_length
        perp_vector = np.array([-unit_edge_vector[1], unit_edge_vector[0]])

        # Move the edge inward by distance x along the perpendicular direction
        P1_new = P1 + x * perp_vector
        P2_new = P2 + x * perp_vector

        # Get the intersection points of the inwardly moved edge with lines through the fixed points
        i_P1 = get_line_intersection(fixed_vertices[0], P1, P1_new, P2_new)
        i_P2 = get_line_intersection(fixed_vertices[1], P2, P1_new, P2_new)

        # Rebuild the quadrilateral based on the edge_indices
        # We will use fixed vertices as anchors, and make sure the new points are inserted in the correct places.

        # To handle any order of the edge, we'll check how the fixed vertices map to the input quad
        if edge_indices == [0, 1]:
            new_quad = [i_P1, i_P2, fixed_vertices[1], fixed_vertices[0]]
        elif edge_indices == [1, 2]:
            new_quad = [fixed_vertices[0], i_P1, i_P2, fixed_vertices[1]]
        elif edge_indices == [2, 3]:
            new_quad = [fixed_vertices[1], fixed_vertices[0], i_P1, i_P2]
        elif edge_indices == [3,0]:
            new_quad = [i_P1, fixed_vertices[0], fixed_vertices[1], i_P2]
        return new_quad

    def move_all_quad_edges_inward(quad, x):
        mod_quad = quad
        for i in range(4):
            index0 = i
            index1 = (i + 1)%4
            if (any(q is None for q in mod_quad)):
                return None
            mod_quad = move_edge_inward_quad(mod_quad, [index0, index1], x)
        return mod_quad

    '''
    original_triangle = [(0, 2), (4, 0), (4,4), (3,2)]
    selected_edge = [3, 0]
    x_distance = 0.5

    new_triangle = move_all_quad_edges_inward(original_triangle, x_distance)
    x_coords, y_coords = zip(*original_triangle)
    plt.plot(x_coords, y_coords, color='red')
    x_coords1, y_coords1 = zip(*new_triangle)
    plt.plot(x_coords1, y_coords1, color='blue')
    plt.show()'''

    def process_polygons(triangles, quads, x):
        modified_triangles = []
        modified_quads = []

        # Process all triangles
        for triangle in triangles:
            new_triangle = move_all_triange_edges_inward(triangle, x)
            modified_triangles.append(new_triangle)

        # Process all quads
        for quad in quads:
            new_quads = move_all_quad_edges_inward(quad, x)
            if not (new_quads is None):
                modified_quads.append(new_quads)

        return modified_triangles, modified_quads
    return process_polygons(triangles, quads, spacing)

def create_svg(polygon, quads, tris, image, output_path, color_in = (100,200,50), color_fluctuate = 30):
    def centroid(points):
        return np.mean(points, axis=0)

    """Create an SVG file with the polygon and center color."""
    dwg = svgwrite.Drawing(output_path, profile='tiny')

    points = [(float(x), float(y)) for x,y in polygon]
    shape_centroid = centroid(points)

    shape = np.array(polygon)
    outline = []
    n = len(shape)

    for i in range(n):
        p1 = shape[i]
        p2 = shape[(i + 1) % n]

        # Compute edge direction and normal
        edge = p2 - p1
        normal = np.array([-edge[1], edge[0]])  # Rotate 90 degrees
        normal = normal / np.linalg.norm(normal) * 4  # Normalize and scale

        # Offset both points outward
        outline.append(tuple(p1 + normal))
        outline.append(tuple(p2 + normal))

    dwg.add(dwg.polygon(points=outline, fill=svgwrite.rgb(0,0,0, '%')))

    def getNicelyFormatted(traingleOrQued):
        final = ""
        for i in traingleOrQued:
            final += str(i[0]) + " " + str(i[1]) + "\n"
        return final
    for triangle in tris:
        # Ensure the triangle has exactly 3 points
        if len(triangle) == 3:
            centroid_triangle = centroid(triangle)
            if (image is None):
                color = color_in
            else:
                color = image[int(centroid_triangle[1]), int(centroid_triangle[0])][:3]
            fluctuate = random.randint(-color_fluctuate, color_fluctuate)

            color_with_fluctuate = [
                max(0, min(255, int(c) + fluctuate)) for c in color
            ]
            dwg.add(dwg.polygon(triangle, fill=svgwrite.rgb(*color_with_fluctuate)))
            coords = getNicelyFormatted(triangle)

        # Add quadrangles to the drawing
    def quad_to_triangles(quad):
        if len(quad) != 4:
            raise ValueError("Input must be a list of 4 points representing a quadrangle.")

        p1, p2, p3, p4 = quad

        triangle1 = (p1, p2, p3)
        triangle2 = (p1, p3, p4)

        return [triangle1, triangle2]
    for quadrangle in quads:
        # Ensure the quadrangle has exactly 4 points
        if len(quadrangle) == 4:
            centroid_quadrangle = centroid(quadrangle)
            if (image is None):
                color = color_in
            else:
                color = image[int(centroid_quadrangle[1]), int(centroid_quadrangle[0])][:3]
            fluctuate = random.randint(-color_fluctuate, color_fluctuate)

            color_with_fluctuate = [
                max(0, min(255, int(c) + fluctuate)) for c in color
            ]

            dwg.add(dwg.polygon(quadrangle, fill=svgwrite.rgb(*color_with_fluctuate)))
            tris = quad_to_triangles(quadrangle)

    dwg.save()

def get_color(width, height, centroid, color_fluc):
    def distance_to_aabb_edge(point, min_corner, max_corner):
        px, py = point
        min_x, min_y = min_corner
        max_x, max_y = max_corner

        # Clamp the point to the AABB
        clamped_x = min(max(px, min_x), max_x)
        clamped_y = min(max(py, min_y), max_y)

        if min_x <= px <= max_x and min_y <= py <= max_y:
            # Point is inside the AABB
            dist_left = px - min_x
            dist_right = max_x - px
            dist_bottom = py - min_y
            dist_top = max_y - py
            return min(dist_left, dist_right, dist_bottom, dist_top)
        else:
            # Point is outside AABB, compute distance to the closest edge
            dx = max(min_x - px, 0, px - max_x)
            dy = max(min_y - py, 0, py - max_y)
            if dx == 0:
                return dy
            elif dy == 0:
                return dx
            else:
                return (dx ** 2 + dy ** 2) ** 0.5
    #fluctuate = random.randint(-color_fluc, color_fluc)
    x = max(0, min(35, distance_to_aabb_edge(centroid, (0,0), (width * 70, height * 70))))
    fluct = random.randint(-2000, 2000)/10000
    val = (1 - (x / 35) * 0.75)+fluct
    return max((min(val, 1.)), 0.3)



def create_txt(polygon, quads, tris, image, output_path, output_folder, width, height, color_in = (100,200,50), color_fluctuate = 30):
    if (output_path == ""):
        output_path = str(width) + "x" + str(height) +".txt"
    file_path = os.path.join(output_folder, output_path)
    os.makedirs(output_folder, exist_ok=True)
    with open(file_path, 'w') as f:
        def centroid(points):
            return np.mean(points, axis=0)


        points = [(float(x), float(y)) for x,y in polygon]
        shape_centroid = centroid(points)

        shape = np.array(polygon)
        outline = []
        n = len(shape)

        for i in range(n):
            p1 = shape[i]
            p2 = shape[(i + 1) % n]

            # Compute edge direction and normal
            edge = p2 - p1
            normal = np.array([-edge[1], edge[0]])  # Rotate 90 degrees
            normal = normal / np.linalg.norm(normal) * 4  # Normalize and scale

            # Offset both points outward
            outline.append(tuple(p1 + normal))
            outline.append(tuple(p2 + normal))

        def getNicelyFormatted(traingleOrQued):
            final = ""
            for i in traingleOrQued:
                final += str(i[0]) + " " + str(i[1]) + "\n"
            return final
        for triangle in tris:
            # Ensure the triangle has exactly 3 points
            if len(triangle) == 3:
                centroid_triangle = centroid(triangle)
                color_with_fluctuate = get_color(width, height, centroid_triangle, color_fluctuate)
                coords = getNicelyFormatted(triangle)
                f.write(f"{coords}{color_with_fluctuate}\n")

            # Add quadrangles to the drawing
        def quad_to_triangles(quad):
            if len(quad) != 4:
                raise ValueError("Input must be a list of 4 points representing a quadrangle.")

            p1, p2, p3, p4 = quad

            triangle1 = (p1, p2, p3)
            triangle2 = (p1, p3, p4)

            return [triangle1, triangle2]
        for quadrangle in quads:
            # Ensure the quadrangle has exactly 4 points
            if len(quadrangle) == 4:
                centroid_quadrangle = centroid(quadrangle)
                color_with_fluctuate = get_color(width, height, centroid_quadrangle, color_fluctuate)

                tris = quad_to_triangles(quadrangle)
                coords = getNicelyFormatted(tris[0])
                coords2 = getNicelyFormatted(tris[1])
                f.write(f"{coords}{coords2}{color_with_fluctuate} \n")


def filter_triangles(triangles, width, height):

    def is_inside(vertex):
        x, y = vertex
        return 0 <= x <= width and 0 <= y <= height

    filtered = []
    for tri in triangles:
        if all(is_inside(v) for v in tri):
            filtered.append(tri)
    return filtered

def filter_triangles_inside_polygon(triangles, polygon_vertices):
    polygon = Polygon(polygon_vertices)
    filtered_triangles = []

    for triangle in triangles:
        triangle_polygon = Polygon(triangle)

        # Check if the triangle is fully inside the polygon
        if polygon.contains(triangle_polygon):
            filtered_triangles.append(triangle)

    return filtered_triangles

def scale_shape(shapes, scale):
    scaled_triangles = [
        tuple(tuple(v * scale for v in vertex) for vertex in triangle)
        for triangle in shapes
    ]
    return scaled_triangles


def filter_shapes_outside_bbox(shapes, min_coord, max_coord):
    x_min, y_min = min_coord
    x_max, y_max = max_coord

    def is_fully_inside(shape):
        return all(x_min <= x <= x_max and y_min <= y <= y_max for (x, y) in shape)

    # Keep only the shapes that are NOT fully inside the bounding box
    return [shape for shape in shapes if not is_fully_inside(shape)]


def low_poly_vectorize(input_path, distance_between_points_arg, points_min_distance, output_path, generate_corner):
    """Main function to vectorize the object in the PNG image."""
    image_array = np.array(Image.open(input_path).convert("RGBA"))
    polygon = generate_circumference_points(image_array, generate_corner)
    points = generate_random_points_in_polygon(polygon,5,points_min_distance)
    points_with_edge_points = add_edge_points_to_polygon(polygon, distance_between_points_arg/points_min_distance -1)

    all_points = points + points_with_edge_points+points
    triangles, delaunay = triangulate_points(all_points)
    triangles = filter_triangles_inside_polygon(triangles, polygon)

    plot_triangles(triangles)
    quad, tri = combine_triangles_to_quadrangles(int(len(triangles) / 2), triangles)
    tris, quads  = separate_shapes(quad, tri, 0.5)
    plot_triangles_and_quadrangles(tris, quads)
    #create_svg(polygon, quads, tris, image_array, output_path)


def low_poly_vectorize_to_txt(input_path, distance_between_points_arg, points_min_distance, output_path_svg, ouput_path_txt, output_folder, generate_corner, width, height, color):
    """Main function to vectorize the object in the PNG image."""
    if (input_path == ""):

        polygon = generate_rectangle_perimeter_points(width * 70, height * 70, points_min_distance + 10, points_min_distance // 2)

        points = generate_random_points_in_polygon(polygon,5,points_min_distance)
        points = [p for p in points if p is not None]
        points_with_edge_points = add_edge_points_to_polygon(polygon, distance_between_points_arg/points_min_distance -1)

        all_points = points + points_with_edge_points+points
        triangles, delaunay = triangulate_points(all_points)
        triangles = filter_triangles(triangles, width*70, height*70)
        triangles = filter_triangles_inside_polygon(triangles, polygon)
        quad, tri = combine_triangles_to_quadrangles(int(len(triangles) / 2), triangles)

        if ((width >1 and height >1) and (width>2 or height>2)):
            bb_min = (35,35)
            bb_max = (35*(2 * width-1), 35*(2*height-1))
            quad = filter_shapes_outside_bbox(quad, bb_min, bb_max)
            tri = filter_shapes_outside_bbox(tri, bb_min, bb_max)

        tris, quads  = separate_shapes(quad, tri, 0.5)
        plot_triangles_and_quadrangles(tris, quads)
        if (output_path_svg != ""):
            pass#create_svg(polygon, quads, tris, None, output_path_svg, color_in = color)
        create_txt(polygon, quads, tris, None, ouput_path_txt, output_folder, width, height, color_in = color)
    else:
        image_array = np.array(Image.open(input_path).convert("RGBA"))
        polygon = generate_circumference_points(image_array, generate_corner)

        points = generate_random_points_in_polygon(polygon,5,points_min_distance)
        points_with_edge_points = add_edge_points_to_polygon(polygon, distance_between_points_arg/points_min_distance -1)

        all_points = points + points_with_edge_points+points
        triangles, delaunay = triangulate_points(all_points)
        triangles = filter_triangles_inside_polygon(triangles, polygon)

        plot_triangles(triangles)
        quad, tri = combine_triangles_to_quadrangles(int(len(triangles) / 2), triangles)

        tris, quads  = separate_shapes(quad, tri, 0.5)
        plot_triangles_and_quadrangles(tris, quads)
        #create_svg(polygon, quads, tris, image_array, output_path_svg)
        create_txt(polygon, quads, tris, image_array, ouput_path_txt, output_folder, width, height)
def wektoruj(width, height, color, reflect_dir):
    folder = reflect_dir+'building_blocks/'#{:02x}{:02x}{:02x}'.format(*color)
    def get_next_filename(folder_path, base_name):
        pattern = re.compile(rf'{re.escape(base_name)}-(\d+)\.txt$')
        max_number = -1
        os.makedirs(folder, exist_ok=True)

        for filename in os.listdir(folder_path):
            match = pattern.match(filename)
            if match:
                number = int(match.group(1))
                if number > max_number:
                    max_number = number

        next_number = max_number + 1
        next_filename = f"{base_name}-{next_number}.txt"
        return next_filename
    filename = get_next_filename(folder, str(width)+"x"+str(height))
    low_poly_vectorize_to_txt("", 20, 20,
                              "", #str(width)+"x"+str(height)+".svg",
                              filename, folder, True, width, height, color)

