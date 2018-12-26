if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#display_buffer(buffer_name)
    let l:stripped_buffer_name = substitute(tolower(string(a:buffer_name)), "'", '', 'g')
    if l:stripped_buffer_name != '' && g:vg_config_dictionary != {}
        if has_key(g:vg_config_dictionary['buffers'], l:stripped_buffer_name)
            let l:buffer_command = vg_display#get_buffer_command(g:vg_config_dictionary['buffers'][l:stripped_buffer_name])
            call vg_display#default_display_buffer_run_command(l:stripped_buffer_name, l:buffer_command)
         else
             echo "unable to find buffer in config: " . l:stripped_buffer_name
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

function! vg_display#default_display_buffer_run_command(buffer_name, command)
    let l:python_command = vg_display#set_python_command_from_process_command(a:command, a:buffer_name)
    let l:scrolling_buffer = vg_display#is_scrolling_buffer(a:buffer_name)
    call vg_display#default_display_buffer(a:buffer_name, l:python_command, l:scrolling_buffer)
endfunction

function! vg_display#set_python_command_from_process_command(command, buffer_name)
    if len(a:command) > 0
        return 'vgdb.run_config_command("' . a:command . '", "'. a:buffer_name .'")'
    endif
    return ''
endfunction

function! vg_display#is_scrolling_buffer(buffer_name)
    if has_key(g:vg_config_dictionary['buffers'][a:buffer_name], 'scrolling_buffer')
        if vg_display#is_value_true(g:vg_config_dictionary['buffers'][a:buffer_name]['scrolling_buffer'])
            return 1
        endif
    endif
    return 0
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_display#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "on_startup", ""))
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

function! vg_display#is_value_true(test_value)
    let l:to_test = substitute(tolower(string(a:test_value)), "'", '', 'g')
    let l:true_list = [ "true", "1", "yes", "y" ]
    for l:true_item in l:true_list
        if l:true_item ==? l:to_test
           return 1
        endif
    endfor
    return 0
endfunction


function! vg_display#default_display_buffer(buffer_name, python_command, ...)
    let a:scrolling_buffer = get(a:, 1, 0)
    let l:current_window_num = winnr()
    let l:primary_window = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'primary_window', 0)
    let l:primary_window = vg_display#is_value_true(l:primary_window)
    let l:language = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'language', "")
    let l:clear_buffer = vg_display#get_clear_buffer(a:buffer_name)
    let l:buffer_input_variable = vg_display#get_buffer_input_variable(a:buffer_name)
    if l:primary_window
        call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split(a:buffer_name, l:language)
    else
        call vg_buffer#create_split(a:buffer_name)
    endif
    call vg_display#check_run_python_command(a:python_command)
    call vg_display#write_array_to_buffer(a:buffer_name, l:buffer_input_variable, l:clear_buffer)
    call vg_diff#check_do_buffer_diff(a:buffer_name)
    call vg_display#check_do_scroll_to_end(a:scrolling_buffer)
    if l:primary_window
        call vg_primary_window#update_highlight_lines(a:buffer_name)
        call vg_primary_window#update_piets(a:buffer_name)
    endif
    exec l:current_window_num . 'wincmd w'
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

function! vg_display#write_array_to_buffer(buffer_name, array_name, ...)
    let a:clear_buffer = get(a:, 1, 1)
    call vg_buffer#window_by_bufname(a:buffer_name, 1)
    setlocal modifiable
    if a:clear_buffer | silent! 1,$delete _ | endif
    execute "silent! call setline('.', " . a:array_name . '))'
    setlocal nomodifiable
endfunction

function! vg_display#get_buffer_input_variable(buffer_name)
    if vg_display#is_session_log_buffer(a:buffer_name)
        return g:vg_config_dictionary['settings']['logging']['buffer_input_variable']
    endif
    return g:vg_config_dictionary['settings']['buffers']['default_input_buffer_variable']
endfunction
