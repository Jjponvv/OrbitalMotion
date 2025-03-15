# Orbital motion

<img src="img/screen.png" alt="screenshot" width="500" height="350">

## What i do to make this project?

For each object in the project, I created a separate class that contained functions for determining gravity, drawing, and updating velocity and position.

## The force of gravity

In my project I defined it using this formula: 
### G * m₁ * m₂ / r^2  
#### Where:  
  
 **G** ⏤ Gravitational constant\
 **m** ⏤ mass\
 **r** ⏤ distance between object1 and object2

<img src="img/newton-law-gravitation-gravity-gravitational-force.png" alt="Newton gravity formula" width="250" height="150">

This formula returns only the force modulus  
To get a vector for x and y I use the arctan function - the opposite of tan with the values ​​Δx, Δy  
**Δx** ⏤  x2 - x1  
**Δy** ⏤  y2 - y1  
Next, I use cosine and sine to determine the horizontal (x) and vertical (y) respectively, multiplying them by force

## Updating velocity and position

To update the velocity and positions, I used Euler's method and Newton's second law:  

Euler's method:  
<img src="img/Euler.png" alt="Euler method" width="auto" height="auto">

Where:  
**v** ⏤ velocity  
**a** ⏤ acceleration  
**x** ⏤ position x  
**y** ⏤ position y  
​**Δt** ⏤ delta time (in my case it's TIMESTEP)

Newton's second law for finding acceleration:  
<img src="img/NewtonsSecondLaw.png" alt="Newton's second law" width="150" height="100">  
Where:  
**F** ⏤ force  
**m** ⏤ mass

## Drawing
This is a common method for drawing objects in pygame but using SCALE to make the object fit on the screen.

## What can be depicted

This program can draw a circular object of any color, any radius, any position (x, y), and any mass.

This is what it looks like in the example:  
### "Model of sun" ⏤ `Object_(WIDTH / 2, HEIGHT / 2, 30, pg.Color('Yellow'), 1.989e30)` 
### Where:  
**WIDTH / 2, HEIGHT / 2** ⏤ x, y cordinate  
**30** ⏤ radius  
**pg.Color('Yellow')** ⏤ color  
**1.989e30** ⏤ mass

## How can this be used?

This is just a simulation of orbital motion. Can be used as a toy

### People
[@tolikhalas](https://github.com/tolikhalas)

