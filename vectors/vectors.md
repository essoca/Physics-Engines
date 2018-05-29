Vectors
============

Vectors are objects used in Physics to represent quantities that have a direction associated (like displacement: you walk a certain amount of meters heading north). In this project, a given number of vectors are drawn randomly and the user has to add them using the tail-to-head method.

### How to represent vectors?

In 2D, vectors are represented by the cartesian coordinates (*A*<sub>*x*</sub>, *A*<sub>*y*</sub>) or by the polar coordinates (*r*, *θ*), where *r* gives the length of the vector (magnitude), and *θ* the direction along which the arrows used to draw them point. Note however that, for the graphical representation using arrows, we need to know *where* to put them in the screen, which can be done e.g. by saving the coordinates of the tail.

### How to draw vectors?

The length of a vector gives a natural scale to draw. Once you identified the coordinates of the tail, you can get the vertices of the polygon defining the arrow by knowing the polar coordinates of the vector and some aspect ratios. For the figure below, for instance,
*w* = 0.1*l*,   *t* = 0.2*l*,   *w*<sub>*t*</sub> = 0.6*w*.

 ![Drawing a vector as an arrow](https://raw.githubusercontent.com/essoca/Physics-Engines/master/images/arrow.png)
### Detecting mouse events

The simpler the better. In order to check if you have clicked on the vector, you may just detect the collision of the mouse position with the shortest rectangle containing the polygon (easily obtained in Pygame with get\_rect). To detect if the tail of one vector is on the head of another one, you may just check if you have clicked inside the circle centered half way between the head and tip of the arrow representing the vector, with radius *t*/2. Make sure that when these events happen, you force the coordinates of the involved head and tail to coincide (here head denotes the coordinates that you get by using the components of the vector referred to the coordinates of the tail).

Note that once the vector sum---which you should draw using a different color (say red) than the blue above---has been drawn, the dragging events for the vectors should stop, which basically freeze the vectors.
