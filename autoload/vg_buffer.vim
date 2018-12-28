if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_buffer#close_all_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        let l:buffer_number = bufnr(l:buffer_name)
        if index(l:buffer_numbers, l:buffer_number) != -1
            execute 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vg_buffer#switch_to_buffer(buffer_name, ...)
    let a:primary_window = get(a:, 1, 0)
    let a:syntax = get(a:, 2, '')
    if a:primary_window
       if vg_buffer#window_by_bufname(a:buffer_name, 1) == -1
           if vg_buffer#switch_to_empty_buffer() == -1
               call vg_buffer#create_split(a:buffer_name, a:syntax, 1)
           else
               call vg_buffer#set_current_buffer_for_vgdb(a:buffer_name, a:syntax)
           endif
       endif
    else
        call vg_buffer#create_split(a:buffer_name, a:syntax)
    endif
endfunction

function! vg_buffer#switch_to_empty_buffer()
    let l:empty_buffer_number = vg_buffer#find_empty_buffer_number()
    if l:empty_buffer_number != -1
        let l:empty_buffer_window_id = win_findbuf(l:empty_buffer_number)
        call win_gotoid(l:empty_buffer_window_id[0])
        return l:empty_buffer_number
    endif
    return -1
endfunction

function! vg_buffer#remove_unlisted_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if !bufloaded(l:buffer_number) && !buflisted(l:buffer_number)
            execute 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vg_buffer#find_empty_buffer_number()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if bufname(l:buffer_number) == ''
            return l:buffer_number
        endif
    endfor
    return -1
endfunction

function! vg_buffer#create_split(buffer_name, ...)
    let a:syntax = get(a:, 1, '')
    let a:split_for_main_window = get(a:, 2, 0)
    call vg_buffer#remove_unlisted_buffers()
    let l:existing_window = vg_buffer#get_window_to_split_for(a:split_for_main_window)
    if vg_buffer#window_by_bufname(a:buffer_name, 0) == -1
        call vg_buffer#split_windows_for_existing_or_new(l:existing_window)
        call vg_buffer#set_current_buffer_for_vgdb(a:buffer_name, a:syntax)
    endif
endfunction

function! vg_buffer#split_windows_for_existing_or_new(existing_window)
    let l:window_width = g:vg_config_dictionary['settings']['buffers']['stack_buffer_window_width']
    let l:stack_buffers = g:vg_config_dictionary['settings']['buffers']['stack_buffers_by_default']
    if l:stack_buffers
        if a:existing_window != -1
            execute a:existing_window . 'wincmd w'
            new
        else
            exec l:window_width . 'vnew'
        endif
    else
        exec l:window_width . 'vnew'
    endif
endfunction

function! vg_buffer#get_window_to_split_for(split_for_main_window)
    if a:split_for_main_window
        return vg_buffer#get_current_window_number()
    endif
    return vg_buffer#first_window_by_valid_buffers()
endfunction

function! vg_buffer#get_current_window_number()
   let l:current_buffer = bufnr("%")
   let l:first_matching_window = bufwinnr(l:current_buffer)
   return l:first_matching_window
endfunction

function! vg_buffer#set_current_buffer_for_vgdb(buffer_name, ...)
    let a:syntax = get(a:, 1, '')
    setlocal buftype=nofile
    setlocal nonumber
    setlocal foldcolumn=0
    setlocal wrap
    setlocal noswapfile
    setlocal bufhidden=delete
    setlocal nomodifiable
    exec 'setlocal syntax=' . a:syntax
    silent exec 'file ' . a:buffer_name
endfunction

function! vg_buffer#window_by_bufname(bufname, ...)
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

function! vg_buffer#first_window_by_valid_buffers()
    for buffer_name in keys(g:vg_config_dictionary["buffers"])
       if !vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "primary_window", 0))
           let l:window_number = vg_buffer#window_by_bufname(buffer_name)
           if l:window_number != -1
               return window_number
           endif
        endif
    endfor
    return -1
endfunction
