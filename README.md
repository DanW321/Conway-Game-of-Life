# Conway's Game of Life

**An interactive implementation of Conway's Game of Life.**

## Introduction
Conway's Game of Life is a cellular simulation developed by John Conway in 1970. The world of this simulation is an infinite grid of cells, and each cell can either be "off" or "on". Given an initial state, the progression of the simlulation is determined by a simple set of rules.

From [Wikipedia](https://en.wikipedia.org/wiki/Conway's_Game_of_Life#cite_note-68):

1. Any live cell with fewer than two live neighbors dies, as if by underpopulation
2. Any live cell with two or three live neighbors lives on to the next generation
3. Any live cell with more than three live neighbors dies, as if by overpopulation
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction

Some patterns of cells are stable, meaning they do not change without influence from an outside source. Some patterns are dynamically stable, meaning they oscillate with a certain period. Some patterns grow infinitely.
Continue reading to learn more about this specific implementation!

## Program



