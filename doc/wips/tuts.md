[ ] write some small tutorials on how to do things with the config files and filters/functions
  - do a hello world example
  - do a logging to buffer example
  - do a python function example
  - show grabbing a variable from a filter
  - show setting a variable from config and using it in a config command
  - show setting a variable from config and using it in a python function


Standard process:

The standard process is to have a buffer designated for accepting the output of a command.

The command is run against the process and the output is filtered then placed in the buffer.

A buffer is specified in the config under the buffers section.

A command is specified in the config under the commands section.

A filter is specified in a path (that has been set in the config settings). A filter is for a buffer and will have the same name as the buffer it is providing output for. A base filter may also be provided to do some initial filtering before the buffer's filter does it's work.

For example, the process for running a single command would have the following flow:

Run named config command from Vim -> command is run against running process -> output is filtered with a base filter -> output is filtered with the buffer's filter -> output is displayed in vim

The name of the buffer that the command is for can be set in one of the following ways:
- If the command is called from the buffer, e.g. <buffer_name>.command: the buffer name will be passed to the command.
- If the command is called as an event after a buffer command is run e.g. <buffer_name>.events:
- If the buffer_name is specified explicitly in a run_command config command.


