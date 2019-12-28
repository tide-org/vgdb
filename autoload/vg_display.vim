if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#check_update_config_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_buffer_find#find_window_by_bufname(l:buffer_name) != -1
            call vg_display#display_buffer(l:buffer_name)
        endif
    endfor
endfunction

function! vg_display#display_buffer(buffer_name)
    let l:stripped_buffer_name = substitute(tolower(string(a:buffer_name)), "'", '', 'g')
    if l:stripped_buffer_name != '' && g:vg_config_dictionary != {}
        if has_key(g:vg_config_dictionary['buffers'], l:stripped_buffer_name)
            call vg_display#default_display_buffer(a:buffer_name)
         endif
    endif
endfunction

function! vg_display#default_display_buffer(buffer_name)
    let l:current_window_num = winnr()

    let l:primary_window = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'primary_window', 0)
    let l:is_primary_window = vg_helpers#is_value_true(l:primary_window)
    let l:language = get(g:vg_config_dictionary['buffers'][a:buffer_name], 'language', "")
    let l:clear_buffer = !vg_display_is#is_session_log_buffer(a:buffer_name)
    let l:line_numbers = vg_display_is#is_buffer_using_line_numbers(a:buffer_name)
    let l:using_filename = vg_display_is#is_buffer_using_filename(a:buffer_name)
    call vg_buffer#switch_to_buffer(a:buffer_name, l:is_primary_window, l:language, l:line_numbers)

    if !l:using_filename
        call vg_buffer_do#write_array_to_buffer(a:buffer_name, l:clear_buffer)
    endif

    let l:scrolling_buffer = vg_display_is#is_scrolling_buffer(a:buffer_name)
    call vg_buffer_do#check_do_scroll_to_end(l:scrolling_buffer)

    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_display#open_startup_buffers()
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        if vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "on_startup", ""))
            if vg_helpers#is_value_true(get(g:vg_config_dictionary["buffers"][l:buffer_name], "use_buffer_cache", 1))
              call vg_display#default_display_buffer(l:buffer_name)
            endif
        endif
    endfor
endfunction
