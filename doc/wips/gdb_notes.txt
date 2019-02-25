for debugging c applications that were built on mac as a MachO binary:

brew install https://raw.githubusercontent.com/timotheecour/homebrew-timutil/master/gdb_tim.rb

as gdb needs to be codesigned (for local work) you should run vim as sudo with environment variables:

e.g.

sudo -E vim

for debugging a remote linux target:

http://tomszilagyi.github.io/2018/03/Remote-gdb-with-stl-pp

brew install gdb --with-all-targets


to switch:

for remote:

brew unlink gdb && brew link --overwrite gdb

for local:

brew unlink gdb_tim && brew link --overwrite gdb_tim
