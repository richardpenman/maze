# Maze Generator

## Description

Uses depth first search to generate a maze

## Setup

    $ pip install -r requirements.txt

## Usage

    maze.py [-h] [--width WIDTH] [--height HEIGHT] [--filename FILENAME] [--video] [--scale SCALE] [--duration DURATION]

    optional arguments:
      -h, --help           show this help message and exit
      --width WIDTH        The width of the maze (default 50)
      --height HEIGHT      The height of the maze (default 50)
      --filename FILENAME  The filename where to save the result
      --video              Whether to generate video output instead of image
      --scale SCALE        The scale of the rendered output (default 100)
      --duration DURATION  The duration of the rendered video (default 200) 
          
## Results

    $ python maze.py

![Image](output/maze.png)
