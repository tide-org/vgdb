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
