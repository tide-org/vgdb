ideal state:

- events.on_startup
- buffers.<name>.command
- buffers.<name>.events.after_startup 


current state (understanding):

 - before buffer opens
 - after buffer opens

 - after startup

startup tracing:

Tide started successfully
opening buffer: vg_session_log for window: 2
opening buffer: vg_test_template for window: 2
COMMAND: vgdb.run_config_command("display_template", "vg_test_template")
opening buffer: vg_code for window: 2
COMMAND: vgdb.run_config_command("set_piets", "vg_code", "after_command")
call buffer_piets#set_piets({'function_args': 'None', 'event_input_args': {'piet_match_array_variable': 'file_lines', 'current_filename_variable': 'current_filename'}, 'buffer_name': 'vg_code'})
COMMAND: vgdb.run_config_command("set_highlight_line", "vg_code", "after_command")
call buffer_breakpoint#set_highlight_line({'function_args': 'None', 'event_input_args': {'highlight_line_variable': 'current_line_number'}, 'buffer_name': 'vg_code'})
config command ran successfully: load_file
opening buffer: vg_session_log for window: 2
opening buffer: vg_test_template for window: 2
opening buffer: vg_code for window: 2
call set_highlight#for_breakpoint_and_diff({'function_args': 'None', 'event_input_args': 'None', 'buffer_name': ''})
config command ran successfully: set_highlight_for_breakpoint_and_diff
opening buffer: vg_session_log for window: 2
opening buffer: vg_test_template for window: 2
opening buffer: vg_code for window: 2
call set_buffer#for_filename({'function_args': {'buffer_name': 'vg_code', 'file_name': '/Users/willvk/source/wilvk/vgdb/tests/binaries/c_test/main.c'}, 'event_input_args': 'None', 'buffer_name': ''})
call buffer_breakpoint#set_highlight_line({'function_args': 'None', 'event_input_args': {'highlight_line_variable': 'current_line_number'}, 'buffer_name': ''})
call buffer_piets#set_piets({'function_args': 'None', 'event_input_args': {'piet_match_array_variable': 'file_lines', 'current_filename_variable': 'current_filename'}, 'buffer_name': ''})
config command ran successfully: info_source
opening buffer: vg_session_log for window: 2
opening buffer: vg_test_template for window: 2

switched order:

Tide started successfully
config command ran successfully: load_file
call set_highlight#for_breakpoint_and_diff({'function_args': 'None', 'event_input_args': 'None', 'buffer_name': ''})
config command ran successfully: set_highlight_for_breakpoint_and_diff

call buffer_breakpoint#set_highlight_line({'function_args': 'None', 'event_input_args': {'highlight_line_variable': 'current_line_number'}, 'buffer_name': ''})
call buffer_piets#set_piets({'function_args': 'None', 'event_input_args': 'None', 'buffer_name': ''})
config command ran successfully: info_source
opening buffer: vg_session_log for window: 1
opening buffer: vg_test_template for window: 1
COMMAND: vgdb.run_config_command("display_template", "vg_test_template")
opening buffer: vg_code for window: 1
COMMAND: vgdb.run_config_command("set_piets", "vg_code", "after_command")
call buffer_piets#set_piets({'function_args': 'None', 'event_input_args': {'piet_match_array_variable': 'file_lines', 'current_filename_variable': 'current_filename'}, 'buffer_name': 'vg_code'})
COMMAND: vgdb.run_config_command("set_highlight_line", "vg_code", "after_command")
call buffer_breakpoint#set_highlight_line({'function_args': 'None', 'event_input_args': {'highlight_line_variable': 'current_line_number'}, 'buffer_name': 'vg_code'})
