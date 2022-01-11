# -*- coding: utf-8 -*-

import argparse, random, sys
from PIL import Image


def valid_point(p, width, height):
    """Return whether this point is within bounds of the maze
    """
    x, y = p
    return x >= 0 and x < width and y >= 0 and y < height


def get_neighbors(p, width, height):
    """Return the neighboring points
    """
    x, y = p
    points = []
    for neighbor_p in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
        if valid_point(neighbor_p, width, height):
            points.append(neighbor_p)
    return points


def render_maze(removed_edges, width, height):
    """Generate an iterator of frames to build a maze
    """
    image = Image.new('1', (2 * width + 1, 2 * height + 1))
    pixels = image.load()

    # add entrance
    pixels[1, 0] = 1
    yield image

    # add nodes and edges
    for a, b in removed_edges:
        a_x, a_y = a
        b_x, b_y = b
        wall_x, wall_y = a_x * 2, a_y * 2
        if a_x < b_x:
            wall_x += 1
        elif a_x > b_x:
            wall_x -= 1
        elif a_y < b_y:
            wall_y += 1
        elif a_y > b_y:
            wall_y -= 1
        pixels[wall_x + 1, wall_y + 1] = 1
        pixels[a_x * 2 + 1, a_y * 2 + 1] = 1
        pixels[b_x * 2 + 1, b_y * 2 + 1] = 1
        yield image

    # add exit
    pixels[2 * width - 1, 2 * height] = 1
    yield image


def save_image(filename, frames, scale):
    """Save the final frame as an image
    """
    image = None
    # get the final frame
    for image in frames:
        pass
    # upscale the image
    width, height = image.size
    image.resize((width * scale, height * scale)).save(filename)


def save_video(filename, frames, scale, duration):
    """Save frames as a video
    """
    images = []
    for image in frames:
        width, height = image.size
        images.append(image.resize((width * scale, height * scale)).convert('L'))
    images[0].save(fp=filename, format='GIF', append_images=images[1:], save_all=True, duration=duration, loop=0)


def generate_dfs_maze(width, height):
    """Generate a maze using the depth first search algorithm:
        expand randomly at the current node and backtrack when no more options
    """
    start = 0, 0
    visited = set([start])
    outstanding = [start]
    removed_edges = []
    while outstanding:
        current_pos = outstanding[-1]
        candidates = [p for p in get_neighbors(current_pos, width, height) if p not in visited]
        if candidates:
            next_pos = random.choice(candidates)
            visited.add(next_pos)
            outstanding.append(next_pos)
            edge = current_pos, next_pos
            removed_edges.append(edge)
        else:
            outstanding.pop()
    return removed_edges


def generate_bst_maze(width, height):
    """Generate a maze using the binary search tree algorithm:
        at a random node expand randomly to an unvisited node to the east or south
    """
    start = 0, 0
    visited = set([start])
    outstanding = [start]
    removed_edges = []
    while outstanding:
        index = random.randint(0, len(outstanding) - 1)
        current_pos = outstanding[index]
        candidates = [p for p in get_neighbors(current_pos, width, height) if p not in visited and p > current_pos]
        if candidates:
            next_pos = random.choice(candidates)
            visited.add(next_pos)
            outstanding.append(next_pos)
            edge = current_pos, next_pos
            removed_edges.append(edge)
        else:
            outstanding.pop(index)
    return removed_edges


def generate_kruskal_maze(width, height):
    removed_edges = []
    # initialize each node in a separate group and find all distinct edges
    nodes = {}
    outstanding_edges = []
    for row in range(height):
        for col in range(width):
            p = col, row
            nodes[p] = len(nodes)
            for neighbor in get_neighbors(p, width, height):
                if neighbor > p:
                    outstanding_edges.append((p, neighbor))

    while outstanding_edges:
        index = random.randint(0, len(outstanding_edges) - 1)
        a, b = outstanding_edges.pop(index)
        a_group, b_group = nodes[a], nodes[b]
        if a_group != b_group:
            # join these groups
            removed_edges.append((a, b))
            for node, group in nodes.items():
                if group == a_group:
                    nodes[node] = b_group
    return removed_edges


def main():
    algorithms = {
        'bst': generate_bst_maze,
        'dfs': generate_dfs_maze,
        'kruskal': generate_kruskal_maze,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=40, help='The width of the maze (default 40)')
    parser.add_argument('--height', type=int, default=40, help='The height of the maze (default 40)')
    parser.add_argument('--algorithm', help='The maze generation algorithm to use (default dfs)', default='dfs', choices=algorithms.keys())
    parser.add_argument('--filename', help='The filename where to save the result')
    parser.add_argument('--video', action='store_true', help='Whether to generate video output instead of image')
    parser.add_argument('--scale', type=int, default=100, help='The scale of the rendered output (default 100)')
    parser.add_argument('--duration', type=int, default=200, help='The duration of the rendered video (default 200)')
    args = parser.parse_args()

    generate_maze_algorithm = algorithms[args.algorithm]
    removed_edges = generate_maze_algorithm(args.width, args.height)
    frames = render_maze(removed_edges, args.width, args.height)
    if args.video:
        # generate video output
        save_video(args.filename or 'maze.gif', frames, args.scale, args.duration)
    else:
        # generate image output
        save_image(args.filename or 'maze.png', frames, args.scale)


if __name__ == '__main__':
    main()
