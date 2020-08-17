# Solving-Lights-Out

In 1995, Tiger Electronics put out the handheld game, Lights Out. 

![Lights Out](Design%20Process/images/LightsOut.jpg)

The premise of the game was simple. Sporting a 5x5 grid of lights, the object of the game was to turn out all of the lights. By pressing a button, the light underneath and on all 4 sides of that button were toggled, either on or off. 

![Button Pressed](Design%20Process/images/ButtonPressed.jpg)

Using this method, the player had to think strategically about where to press to get them closer to having all of the lights out.

This application is designed to generate all the solvable states of the game, and using a breadth first search from the solved state, get the shortest path to solution for every state. Using the created solutions data set, the player can easily generate the fastest solution to solving any solvable board.

---

![App Start](Design%20Process/images/AppStart.png)

On starting the application, the user has to load the game solutions. If the user has never generated solutions before, the dataset will be generated and stored in a ./data folder.

![Generating Solutions](Design%20Process/images/GeneratingSolutions.png)

Once generated they can be loaded. The generation process will only happen once, unless the user deletes ore moves the ./data folder.

![Loading Solutions](Design%20Process/images/LoadingSolutions.png)

With everything loaded, the Load button is swapped out with a New and Solve button.

![Ready](Design%20Process/images/Ready.png)

The user can now enter their Lights Out board using the checkboxes.

![Entered](Design%20Process/images/Entered.png)

Then the user can press Solve, and get their answer on how to beat the current Lights Out board.

![Solved](Design%20Process/images/Solved.png)

There are boards that cannot be solved in Lights Out. If the player happens to enter one in a custom board, the application will let them know that the board is unsolvable.

![Unsolvable](Design%20Process/images/Unsolvable.png)
