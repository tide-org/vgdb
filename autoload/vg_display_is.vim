if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display_is#is_scrolling_buffer(buffer_name)
    if has_key(g:vg_config_dictionary['buffers'][a:buffer_name], 'scrolling_buffer')
        if vg_helpers#is_value_true(g:vg_config_dictionary['buffers'][a:buffer_name]['scrolling_buffer'])
            return 1
        endif
    endif
    return 0
endfunction

function! vg_display_is#is_session_log_buffer(buffer_name)
    if a:buffer_name ==? g:vg_config_dictionary['settings']['logging']['session_buffer_name']
        return 1
    endif
    return 0
endfunction
