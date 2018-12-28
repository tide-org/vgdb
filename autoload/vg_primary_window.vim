if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_primary_window#update_piets(buffer_name)
    let l:piet_match_array_variable = get(g:vg_config_dictionary["buffers"][a:buffer_name], "piet_match_array_variable", "")
    if l:piet_match_array_variable != ''
        let l:piet_match_list = g:vg_config_dictionary["variables"][l:piet_match_array_variable]
        if len(l:piet_match_list) > 0
            for l:piet_match in l:piet_match_list
                let l:line_counter = 1
                for l:line in g:vg_config_dictionary["internal"]["buffer_caches"][a:buffer_name]
                    if l:line =~ l:piet_match
                        execute "sign place 3 line=" . l:line_counter . " name=piet file=" . expand("%:p")
                    endif
                    let l:line_counter += 1
                endfor
            endfor
        endif
    endif
endfunction

function! vg_primary_window#update_highlight_lines(buffer_name)
    let l:highlight_line_variable = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'highlight_line_variable', '')
    if l:highlight_line_variable != '' && g:vg_config_dictionary['variables'][l:highlight_line_variable] != ''
        let l:local_buffer_input_variable = []
        let l:line_counter = 1
        let l:highlight_line = -1
        let l:line_to_match = g:vg_config_dictionary['variables'][l:highlight_line_variable]
        for l:line in g:vg_config_dictionary["internal"]["buffer_caches"][a:buffer_name]
            if l:line =~ l:line_to_match
                let l:highlight_line = l:line_counter
            endif
            let l:line_counter +=1
        endfor
        if l:highlight_line != -1
            execute "sign unplace 2"
            execute "sign place 2 line=" . l:highlight_line . " name=wholeline file=" . expand("%:p")
        endif
    endif
endfunction
