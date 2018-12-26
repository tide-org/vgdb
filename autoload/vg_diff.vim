if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_diff#check_do_buffer_diff(buffer_name)
    if vg_diff#is_diff_buffer(a:buffer_name)
        let l:buffer_input_value = vg_diff#get_buffer_input_value(a:buffer_name)
        let l:buffer_input_cache_variable_name = vg_diff#get_buffer_input_cache_variable_name(a:buffer_name)
        let l:buffer_input_cache_value = vg_diff#get_buffer_input_cache_value(a:buffer_name)
        execute "sign unplace * file=" . expand("%:p")
        if len(l:buffer_input_cache_value) > 0 && len(l:buffer_input_cache_value) <= len(l:buffer_input_value)
            let l:line_index = 0
            for l:line in l:buffer_input_value
                if l:line !=? l:buffer_input_cache_value[l:line_index]
                    let l:line_number = l:line_index + 1
                    execute "sign place 3 line=" . l:line_number . " name=wholeline file=" . expand("%:p")
                endif
                let l:line_index += 1
            endfor
        endif
        if l:buffer_input_cache_variable_name != ''
            let g:vg_config_dictionary["variables"][l:buffer_input_cache_variable_name] = l:buffer_input_value
        endif
    endif
endfunction

function! vg_diff#get_buffer_input_cache_value(buffer_name)
    let l:buffer_config = g:vg_config_dictionary['buffers'][a:buffer_name]
    if has_key(l:buffer_config, 'diff') && has_key(l:buffer_config['diff'], 'buffer_input_cache_variable')
         let l:cache_variable = l:buffer_config['diff']['buffer_input_cache_variable']
         return g:vg_config_dictionary["variables"][l:cache_variable]
    endif
    return []
endfunction

function! vg_diff#get_buffer_input_cache_variable_name(buffer_name)
    let l:buffer_config = g:vg_config_dictionary['buffers'][a:buffer_name]
    if has_key(l:buffer_config, 'diff')
        return get(l:buffer_config['diff'], 'buffer_input_cache_variable', '')
    endif
    return ''
endfunction

function! vg_diff#get_buffer_input_value(buffer_name)
    if vg_display#is_session_log_buffer(a:buffer_name)
        let l:input_variable_name = g:vg_config_dictionary['settings']['logging']['buffer_input_variable']
    else
        let l:input_variable_name =  g:vg_config_dictionary['settings']['buffers']['default_input_buffer_variable']
    endif
    execute "let l:local_buffer_input_value = " . l:input_variable_name
    return l:local_buffer_input_value
endfunction

function! vg_diff#is_diff_buffer(buffer_name)
    let l:buffer_config = g:vg_config_dictionary['buffers'][a:buffer_name]
    if has_key(l:buffer_config, 'diff') &&  has_key(l:buffer_config['diff'], 'show_diff') && l:buffer_config['diff']['show_diff'] =~ 'true'
        return 1
    endif
   return 0
endfunction
