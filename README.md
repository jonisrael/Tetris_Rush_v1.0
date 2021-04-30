# Tetris_Rush_v1.0
Created by Jonathan Israel in PyGame, an extension of Python.  Started on December 7th, 2020, Released 4/30/2021.  Original Concept by a FreeCodeCamp template from the video here: https://youtu.be/zfvxp7PgQ6c.

Tetris with Classic and Modern Tetris Physics (Python).  You must import pygame from a python interpreter in order to play.  Luckily, it is built in to most versions of python!
Uses a freeCodeCamp Tetris template from the video https://youtu.be/zfvxp7PgQ6c

The purpose is to create a program that can play both the original early versions of NTSC Tetris (NES Tetris, Gameboy Tetris), as well as a modern tetris minigame using physics from most tetris games after 2006. More specifically, it uses the "Tetris guideline" https://tetris.fandom.com/wiki/Tetris_Guideline.  This recreation is not perfect and the code is a mess, but I did my best spending a couple hundred hours on this!  I will improve these changes over time, but I needed to finally release at least some sort of finished project.


==========================================================
                   VERSION DIFFERENCES
==========================================================


TL:DR Classic Tetris Rules:
  - Piece generation is random, with one re-roll to try and combat repetition (yet, it isn't very good, as shown in this video of an 83 piece drought before spawning an "I" piece: https://youtu.be/1hIlqkwUcy0)
  - When a piece hits the ground or another piece, when it falls another grid cell it will lock into place.  There is no delay.
  - There is no piece rotation correction, also known as wall kicks.  If a piece cannot rotate, there is no correction to rotate it anyway.  (For example, try having a long bar on the right-most x coordinate.  If you try rotating, it will not work.)
  - There is an auto-repeater for most tetris games by holding left or right.  The classic ones are hilariously slow, but I implemented it anyway.  I did NOT use pygame's set_repeat function, I created my own from scratch as I had too many problems with the built-in one.
  - There is an animation for clearing lines in an attempt to match the piece clear timing

TL:DR Modern Tetris Rules:
  - Piece generation is NOT random, but 7 piece bags are.  Each bag contains one instance of each piece type, randomly ordered.  This makes getting pieces you need more predictable. More information of the modern random generator: https://tetris.fandom.com/wiki/Random_Generator
  - You can hold a certain piece for later use.  You must place the next piece before being able to swap the hold piece for another piece.
  - The auto-repeater by holding left or right is much faster than the classic version
  - Piece rotation attempts to correct itself if it is stuck on a wall using a "wall kick".  For example, if you try and hold a long bar on the right-most x coordinate, if you rotate it clockwise it will correct itself by moving two units to the left before rotating.  Without this, the piece simply cannot rotate as it would be out of bounds if it tried to.
  - There is a half of a second before piece lock, meaning you can still move pieces left and right as well as rotate them for a bit before the piece locks into place.
  - Other things that I probably forgot to mention here.

MODERN TETRIS MINIGAME RULES:
  - After 15 seconds of setting up a tetris field, the player will be trying to clear garbage that rises from the bottom.  The more lines that are cleared, the more time the player has to place pieces without garbage rising.  There is a max "buffer" of 6, and every time a piece is placed, it goes down one.  When you clear lines, it goes up one, two, three, or five based on if you get a single, double, triple, or quad clear, respectively.  When the buffer hits one or zero, the field starts blinking red, warning the player that when the buffer hits zero the garbage will start rising.
  - 
==========================================================
                       CHANGES
==========================================================

CRITICAL BUG FIXES (Things that caused the freeCodeCamp original program to not work correctly):
  - Fixed a line clear calculation bug when clearing three or four lines with non-cleared line(s) in-between. (Hardest and most important bug to fix)
  - Fixed having pieces hang off the top of the grid, leading to accidental game-overs or pieces being locked on the top rows.
  - Fixed game-over rule to match regular tetris, where the game ends if a piece cannot spawn, instead of if a piece goes above the grid
  - Fixed bug where pieces were sometimes locked in mid-air
  - Added error handler to pause and say "Error!" when an exception occurs, allowing the developer to analyze the grid before quitting, instead of the program just locking up and having to restart the python kernal or using the Windows/Mac/Linux OS to terminate the program.



What I added within the last five months (Not necessarily in order):
  - Added two different game-modes with different mechanics, scoring, and game objectives.
  - Added counterclockwise rotation
  - Added a ghost piece (location where the piece will drop), which does not interact with the grid other than for information.  This was the hardest thing to program.
  - Added a hard-drop function by pressing "Up", where a piece is automatically placed where the ghost piece is at.  [Modern Only]
  - Changed function of down key to drop one cell, then shortly after, alter gravity to dropping 30 grid-cells per second until key is no longer pressed.
    Changed Keys to be more ergonomic, and eventually added control list upon bootup.  Press Q to restart program, and "\" to enable developer mode, where the grid does not disappear when you pause
  - Ajustable levels, gravity speeds, and score system, based off Classic and Modern score systems
  - Added Pause Function (which is also used as the error handler)
  - Added a 3-2-1-Go function at the beginning
  - Changed how pressing and holding the down key worked to match other tetris games
  - Added line-clear effects
  - Added a cool game-over effect
  - Cool grid-line changes based on level (classic) or buffer amount (modern)
  - Added a slight delay before the next piece is dropped [Classic Only]
  - Added more things to the heads-up display when playing, based off the game mode:
    - Added statistics for Classic Mode based on what completely random pieces are generated, by both number and percentage
    - Added Tetris Rate or Safety Buffer for classic/modern respectively (number of quad clears / total_lines_cleared), and safety buffer counter 

Known Bugs:
  - Wall-kicks still are not perfect, particularly with T-spins.  It will still fail to rotate sometimes.  Help me by looking at the rotate() function!  The SRS rotation system should match this: https://tetris.fandom.com/wiki/SRS
  - When holding left or right and then rotating, pieces sometimes move a lot further to the left or right than they are supposed to.
  - There are ways to create a situation where you can have infinite rotations in the modern version of tetris
  - Somehow, I need to find a way to not use pygame.time.delay(), as it causes problems of dropping "invisible" pieces if hard dropping too fast (these pieces have a color value of (1,1,1) and are used for a lot of functions, such as the classic-mode piece spawn delay).

Future Changes Planned:
  - Remove all instances of pygame.time.delay() and replace them with necessary game stoppages (such as when a line is cleared).  This will lead to less controls issues and easier effects to animate like flashing effects.
  - Count all Singles, Doubles, Triples, and Quads, and try and figure out where to put them.
  - Allow scores to be written to .txt files so that they can be saved.  I may also read off them too.
  - Create opening message with Title, Author, and cool drawing or animation
  - Make minigame optional or add configurable settings (only created it a week ago because it made modern tetris a lot more interesting)
  - Work more on trying to make the SRS system work better (still having problems with wall-kicks and double or triple t-spins
  - Clean up the code, maybe use other .py files to organize it
  - I always seem to come up with more as I code the program, so I am sure there will be more!

Thank you for reading, and thank you for playing!!!
