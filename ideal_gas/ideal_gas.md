The ideal gas
=============

The [ideal gas](https://en.wikipedia.org/wiki/Ideal_gas) is perhaps one of the most simplistic models of a physical system which actually describe real gases under special conditions (low densities, high temperatures).

*Macroscopically*, an ideal gas enclosed in a container of volume  at  pressure  and temperature  is one that satisfies the equation of state

*p**V* = *N**k*<sub>*B*</sub>*T*

where *N* is the number of particles in the gas and *k*<sub>*B*</sub> is the Boltzmann constant. Our goal is to simulate this macroscopic behavior by a using a microscopic model for the ideal gas.

### Microscopic model

We want to put a bunch of noninteracting particles in a container, moving at constant speed and elastically colliding with the walls of the container. The probability distribution of the speed of each particle turns out to be the Maxwell-Boltzmann distribution. For a 2D gas (we are in two-dimensions in Pygame), take a look at [this](http://fab.cba.mit.edu/classes/864.11/people/dhaval_adjodah/final_project/write_up_boltzmann.pdf) for the derivation of the Maxwell-Bolztmann distribution in 2D. This turns out to be a chi distribution with 2 degrees of freedom (also known as Raileigh distribution) which is built-in in most statistical packages (for instance, the python numpy.random.rayleigh). The corresponding probability density function is

$$f\_\\sigma(v)=\\dfrac{v}{\\sigma^2}e^{-v^2/2\\sigma^2}$$

where *v* is the speed, and *σ*<sup>2</sup> = *k*<sub>*B*</sub>*T*/*m*, with *m* being the mass of each particle. Here *σ* plays the role of the scale parameter.

### Simulation

Using the microscopic model, we want to test Boyle's law (keeping *T* constant in the equation of state). That is, we want to compress our gas and measure pressure versus volume, plotting the result. Therefore, we want to compare with

$$p=\\dfrac{mN\\sigma^2}{h}$$

where *σ*<sup>2</sup> is a measure of the (fixed) temperature and *h* the height of the closed container, which you should vary in the simulation. For a given number of particles *N*, we will choose values of *m* that fit your data (this method can be improved).

Note: to measure pressure, choose a fixed interval of time (for instance 100 ) and count how many collisions occur on each wall. For each wall, multiply that by the change in momentum perpendicular to the wall, and average the resulting number among the 4 walls.

Run the simulation by slowly varying the vertical position *h* of the wall at the top (piston) from an initial value to a final value. The screen should show the process. Once the final value is reached you should have two arrays: all the values of pressure that you measure for each corresponding value of *h*. Look up how to plot (using python matplotlib) *h* in the horizontal axis, *p* in the vertical axis (your data), superimposed to the curve *p* = *m**N**σ*<sup>2</sup>/*h* (which you generate in the same plot and display with line, no points). This should go directly to a png file in your working directory, not to the screen, which is then read by Pygame (say as myplot = pygame.image.load("file.png") and placed on the screen (say as screen.blit(myplot, choose where)). Probably there is a better way to do this, but this ensures that the plot appears on the same screen as the Pygame simulation.

A sample plot:

![Boyle's law](https://raw.githubusercontent.com/essoca/Physics-Engines/master/images/idealgas.png)
