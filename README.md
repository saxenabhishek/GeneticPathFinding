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
  
  
when run with the above parameters we can see:
![test1](https://github.com/saxenabhishek/GeneticPathFinding/blob/master/pics/gen1.jpg)

* Small Green squares - Agents
* lines and circles on agents - to show their velocity vector.
* Big Blue Boxes - Obstacles 
* Green Line - Best path as of now.
* Blue Dot - Destination Point
* Red Dot - Point with the Highest score on the green line.

This image is of the 5th genaration. Notice how it's easy for the agents to colide with the edge of the screen to reduce their speed and then go in the opposite direction to reach their destination.

After about 20 secs of training and at genaration 43.
![test1](https://github.com/saxenabhishek/GeneticPathFinding/blob/master/pics/gen2.jpg)


The agents have figured out an easier path by bending towards the destination so they could reach the destination quicker.
