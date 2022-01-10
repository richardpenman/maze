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
    """Render maze to an image
    """
    image = Image.new('1', (2 * width + 1, 2 * height + 1))
    pixels = image.load()
    # add edges
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
    # add points
    for y in range(height):
        for x in range(width):
            pixels[x * 2 + 1, y * 2 + 1] = 1
    # add entrances
    pixels[1, 0] = 1
    pixels[2 * width - 1, 2 * height] = 1
    # upscale the image
    return image


def create_maze(width, height):
    """Create a maze of these dimensions and return the edges that have been removed
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', type=int, default=50, help='The width of the maze (default 50)')
    parser.add_argument('--height', type=int, default=50, help='The height of the maze (default 50)')
    parser.add_argument('--filename', default='maze.png', help='The image filename where to save the result (default maze.png)')
    parser.add_argument('--scale', type=int, default=100, help='The scale of the rendered image (default 100)')
    args = parser.parse_args()

    removed_edges = create_maze(args.width, args.height)
    image = render_maze(removed_edges, args.width, args.height)
    image.resize((args.width * args.scale, args.height * args.scale)).save(args.filename)


if __name__ == '__main__':
    main()
