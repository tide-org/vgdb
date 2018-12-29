if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_buffer_do#close_all_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_name in keys(g:vg_config_dictionary["buffers"])
        let l:buffer_number = bufnr(l:buffer_name)
        if index(l:buffer_numbers, l:buffer_number) != -1
            execute 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vg_buffer_do#remove_unlisted_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if !bufloaded(l:buffer_number) && !buflisted(l:buffer_number)
            execute 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vg_buffer_do#set_buffer_for_vgdb(buffer_name, ...)
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

function! vg_buffer_do#write_array_to_buffer(buffer_name, ...)
    let a:clear_buffer = get(a:, 1, 1)
    let l:array_cache = g:vg_config_dictionary["internal"]["buffer_caches"][a:buffer_name]
    call vg_buffer_find#find_window_by_bufname(a:buffer_name, 1)
    setlocal modifiable
    if a:clear_buffer
        silent! 1,$delete _
    endif
    silent! call setline('.', l:array_cache)
    setlocal nomodifiable
endfunction

function! vg_buffer_do#check_do_scroll_to_end(scrolling_buffer)
    if a:scrolling_buffer
        execute 'normal! G'
    endif
endfunction
