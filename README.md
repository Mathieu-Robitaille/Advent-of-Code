# Advent of Code

This is an autogen for an advent of code project. We all want to just sit back and focus on actualyl writing the code, so this should auto build dir structure and pull the input.

You'll need to populate ```secrets/.cookie``` and ```secrets/.twilio``` following the template put there.

Also you'll need to put these in a crontab. If you're on windows... well... **sucks to suck**.

advent-init.py
-----

Creates folder structure for your project, if it is December before the 26th (basically a valid advent day) it creates all the missing files for your project as follows.

- Copies the templates in template/ to ```source/{year}/{day}/part1.py``` and ```source/{year}/{day}/part2.py```
- Pulls the input from advent of code for that day.

There are optional cli args if you wanna test stuff or for wtv.
- ```-y``` Specify the year to pull and create for.
- ```-d``` Specify the day, this is the last day it will itterate to.
  - Ex: ```python3 advent-init.py -y 2020 -d 15``` will pull and create the structure for 2020, from the 1st to the 15th.
- ```-s``` Specify a non default path for your source. (Default: ```./source/```)
- ```-v``` Verbose mode. (Warning: very loud)
- ```-i``` Check if paths are alright before proceeding.

annoy.py
-----
This texts you if you havent started, or havent completed today's challenge yet. Get cracking.