if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_buffer#switch_to_buffer(buffer_name, primary_window, syntax, line_numbers)
    if a:primary_window
      call vg_buffer#switch_to_primary_window(a:buffer_name, a:syntax, a:line_numbers)
    else
        call vg_buffer#create_split(a:buffer_name, a:syntax)
    endif
endfunction

function! vg_buffer#switch_to_primary_window(buffer_name, syntax, line_numbers)
    if vg_buffer_find#find_window_by_bufname(a:buffer_name, 1) == -1
       if vg_buffer#switch_to_empty_buffer() == -1
            call vg_buffer#create_split(a:buffer_name, a:syntax, 1, a:line_numbers)
       else
          call vg_buffer_do#set_buffer_for_vgdb(a:buffer_name, a:syntax, a:line_numbers)
       endif
    endif
endfunction

function! vg_buffer#switch_to_empty_buffer()
    let l:empty_buffer_number = vg_buffer_find#find_empty_buffer_number()
    if l:empty_buffer_number != -1
        let l:empty_buffer_window_id = win_findbuf(l:empty_buffer_number)
        call win_gotoid(l:empty_buffer_window_id[0])
        return l:empty_buffer_number
    endif
    return -1
endfunction

function! vg_buffer#create_split(buffer_name, ...)
    let l:syntax = get(a:, 1, '')
    let l:split_for_main_window = get(a:, 2, 0)
    let l:line_numbers = get(a:, 3, 0)
    call vg_buffer_do#remove_unlisted_buffers()
    let l:existing_window = vg_buffer_find#find_window_to_split_for(l:split_for_main_window)
    if vg_buffer_find#find_window_by_bufname(a:buffer_name, 0) == -1
        call vg_buffer#split_windows_for_existing_or_new(l:existing_window)
        call vg_buffer_do#set_buffer_for_vgdb(a:buffer_name, l:syntax, l:line_numbers)
    endif
endfunction

function! vg_buffer#split_windows_for_existing_or_new(existing_window)
    let l:window_width = g:vg_config_dictionary['settings']['buffers']['stack_buffer_window_width']
    let l:stack_buffers = vg_helpers#is_value_true(g:vg_config_dictionary['settings']['buffers']['stack_buffers_by_default'])
    if l:stack_buffers && a:existing_window != -1
         execute a:existing_window . 'wincmd w'
         new
    else
        execute l:window_width . 'vnew'
    endif
endfunction
