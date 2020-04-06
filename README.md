# GeneticPathFinding

### What is this?
This is a simulation to find the shortest path between two points using a version of the genetic algorithm

### How does it work?
Small agents start from a point and try to reach the end in a given amount of time. They are given a score based on how well they performed. A new generation is formed on the vectors of the top performers. This goes on till the best path is found.

### Why is this significant?
Agents do whatever gives them a higher score. My implementation finds the path between two points. Only by changing how the scoring system works you can tell them to do anything given that the tast can be scored. 

### How can I run it?
you need a version of pygame and the files in this repo

In gamevo.py you can play with these variables
* width, height of screen
  > w, h = 1280, 600
* start and end points
  >start = (20, 20)
  >end = (1100, 500)
* population size (pop)
* mutation rate (mutrate)
* frames per generation (fpg)
* obstacles (obs)
  * >pop = 200
  * >mutrate = 0.01
  * >fpg = 300
  * >obs = 15
  

@ TODO

* comment everything
* add screenshots
