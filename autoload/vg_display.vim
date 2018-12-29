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

function! vg_display#get_buffer_command(buffer_config)
    return get(a:buffer_config, 'command', '')
endfunction

function! vg_display#check_update_config_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_buffer#window_by_bufname(l:buffer_name) != -1
            call vg_display#display_buffer(l:buffer_name)
        endif
    endfor
endfunction

function! vg_display#default_display_buffer_run_command(buffer_name)
    let l:scrolling_buffer = vg_display#is_scrolling_buffer(a:buffer_name)
    call vg_display#default_display_buffer(a:buffer_name, l:scrolling_buffer)
endfunction

function! vg_display#set_python_command(command, buffer_name)
    if len(a:command) > 0
        return 'vgdb.run_config_command("' . a:command . '", "'. a:buffer_name .'")'
    endif
    return ''
endfunction

function! vg_display#is_scrolling_buffer(buffer_name)
    if has_key(g:vg_config_dictionary['buffers'][a:buffer_name], 'scrolling_buffer')
        if vg_helpers#is_value_true(g:vg_config_dictionary['buffers'][a:buffer_name]['scrolling_buffer'])
            return 1
        endif
    endif
    return 0
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "on_startup", ""))
            call vg_display#display_buffer(l:buffer_name)
        endif
    endfor
endfunction

function! vg_display#update_buffers()
    call vg_buffer#remove_unlisted_buffers()
    call vg_display#check_update_config_buffers()
endfunction

function! vg_display#check_update_buffer(buffer_name)
    if vg_buffer#window_by_bufname(a:buffer_name) != -1
        call vg_display#display_buffer(a:buffer_name)
    endif
endfunction

function! vg_display#is_session_log_buffer(buffer_name)
    if a:buffer_name ==? g:vg_config_dictionary['settings']['logging']['session_buffer_name']
        return 1
    endif
    return 0
endfunction

function! vg_display#default_display_buffer(buffer_name, ...)
    let a:scrolling_buffer = get(a:, 1, 0)
    let l:current_window_num = winnr()
    let l:buffer_command = vg_display#get_buffer_command(g:vg_config_dictionary['buffers'][a:buffer_name])
    let l:python_command = vg_display#set_python_command(l:buffer_command, a:buffer_name)
    let l:primary_window = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'primary_window', 0)
    let l:is_primary_window = vg_helpers#is_value_true(l:primary_window)
    let l:language = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'language', "")
    let l:clear_buffer = vg_display#get_clear_buffer(a:buffer_name)
    call vg_buffer#switch_to_buffer(a:buffer_name, l:is_primary_window, l:language)
    call vg_display#run_config_events(a:buffer_name, 'before_command')
    call vg_display#check_run_python_command(l:python_command)
    call vg_display#write_array_to_buffer(a:buffer_name, l:clear_buffer)
    call vg_display#run_config_events(a:buffer_name, 'after_command')
    call vg_display#check_do_scroll_to_end(a:scrolling_buffer)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_display#run_config_events(buffer_name, event_name)
    let l:has_events = has_key(g:vg_config_dictionary["buffers"][a:buffer_name], "events")
    if l:has_events
        let l:event_commands = get(g:vg_config_dictionary["buffers"][a:buffer_name]["events"], a:event_name, [])
        for l:event_command in l:event_commands
            let l:event_command_name = l:event_command["command"]
            let l:python_command = vg_display#get_python_command_for_event(l:event_command_name, a:buffer_name, a:event_name)
            call vg_display#check_run_python_command(l:python_command)
        endfor
    endif
endfunction

function! vg_display#get_python_command_for_event(command_name, buffer_name, event_name)
    if len(a:command_name) > 0
        let l:return_string = 'vgdb.run_config_command("' . a:command_name . '", "'. a:buffer_name . '", "' . a:event_name . '")'
        return l:return_string
    endif
    return ''
endfunction


function! vg_display#check_do_scroll_to_end(scrolling_buffer)
    if a:scrolling_buffer
        execute 'normal! G'
    endif
endfunction

function! vg_display#check_run_python_command(python_command)
    if len(a:python_command) > 0
        execute g:vg_py . a:python_command
    endif
endfunction

function! vg_display#get_clear_buffer(buffer_name)
    if vg_display#is_session_log_buffer(a:buffer_name)
        return 0
    endif
    return 1
endfunction

function! vg_display#write_array_to_buffer(buffer_name, ...)
    let a:clear_buffer = get(a:, 1, 1)
    let l:array_cache = g:vg_config_dictionary["internal"]["buffer_caches"][a:buffer_name]
    call vg_buffer#window_by_bufname(a:buffer_name, 1)
    setlocal modifiable
    if a:clear_buffer | silent! 1,$delete _ | endif
    silent! call setline('.', l:array_cache)
    setlocal nomodifiable
endfunction
