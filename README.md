# 20questions

See https://en.wikipedia.org/wiki/Twenty_Questions

The idea is to have the program guess an object the player is thinking of. It starts with a blank slate, but over time collects information (both objects and questions) that allows it to narrow down the questions and make smarter guesses.

I've already built something like this a few years ago but back then all input/output took place at the command prompt, and both guesses and questions were limited to very low numbers and were only stored in memory.

This time I want to have a GUI and store the game data in json. Of course, the really interesting part is using entropy comparisons to allow the computer to pick the best questions and guesses depending on previous sessions as well as questions already asked in the current session.

I've decided on pyqt, so I can learn Qt and gain some more experience in Python (particularly version 3.x).
