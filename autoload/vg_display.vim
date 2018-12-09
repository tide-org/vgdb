if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#display_buffer(buffer_name)
    if a:buffer_name != '' && g:vg_config_dictionary != {}
        if has_key(g:vg_config_dictionary['buffers'], a:buffer_name)
            let l:buffer_command = vg_display#get_buffer_command(g:vg_config_dictionary['buffers'][a:buffer_name])
            call vg_display#default_display_buffer_run_command(a:buffer_name, l:buffer_command)
        endif
    endif
endfunction

function! vg_display#get_buffer_command(buffer_config)
    return get(a:buffer_config, 'command', '')
endfunction

function! vg_display#check_update_config_buffers()
    for l:buffer_name in g:vg_config_buffers
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
        return 'vgdb.run_command_with_result("' . a:command . '", "'. a:buffer_name .'")'
    endif
    return ''
endfunction

function! vg_display#is_scrolling_buffer(buffer_name)
    if has_key(g:vg_config_dictionary['buffers'][a:buffer_name], 'scrolling_buffer')
        if g:vg_config_dictionary['buffers'][a:buffer_name]['scrolling_buffer'] ==? 'true'
            return 1
        endif
    endif
    return 0
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in g:vg_config_startup_buffers
        call vg_display#display_buffer(l:buffer_name)
        " one edge case to refactor for
        if l:buffer_name == 'vg_disassembly'
            call vg_display#display_vg_disassembly()
        endif
    endfor
endfunction

function! vg_display#update_buffers()
    call vg_buffer#remove_unlisted_buffers()
    call vg_display#check_update_config_buffers()
    call vg_display#check_update_disassembly()
endfunction

function! vg_display#check_update_buffer(buffer_name)
    if vg_buffer#window_by_bufname(a:buffer_name) != -1
        call vg_display#display_buffer(a:buffer_name)
    endif
endfunction

function! vg_display#check_update_disassembly()
    if vg_buffer#window_by_bufname('vg_disassembly') != -1
        call vg_display#display_vg_disassembly()
    endif
endfunction

function! vg_display#is_session_log_buffer(buffer_name)
    if a:buffer_name ==? g:vg_config_dictionary['settings']['logging']['session_buffer_name']
        return 1
    endif
    return 0
endfunction

function! vg_display#get_buffer_input_variable(buffer_name)
    if vg_display#is_session_log_buffer(a:buffer_name)
        return g:vg_config_dictionary['settings']['logging']['buffer_input_variable']
    endif
    return g:vg_config_dictionary['settings']['buffers']['default_input_buffer_variable']
endfunction

function! vg_display#is_diff_buffer(buffer_name)
    let l:buffer_config = g:vg_config_dictionary['buffers'][a:buffer_name]
    if has_key(l:buffer_config, 'diff')
        if has_key(l:buffer_config['diff'], 'show_diff')
            if l:buffer_config['diff']['show_diff'] =~ 'true'
                return 1
            endif
        endif
    endif
   return 0
endfunction

function! vg_display#check_do_buffer_diff(buffer_name, buffer_input_variable)
    if vg_display#is_diff_buffer(a:buffer_name)
         let l:cache_variable = vg_display#get_buffer_input_cache_variable(a:buffer_name)
         let l:local_cache_copy = []
         execute "if !exists('" . l:cache_variable . "') | let " . l:cache_variable . " = [] | endif"
         execute 'let l:local_cache_copy = ' . l:cache_variable
         let l:local_buffer_input = []
         execute 'let l:local_buffer_input = ' . a:buffer_input_variable
         call vg_display#do_diff_highlight(a:buffer_name, l:local_cache_copy, l:local_buffer_input)
         execute 'let ' . l:cache_variable . ' = ' . a:buffer_input_variable
         unlet l:local_cache_copy
         unlet l:local_buffer_input
    endif
endfunction

function! vg_display#do_diff_highlight(buffer_name, cached_lines, current_lines)
    execute "sign unplace * file=" . expand("%:p")
    if len(a:cached_lines) > 0
       if len(a:cached_lines) <= len(a:current_lines)
          let l:line_index = 0
          for l:line in a:current_lines
              if l:line !=? a:cached_lines[l:line_index]
                  call vg_display#set_diff_line(l:line_index + 1)
              endif
              let l:line_index += 1
           endfor
       endif
    endif
endfunction

function! vg_display#get_buffer_input_cache_variable(buffer_name)
    let l:buffer_config = g:vg_config_dictionary['buffers'][a:buffer_name]
    if has_key(l:buffer_config, 'diff')
        if has_key(l:buffer_config['diff'], 'buffer_input_cache_variable')
             return l:buffer_config['diff']['buffer_input_cache_variable']
        endif
    endif
    return ''
endfunction

function! vg_display#default_display_buffer(buffer_name, python_command, ...)
    let a:scrolling_buffer = get(a:, 1, 0)
    let l:current_window_num = winnr()
    let l:buffer_input_variable = vg_display#get_buffer_input_variable(a:buffer_name)
    call vg_buffer#create_split(a:buffer_name)
    call vg_display#check_run_python_command(a:python_command)
    let l:clear_buffer = vg_display#get_clear_buffer(a:buffer_name)
    call vg_display#write_array_to_buffer(a:buffer_name, l:buffer_input_variable, l:clear_buffer)
    call vg_display#check_do_buffer_diff(a:buffer_name, l:buffer_input_variable)
    call vg_display#check_do_scroll_to_end(a:scrolling_buffer)
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

function! vg_display#display_vg_disassembly(...)
    let l:current_window_num = winnr()
    call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split('vg_disassembly', 'asm')
    execute g:vg_py . 'vgdb.display_disassembly()'
    call vg_display#write_array_to_buffer('vg_disassembly', vg_display#get_default_input_buffer_variable())
    if g:vg_current_frame_address != '' | call vg_display#update_breakpoint_lines() | endif
    if len(g:vg_breakpoints) != 0 | call vg_display#update_breakpoint_piets() | endif
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_display#get_default_input_buffer_variable()
    return g:vg_config_dictionary["settings"]["buffers"]["default_input_buffer_variable"]
endfunction

function! vg_display#write_array_to_buffer(buffer_name, array_name, ...)
    let a:clear_buffer = get(a:, 1, 1)
    call vg_buffer#window_by_bufname(a:buffer_name, 1)
    setlocal modifiable
    if a:clear_buffer | silent! 1,$delete _ | endif
    execute "silent! call setline('.', " . a:array_name . '))'
    setlocal nomodifiable
endfunction

function! vg_display#update_breakpoint_piets()
    let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
    let l:local_buffer_input_variable = []
    execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
    for l:breakpoint in g:vg_breakpoints
        let l:line_counter = 1
        for l:line in l:local_buffer_input_variable
            if l:line =~ l:breakpoint
                execute "sign place 3 line=" . l:line_counter . " name=piet file=" . expand("%:p")
            endif
            let l:line_counter += 1
        endfor
    endfor
    unlet l:local_buffer_input_variable
endfunction

function! vg_display#update_breakpoint_lines()
    let l:breakpoint_line = vg_display#find_breakpoint_line()
    call vg_display#set_breakpoint_line(l:breakpoint_line)
endfunction

function! vg_display#set_diff_line(diff_line)
    if a:diff_line > 0
        execute "sign place 3 line=" . a:diff_line . " name=wholeline file=" . expand("%:p")
    endif
endfunction

function! vg_display#set_breakpoint_line(breakpoint_line)
    if a:breakpoint_line != -1
        execute "sign unplace 2"
        execute "sign place 2 line=" . a:breakpoint_line . " name=wholeline file=" . expand("%:p")
    endif
endfunction

function! vg_display#find_breakpoint_line()
    let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
    let l:local_buffer_input_variable = []
    execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
    let l:line_counter = 1
    let l:breakpoint_line = -1
    for l:line in l:local_buffer_input_variable
        if l:line =~ g:vg_current_frame_address
            let l:breakpoint_line = l:line_counter
        endif
        let l:line_counter +=1
    endfor
    unlet l:local_buffer_input_variable
    return l:breakpoint_line
endfunction
