# Advent of Code

This is an autogen for an advent of code project. We all want to just sit back and focus on actually writing the code, so this auto builds a directory structure, clones over template files, and pulls the input.

What you need to do
- Populate ```secrets/.cookie``` and ```secrets/.twilio``` following the template put there.
- Put your own templates in ```templates```. Any name is fine, any directory structure is fine.
- put these in a crontab. If you're on windows... well... **sucks to suck**.

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
- ```-l``` Specify the language to be used, so far we have Rust and Python. Default is Python.

annoy.py
-----
This texts you if you havent started, or havent completed today's challenge yet. Get cracking.
You should populate ```local_src.txt``` if you intend to source your project in another dir, it will then check for the path in that file. 

Ex: ```local_src.txt``` contains ```/home/$USER/git/src-advent-of-code/src```

We check ```/home/$USER/git/src-advent-of-code/src/$YEAR/$DAY/```


# Example crontab

You'll wanna automate this so you can sit down with your coffee and relax with some AoC.

#### Setup
```shell
# make a logging dir
mkdir $HOME/log/advent

# Create the file
touch $HOME/log/advent/advent.log

# The sudo is due to default perms on logrotate being 644 root:root
# its almost like you dont need this!
cat << EOF | sudo tee -a /etc/logrotate.d/aoc
$HOME/log/advent/*.log {
        compress
        copytruncate
        delaycompress
        missingok
        rotate 1
        size 10k
}
EOF
```

## The corncob itself
```
0 17 * 12 * .../advent-of-code/env/bin/python3 .../advent-of-code/annoy.py >/dev/null 2>&1
0 6 * 12 * .../advent-of-code/env/bin/python3 .../advent-of-code/advent-init.py -s .../src-advent-of-code/src/python/ -v | tee -a $HOME/log/advent/advent.log
```

# Example Usage

Say you want to start a python project, or you have one going in ```$GIT_DIR/src-advent-of-code/src/python/```, ```$GIT_DIR``` is some arbitrary root location, it'll be different for everyone. If you dont know whats what just use this 
```shell
GIT_DIR=$HOME/git
```
```shell
$GIT_DIR/advent-of-code/env/bin/python3 $GIT_DIR/advent-of-code/advent-init.py -s $GIT_DIR/src-advent-of-code/src/python/ -v | tee -a $HOME/log/advent/advent.log
```

Or maybe a rust project?
```shell
$GIT_DIR/advent-of-code/env/bin/python3 $GIT_DIR/advent-of-code/advent-init.py -s $GIT_DIR/src-advent-of-code/src/rust/ -v -l rust | tee -a $HOME/log/advent/advent.log
```

Note that I change the dest path ```-s``` cause I like it sperate. You do you tho!
from_utf8