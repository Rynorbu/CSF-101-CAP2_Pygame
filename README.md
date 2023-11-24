# Flappy Bird Game Testing

## 1.  Test Game Initializatio

+ Initializes Pygame and creates a display surface
+ Verifies successful initialization by checking display surface is not None

## 2.  Test image loading and scaling

+  Attempts to load the bluebird-downflap.png image file from /Images folder
+ Scales the bird surface to 2x original size using Pygame transform
+ Validates image loaded and scaled properly by checking surface is not None
+ Catches Pygame errors during image load/manipulation and fails test

## 3.  Test event handling

+ Posts a keyboard spacebar press event to the Pygame event queue
+ Iterates through event queue and checks for space keydown event
+ Fails if spacebar event not posted or handled correctly

## 4.  Test collision detection

+ Creates sample bird and pipe surfaces
+ Positions pipe rect to collide with bird rect
+ Passes rects to custom collision function your_collision_function
+ Verifies collision function returns expected True value on collision

## 5.  Test create pipe

+ Defines sample pipe heights and picks random height
+ Calls create_pipe to generate pipe rects
+ Compares pipe positions and dimensions to expected values
+ Fails if any pipe property does not match expected
