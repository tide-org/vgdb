# vgdb

A vim plugin to give your editor super powers.

[![asciicast](https://asciinema.org/a/eOXrRp8ki4Ptz7w9H8Nc73J7k.svg)](https://asciinema.org/a/eOXrRp8ki4Ptz7w9H8Nc73J7k)

# Prerequisites:

Make sure git is installed. Works on MacOS and Linux.

# Installation

1. Install into Vim:

Using Vundle, in your `.vimrc` file:

    Plugin 'wilvk/vgdb'

2. Install the prerequisite libraries:

e.g.

    cd ~/.vim/bundle/vgdb
    bin/git-install

# Quick Start

3. From the command-line, tell `vgdb` where find the tide-plugin config details:

e.g.

    export TIDE_CONFIG_LOCATION=~/.vim/bundle/vgdb/plugins/test_go

(There are some tide-plugins that come with vgdb but you are free to make your own plugins.)

4. start up vim:

e.g.

    vgdb git:(master) ✗ vim

5. start up vgdb with an argument to the file to debug (optional):

e.g.

    :Vgdb ./tests/binaries/go_test/hello-world

 _pic here_

6. Set a breakpoint:

7. Run to breakpoint

8. Step through

# Tide configuration files




