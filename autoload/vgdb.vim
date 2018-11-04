if !exists('g:Vgdb_Loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0
let g:Vgdb_PyVersion = 0
let g:query_result = []
let g:app_entrpoint = ''
let g:last_register_result = []


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
    if g:Vgdb_PyVersion == 3
        let pytest = 'python3'
    else
        let pytest = 'python'
        let g:Vgdb_PyVersion = 2
    endif
    if has(pytest)
        if pytest == 'python3'
            let s:py = 'py3'
        else
            let s:py = 'py'
        endif
    else
        let py_alternate = 5 - g:Vgdb_PyVersion
        if py_alternate == 3
            let pytest = 'python3'
        else
            let pytest = 'python'
        endif
        if has(pytest)
            let g:Vgdb_PyVersion = py_alternate
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
        echom "application started and halted at entrypoint: " . g:app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#update_buffers()
    if vgdb#window_by_bufname('vg_registers', 0) != -1
        call vgdb#display_registers()
    endif
endfunction

function! vgdb#display_registers(...)
    let l:current_window_num = winnr()
    if vgdb#window_by_bufname('vg_registers', 1) == -1
        60vnew
        setlocal buftype=nofile
        setlocal nonumber
        setlocal foldcolumn=0
        setlocal wrap
        setlocal noswapfile
        setlocal bufhidden=delete
        file vg_registers
    else
        silent 1,$d _
    endif
    execute s:py . ' vgdb.run_command_with_result("info registers")'
    call append(line('$'), g:query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vgdb#window_by_bufname(bufname, switch_window)
    let bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
    let filtered_map = filter(bufmap, 'v:val[0] =~ a:bufname')
    if len(filtered_map) > 0
        let thewindow = filtered_map[0][1]
        if a:switch_window
            execute thewindow . 'wincmd w'
        endif
        return thewindow
    else
        return -1
    endif
endfunction

function! vgdb#source_python_files()
    exec s:py . "file " . s:scriptdir . "vgdb.py"
endfunction
