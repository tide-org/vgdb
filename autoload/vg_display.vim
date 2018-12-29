if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#display_buffer(buffer_name)
    let l:stripped_buffer_name = substitute(tolower(string(a:buffer_name)), "'", '', 'g')
    if l:stripped_buffer_name != '' && g:vg_config_dictionary != {}
        if has_key(g:vg_config_dictionary['buffers'], l:stripped_buffer_name)
            call vg_display#default_display_buffer_run_command(l:stripped_buffer_name)
         else
             echo "error: unable to find buffer in config: " . l:stripped_buffer_name
             echo "buffers: " . join(keys(g:vg_config_dictionary['buffers']), ",")
         endif
    endif
endfunction

function! vg_display#check_update_config_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_buffer_find#find_window_by_bufname(l:buffer_name) != -1
            call vg_display#display_buffer(l:buffer_name)
        endif
    endfor
endfunction

function! vg_display#default_display_buffer_run_command(buffer_name)
    let l:scrolling_buffer = vg_display_is#is_scrolling_buffer(a:buffer_name)
    call vg_display#default_display_buffer(a:buffer_name, l:scrolling_buffer)
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "on_startup", ""))
            call vg_display#display_buffer(l:buffer_name)
        endif
    endfor
endfunction

function! vg_display#update_buffers()
    call vg_buffer_do#remove_unlisted_buffers()
    call vg_display#check_update_config_buffers()
endfunction

function! vg_display#check_update_buffer(buffer_name)
    if vg_buffer_find#find_window_by_bufname(a:buffer_name) != -1
        call vg_display#display_buffer(a:buffer_name)
    endif
endfunction

function! vg_display#default_display_buffer(buffer_name, ...)
    let a:scrolling_buffer = get(a:, 1, 0)
    let l:current_window_num = winnr()
    let l:buffer_command = get(g:vg_config_dictionary['buffers'][a:buffer_name], "command", "")
    let l:python_command = vg_python#set_python_command(l:buffer_command, a:buffer_name)
    let l:primary_window = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'primary_window', 0)
    let l:is_primary_window = vg_helpers#is_value_true(l:primary_window)
    let l:language = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'language', "")
    let l:clear_buffer = !vg_display_is#is_session_log_buffer(a:buffer_name)
    call vg_buffer#switch_to_buffer(a:buffer_name, l:is_primary_window, l:language)
    call vg_display#run_config_events(a:buffer_name, 'before_command')
    call vg_python#check_run_python_command(l:python_command)
    call vg_buffer_do#write_array_to_buffer(a:buffer_name, l:clear_buffer)
    call vg_display#run_config_events(a:buffer_name, 'after_command')
    call vg_buffer_do#check_do_scroll_to_end(a:scrolling_buffer)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_display#run_config_events(buffer_name, event_name)
    let l:has_events = has_key(g:vg_config_dictionary["buffers"][a:buffer_name], "events")
    if l:has_events
        let l:event_commands = get(g:vg_config_dictionary["buffers"][a:buffer_name]["events"], a:event_name, [])
        for l:event_command in l:event_commands
            let l:event_command_name = l:event_command["command"]
            let l:python_command = vg_python#get_python_command_for_event(l:event_command_name, a:buffer_name, a:event_name)
            call vg_python#check_run_python_command(l:python_command)
        endfor
    endif
endfunction
