# Maze Generator

## Setup

    $ pip install -r requirements.txt

## Usage

    maze.py [-h] [--width WIDTH] [--height HEIGHT] [--algorithm {bst,dfs,kruskal}] [--filename FILENAME] [--video] [--scale SCALE] [--duration DURATION]

    optional arguments:
      -h, --help            show this help message and exit
      --width WIDTH         The width of the maze (default 40)
      --height HEIGHT       The height of the maze (default 40)
      --algorithm {bst,dfs,kruskal}
                            The maze generation algorithm to use (default dfs)
      --filename FILENAME   The filename where to save the result
      --video               Whether to generate video output instead of image
      --scale SCALE         The scale of the rendered output (default 100)
      --duration DURATION   The duration of the rendered video (default 200)

## Results

By default generate a maze image using a depth first search algorithm:

    $ python maze.py

![Image](output/maze_dfs.png)

Generate a video showing each step of the maze generation process:

    $ python maze.py --width=20 --height=20 --video
    
![Image](output/maze_dfs.gif)

Generate a maze using a different algorithm:

    $ python maze.py --width=20 --height=20 --algorithm=kruskal --video
    
![Image](output/maze_kruskal.gif)
