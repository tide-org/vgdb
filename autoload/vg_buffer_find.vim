if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_buffer_find#find_empty_buffer_number()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if bufname(l:buffer_number) == ''
            return l:buffer_number
        endif
    endfor
    return -1
endfunction

function! vg_buffer_find#find_window_to_split_for(split_for_main_window)
    if a:split_for_main_window
        return vg_buffer_find#find_current_window_number()
    endif
    return vg_buffer_find#find_first_window_by_valid_buffers()
endfunction

function! vg_buffer_find#find_current_window_number()
   let l:current_buffer = bufnr("%")
   let l:first_matching_window = bufwinnr(l:current_buffer)
   return l:first_matching_window
endfunction

function! vg_buffer_find#find_window_by_bufname(bufname, ...)
    let a:switch_window = get(a:, 1, 0)
    let l:bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
    let l:filtered_map = filter(l:bufmap, 'v:val[0] =~ a:bufname')
    if len(l:filtered_map) > 0
        let l:found_window = filtered_map[0][1]
        if a:switch_window
            execute l:found_window . 'wincmd w'
        endif
        return l:found_window
    else
        return -1
    endif
endfunction

function! vg_buffer_find#find_first_window_by_valid_buffers()
    for buffer_name in keys(g:vg_config_dictionary["buffers"])
       if !vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "primary_window", 0))
           let l:window_number = vg_buffer_find#find_window_by_bufname(buffer_name)
           if l:window_number != -1
               return window_number
           endif
        endif
    endfor
    return -1
endfunction
