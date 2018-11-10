if !exists('g:Vgdb_Loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0
let g:vg_python_version = 0
let g:vg_query_result = []
let g:vg_full_query_result = []
let g:vg_session_log = []
let g:vg_app_entrypoint = ''
let g:vg_last_register_result = []
let g:vg_binary_loaded = 0
let g:vg_symbols_loaded = 0
let g:vg_valid_buffers = ['vg_registers', 'vg_session_log']

function! vgdb#fail()
    new
    setlocal buftype=nofile
    setlocal nonumber
    setlocal foldcolumn=0
    setlocal wrap
    setlocal noswapfile
    call append('$', 'Vgdb ERROR: Python interface cannot be loaded')
    call append('$', '')
    call append('$', 'Your version of Vim appears to be installed without the Python interface.')
    if !executable("python")
        call append('$', 'You may also need to install Python.')
    endif
endfunction

function! vgdb#dependency_check()
    if s:initialised == 1
        return 1
    endif
    let s:py = ''
    if g:vg_python_version == 3
        let pytest = 'python3'
    else
        let pytest = 'python'
        let g:vg_python_version = 2
    endif
    if has(pytest)
        if pytest == 'python3'
            let s:py = 'py3'
        else
            let s:py = 'py'
        endif
    else
        let py_alternate = 5 - g:vg_python_version
        if py_alternate == 3
            let pytest = 'python3'
        else
            let pytest = 'python'
        endif
        if has(pytest)
            let g:vg_python_version = py_alternate
            if pytest == 'python3'
                let s:py = 'py3'
            else
                let s:py = 'py'
            endif
        endif
    endif
    if s:py == ''
        call vgdb#fail()
        return 0
    endif
    call vgdb#source_python_files()
    return 1
endfunction

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    if !vgdb#dependency_check()
        return 0
    endif
    if s:py == ''
        echohl WarningMsg | echomsg "Vgdb requires the Python interface to be installed. See :help Vgdb for more information." | echohl None
        return 0
    endif

    try
        execute s:py . ' vgdb = Vgdb()'
        execute s:py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_command(...)
    let command = get(a:000, 0, '')
    try
        execute s:py . ' vgdb.run_command_with_result("' . command . '")'
        echom "command ran successfully: " . command
        call vgdb#update_buffers()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_to_entrypoint(...)
    let command = get(a:000, 0, '')
    try
        execute s:py . ' vgdb.run_to_entrypoint()'
        echom "application started and halted at entrypoint: " . g:vg_app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#update_buffers()
    if vgdb#window_by_bufname('vg_registers', 0) != -1
        call vgdb#display_registers()
    endif
    if vgdb#window_by_bufname('vg_session_log', 0) != -1
        call vgdb#display_session_log()
    endif
endfunction

function! vgdb#display_session_log(...)
    let l:current_window_num = winnr()
    call vgdb#create_split('vg_session_log')
    call vgdb#window_by_bufname('vg_session_log', 1)
    call append(line('$'), g:vg_full_query_result)
    let g:vg_full_query_result = []
    execute 'normal! G'
    execute l:current_window_num . 'wincmd w'
endfunction

function! vgdb#display_registers(...)
    let l:current_window_num = winnr()
    call vgdb#create_split('vg_registers')
    execute s:py . ' vgdb.run_command_with_result("info registers")'
    call vgdb#window_by_bufname('vg_registers', 1)
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vgdb#remove_unlisted_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if !bufloaded(l:buffer_number) && !buflisted(l:buffer_number)
            exe 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vgdb#create_split(buffer_name)
    call vgdb#remove_unlisted_buffers()
    if vgdb#window_by_bufname(a:buffer_name, 0) == -1
        if g:vg_stack_buffers
            let l:existing_window = vgdb#first_window_by_valid_buffers()
            if l:existing_window != -1
                execute l:existing_window . 'wincmd w'
                new
            else
                60vnew
            endif
        else
            60vnew
        endif
        setlocal buftype=nofile
        setlocal nonumber
        setlocal foldcolumn=0
        setlocal wrap
        setlocal noswapfile
        setlocal bufhidden=delete
        exec 'file ' . a:buffer_name
    endif
endfunction

function! vgdb#window_by_bufname(bufname, switch_window)
    let l:bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
    let l:filtered_map = filter(bufmap, 'v:val[0] =~ a:bufname')
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

function! vgdb#first_window_by_valid_buffers()
    for buffer_name in g:vg_valid_buffers
        let l:window_number = vgdb#window_by_bufname(buffer_name, 0)
        if l:window_number != -1
            return window_number
        endif
    endfor
    return -1
endfunction

function! vgdb#source_python_files()
    exec s:py . "file " . s:scriptdir . "vgdb.py"
endfunction
