# Buffers

buffers list the buffers/windows available to be displayed.

a buffer has a set of options:

on_startup: determines whether the buffer starts at startup of :Vgdb
command: a config command that can be run for the buffer every time an action occurs
line_numbers: determines whether the buffer will have line numbers or not
buffer_filename_variable: if set, specifies the name of a variable to use for specifying the filename of the buffer. if not specified, the buffer will be named as per the config file designation.
primary_window: if true, the buffer will be the primary window in the editor and will not be stacked with other windows. There should be only one primary window. The primary window is usually used for code editing. Non-primary windows are for more trivial (but still important) windows.
language: defines the syntax language to use for syntax highlighting in the buffer.
events: these can happen either:
 - before_command
 - after_command
and are extra commands that run before/after the `command:` command has run.
Each command can be presupposed with 'input_args:' which are a list of key-values that are sent to the command for further processing depending on the context. Usually used when running python or vim functions.


