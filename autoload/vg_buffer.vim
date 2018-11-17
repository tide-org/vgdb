if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_buffer#default_display_buffer(buffer_name, command)
    let l:current_window_num = winnr()
    call vg_buffer#create_split(a:buffer_name)
    execute g:vg_py . ' vgdb.run_command_with_result("' . a:command . '")'
    call vg_buffer#window_by_bufname(a:buffer_name, 1)
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split(buffer_name, ...)
    let a:syntax = get(a:, 1, '')
    if vg_buffer#window_by_bufname(a:buffer_name, 1) == -1
        if vg_buffer#switch_to_empty_buffer() == -1
            call vg_buffer#create_split(a:buffer_name, a:syntax)
        else
            call vg_buffer#set_current_buffer_for_vgdb(a:buffer_name, a:syntax)
        endif
    endif
endfunction

function! vg_buffer#switch_to_empty_buffer()
    let l:empty_buffer_number = vg_buffer#find_empty_buffer_number()
    if l:empty_buffer_number != -1
        execute 'buffer ' . l:empty_buffer_number
        return l:empty_buffer_number
    endif
    return -1
endfunction

function! vg_buffer#remove_unlisted_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if !bufloaded(l:buffer_number) && !buflisted(l:buffer_number)
            exe 'bwipeout ' . l:buffer_number
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
    call vg_buffer#remove_unlisted_buffers()
    if vg_buffer#window_by_bufname(a:buffer_name, 0) == -1
        if g:vg_stack_buffers
            let l:existing_window = vg_buffer#first_window_by_valid_buffers()
            if l:existing_window != -1
                execute l:existing_window . 'wincmd w'
                new
            else
                exec g:vg_stack_buffer_window_width . 'vnew'
            endif
        else
            exec g:vg_stack_buffer_window_width . 'vnew'
        endif
        call vg_buffer#set_current_buffer_for_vgdb(a:buffer_name, a:syntax)
    endif
endfunction

function! vg_buffer#set_current_buffer_for_vgdb(buffer_name, ...)
    let a:syntax = get(a:, 1, '')
    setlocal buftype=nofile
    setlocal nonumber
    setlocal foldcolumn=0
    setlocal wrap
    setlocal noswapfile
    setlocal bufhidden=delete
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
    for buffer_name in g:vg_valid_buffers
        let l:window_number = vg_buffer#window_by_bufname(buffer_name)
        if l:window_number != -1
            return window_number
        endif
    endfor
    return -1
endfunction
