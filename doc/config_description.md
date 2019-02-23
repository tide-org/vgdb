# Main sections:

buffers:

commands:

events:

settings:

  - buffers:
      - base_filter_name: is the name of a filter to filter all output with. default is ''. if specified, this corresponds with a filter name in the filters path.
      - error_filter_name: is the name of a filter to be applied to output to capture error logs and transform output in some way based on it, if necessary.
      - error_buffer_name: this is the name of an internal buffer to hold the results of the error filter 'error_filter_name' in. this is in the config dictionary as vg_config_dictionary["internal"]["buffers"][error_buffer_name]
      - stack_buffers_by_default: if true, this stacks all new buffers in a single window that splits horizontally with every new buffer.
      - stack_buffer_window_width: this is the width in characters that the buffer will take up of the screen (some of this may need to move once cross-editor is implemented)
      -
  - debugging:
      - log_to_file: if true, debugging output is logged to a file
      - log_filename: the name of the file for output of vgdb
      - debug_*: all the options starting with debug_ are various modules to enable debugging for. e.g. debug_command_action is for the module command_action, with the class CommandAction.
  - editor:
      - name: is the name of the editor that the config will be used for. defaults to 'vim81'
  - logging:
      - use_session_log_file: specifies if the output of the session_log will be written to a file. defaults to true.
      - session_log_filename: the name of the file to output the session_log to defaults to 'vgdb_session.log'
      - session_buffer_name: the name of the buffer to use to store the session_log. defaults to vg_session_log'
      - add_timestamp: if true, adds a timestmp to the session log for every entry. defaults to true.
  - plugins:
      - actions_path: the location of actions relative to the config path, or absolute. defaults to '../actions'. actions can be used to extend the functionality of commands in the config.
      - filters_path: the location of filters relative to the config path, or absolute. filters are used for capturing specific information from the output for processing in a buffer. defaults to '../filters
      - functions_path: the location of functions that can be called from commands in the config. defaults to '../functions'
  - processes:
      - ttl_stream_timeout: the time in seconds of how long to wait before timing out on the output of the ttl stream from the process. defaults to 0.08s.
      - run_command_on_startup: if true, runs a command at startup of Vgdb as specified by 'command_to_run_on_startup'
      - command_to_run_on_startup: TODO: requires rework
      - command_on_startup_log_file: TODO: same
      - main_process_name: the name of the process to start for output
      - main_process_default_arguments: a space-separated list of arguments to pass to the main process
      - find_full_process_name: this locates the full path to the process to run if only the name is specified. similar to using 'which'.
      - end_of_output_regex: a regex that determines the end of output after running a command on the process. This is usually for terminal-type applications.

variables:
  - contains a list of user-defined variables. these can be accessed in the config and are usually used for specifying defaults for variables and making explicit what variables are being used. This is the main way information is passed between commands. variables can also be updated from filters and functions, or even actions.








