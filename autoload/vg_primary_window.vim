if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_primary_window#update_piets(buffer_name)
    let l:piet_match_array_variable = get(g:vg_config_dictionary["buffers"][a:buffer_name], "piet_match_array_variable", "")
    if l:piet_match_array_variable != ''
        let l:piet_match_list = g:vg_config_dictionary["variables"][l:piet_match_array_variable]
        if len(l:piet_match_list) > 0
            let l:buffer_input_variable_name = g:vg_config_dictionary["settings"]["buffers"]["default_input_buffer_variable"]
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
    endif
endfunction

function! vg_primary_window#update_highlight_lines(buffer_name)
    let l:highlight_line_variable = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'highlight_line_variable', '')
    if l:highlight_line_variable != '' && g:vg_config_dictionary['variables'][l:highlight_line_variable] != ''
        let l:buffer_input_variable_name = g:vg_config_dictionary["settings"]["buffers"]["default_input_buffer_variable"]
        let l:local_buffer_input_variable = []
        execute "let l:local_buffer_input_variable = " . l:buffer_input_variable_name
        let l:line_counter = 1
        let l:highlight_line = -1
        let l:current_frame_address = g:vg_config_dictionary['variables'][l:highlight_line_variable]
        for l:line in l:local_buffer_input_variable
            if l:line =~ l:current_frame_address
                let l:highlight_line = l:line_counter
            endif
            let l:line_counter +=1
        endfor
        if l:highlight_line != -1
            execute "sign unplace 2"
            execute "sign place 2 line=" . l:highlight_line . " name=wholeline file=" . expand("%:p")
        endif
        unlet l:local_buffer_input_variable
    endif
endfunction
