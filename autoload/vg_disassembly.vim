if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_disassembly#update_piets(buffer_name)
    let l:piet_match_array_variable = g:vg_config_dictionary["buffers"][a:buffer_name]["piet_match_array_variable"]
    let l:piet_match_list = g:vg_config_dictionary["variables"][l:piet_match_array_variable]
    if len(l:piet_match_list) > 0
        let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
        let l:local_buffer_input_variable = []
        execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
        for l:piet_match in l:piet_match_list
            let l:line_counter = 1
            for l:line in l:local_buffer_input_variable
                if l:line =~ l:piet_match
                    execute "sign place 3 line=" . l:line_counter . " name=piet file=" . expand("%:p")
                endif
                let l:line_counter += 1
            endfor
        endfor
        unlet l:local_buffer_input_variable
    endif
endfunction

function! vg_disassembly#update_highlight_lines(highlight_line_variable)
    let l:highlight_line = vg_disassembly#find_highlight_line(a:highlight_line_variable)
    call vg_disassembly#set_highlight_line(l:highlight_line)
endfunction

function! vg_disassembly#set_highlight_line(highlight_line)
    if a:highlight_line != -1
        execute "sign unplace 2"
        execute "sign place 2 line=" . a:highlight_line . " name=wholeline file=" . expand("%:p")
    endif
endfunction

function! vg_disassembly#find_highlight_line(highlight_line_variable)
    let l:buffer_input_variable_name = vg_display#get_default_input_buffer_variable()
    let l:local_buffer_input_variable = []
    execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
    let l:line_counter = 1
    let l:breakpoint_line = -1
    let l:current_frame_address = g:vg_config_dictionary['variables'][a:highlight_line_variable]
    for l:line in l:local_buffer_input_variable
        if l:line =~ l:current_frame_address
            let l:breakpoint_line = l:line_counter
        endif
        let l:line_counter +=1
    endfor
    unlet l:local_buffer_input_variable
    return l:breakpoint_line
endfunction
