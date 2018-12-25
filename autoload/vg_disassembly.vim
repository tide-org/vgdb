if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_disassembly#check_update_disassembly()
    if vg_buffer#window_by_bufname('vg_disassembly') != -1
        call vg_disassembly#display_vg_disassembly()
    endif
endfunction

function! vg_disassembly#display_vg_disassembly(...)
    let l:current_window_num = winnr()
    call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split('vg_disassembly', 'asm')
    execute g:vg_py . 'vgdb.display_disassembly()'
    call vg_display#write_array_to_buffer('vg_disassembly', vg_display#get_default_input_buffer_variable())
    if g:vg_config_dictionary['variables']['current_frame_address'] != '' | call vg_disassembly#update_breakpoint_lines() | endif
    let l:breakpoints = g:vg_config_dictionary["variables"]["breakpoints"]
    if len(l:breakpoints) != 0 | call vg_disassembly#update_breakpoint_piets() | endif
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_disassembly#update_breakpoint_piets()
    let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
    let l:local_buffer_input_variable = []
    execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
    let l:breakpoints = g:vg_config_dictionary["variables"]["breakpoints"]
    for l:breakpoint in l:breakpoints
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

function! vg_disassembly#update_breakpoint_lines()
    let l:breakpoint_line = vg_disassembly#find_breakpoint_line()
    call vg_disassembly#set_breakpoint_line(l:breakpoint_line)
endfunction

function! vg_disassembly#set_breakpoint_line(breakpoint_line)
    if a:breakpoint_line != -1
        execute "sign unplace 2"
        execute "sign place 2 line=" . a:breakpoint_line . " name=wholeline file=" . expand("%:p")
    endif
endfunction

function! vg_disassembly#find_breakpoint_line()
    let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
    let l:local_buffer_input_variable = []
    execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
    let l:line_counter = 1
    let l:breakpoint_line = -1
    let l:current_frame_address = g:vg_config_dictionary['variables']['current_frame_address']
    for l:line in l:local_buffer_input_variable
        if l:line =~ l:current_frame_address
            let l:breakpoint_line = l:line_counter
        endif
        let l:line_counter +=1
    endfor
    unlet l:local_buffer_input_variable
    return l:breakpoint_line
endfunction
