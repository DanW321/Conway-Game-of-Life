# Conway's Game of Life

**An interactive implementation of Conway's Game of Life.**

## Introduction
Conway's Game of Life is a cellular simulation developed by John Conway in 1970. The world of this simulation is an infinite grid of cells, and each cell can either be "off" or "on". Given an initial state, the progression of the simlulation is determined by a simple set of rules.

From [Wikipedia](https://en.wikipedia.org/wiki/Conway's_Game_of_Life#cite_note-68):

1. Any live cell with fewer than two live neighbors dies, as if by underpopulation
2. Any live cell with two or three live neighbors lives on to the next generation
3. Any live cell with more than three live neighbors dies, as if by overpopulation
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction

Some patterns of cells are stable, meaning they do not change or move without influence from an outside source. Some patterns are dynamically stable, meaning they oscillate with a certain period. Some patterns grow infinitely.
Continue reading to learn more about this specific implementation!

## Program
Run conway.py to start interacting with the simulation!

**Mouse**
- <ins>Left Click</ins> to toggle the state of individual grid cells and place a preset object.
- <ins>Right Click</ins> and drag to "brush" grid cells on.

**Keyboard**
- Press <ins>Space</ins> to play or pause the simulation
- Press the <ins>Left and Right Arrows</ins> to adjust the simulation speed
- Press <ins>R</ins> to randomize the grid
- Press <ins>C</ins> to clear the grid
- Press <ins>1-5</ins> to enter dragging mode
- Press <ins>esc</ins> to exit dragging mode

There are five preset objects hardcoded in presets.py. These are patterns that exhibit interesting behavior such as periodicity, infinite movement, and more (taken from [Wikipedia](https://en.wikipedia.org/wiki/Conway's_Game_of_Life#cite_note-68)). Press 1-5 while the game is paused to view and place these patterns on the grid. Play around with the simulation and see if you can discover your own interesting patterns!

## Notes
The game environment is supposed to be infinite, but this implementation uses a toroidal array to simulate infinity. This means that the top and bottom edges are stitched together, as well as the left and right edges. This is a good but not perfect representation of an infinite grid, as certain patterns can "wrap around" and influence other patterns that they otherwise would never touch.

The graphical side of this program is implemented using the [pygame](https://www.pygame.org/docs/) package. Enjoy!



