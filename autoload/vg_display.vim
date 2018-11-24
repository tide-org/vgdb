if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#default_display_buffer_run_command(buffer_name, command)
    call vg_display#default_display_buffer_python_method(a:buffer_name, 'vgdb.run_command_with_result("' . a:command . '", "'. a:buffer_name .'")')
endfunction

function! vg_display#default_display_buffer_python_method(buffer_name, python_method)
    let l:current_window_num = winnr()
    call vg_buffer#create_split(a:buffer_name)
    execute g:vg_py . ' ' . a:python_method
    call vg_display#write_array_to_buffer(a:buffer_name, 'g:vg_query_result')
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in g:vg_startup_buffers
        execute 'call vg_display#display_' . l:buffer_name . '()'
    endfor
endfunction

function! vg_display#update_buffers()
    call vg_buffer#remove_unlisted_buffers()
    call vg_display#check_update_registers()
    call vg_display#check_update_session_log()
    call vg_display#check_update_breakpoints()
    call vg_display#check_update_disassembly()
endfunction

function! vg_display#check_update_registers()
    if vg_buffer#window_by_bufname('vg_registers') != -1
        call vg_display#display_vg_registers()
    endif
endfunction

function! vg_display#check_update_session_log()
    if vg_buffer#window_by_bufname('vg_session_log') != -1
        call vg_display#display_vg_session_log()
    endif
endfunction

function! vg_display#check_update_breakpoints()
    if vg_buffer#window_by_bufname('vg_breakpoints') != -1
        call vg_display#display_vg_breakpoints()
    endif
endfunction

function! vg_display#check_update_disassembly()
    if vg_buffer#window_by_bufname('vg_disassembly') != -1
        call vg_display#display_vg_disassembly()
    endif
endfunction

function! vg_display#display_vg_session_log(...)
    let l:current_window_num = winnr()
    call vg_buffer#create_split('vg_session_log')
    call vg_display#write_array_to_buffer('vg_session_log', 'g:vg_full_query_result', 0)
    let g:vg_full_query_result = []
    execute 'normal! G'
    execute l:current_window_num . 'wincmd w'
endfunction

function! vg_display#display_vg_registers(...)
    call vg_display#default_display_buffer_run_command('vg_registers', 'info registers')
endfunction

function! vg_display#display_vg_breakpoints(...)
    call vg_display#default_display_buffer_run_command('vg_breakpoints', 'info breakpoints')
endfunction

function! vg_display#display_vg_disassembly(...)
    let l:current_window_num = winnr()
    call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split('vg_disassembly', 'asm')
    execute g:vg_py . ' vgdb.display_disassembly()'
    call vg_display#write_array_to_buffer('vg_disassembly', 'g:vg_query_result')
    if g:vg_current_breakpoint != '' | call vg_display#update_breakpoint_lines() | endif
    if len(g:vg_breakpoints) != 0 | call vg_display#update_breakpoint_piets() | endif
    exec l:current_window_num . 'wincmd w'
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
    for l:breakpoint in g:vg_breakpoints
        let l:line_counter = 1
        for l:line in g:vg_query_result
            if l:line =~ l:breakpoint
                execute "sign place 3 line=" . l:line_counter . " name=piet file=" . expand("%:p")
            endif
            let l:line_counter += 1
        endfor
    endfor
endfunction

function! vg_display#update_breakpoint_lines()
    let l:line_counter = 1
    let l:breakpoint_line = -1
    for l:line in g:vg_query_result
        if l:line =~ g:vg_current_breakpoint
            let l:breakpoint_line = l:line_counter
        endif
        let l:line_counter +=1
    endfor
    if l:breakpoint_line != -1
        execute "sign unplace 2"
        execute "sign place 2 line=" . l:breakpoint_line . " name=wholeline file=" . expand("%:p")
    endif
endfunction
