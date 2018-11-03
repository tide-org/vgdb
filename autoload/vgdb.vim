if !exists('g:Vgdb_Loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0
let g:Vgdb_PyVersion = 0
let g:query_result = []
let g:app_entrpoint = ''

function! vgdb#fail(feature)
    new
    setlocal buftype=nofile
    setlocal nonumber
    setlocal foldcolumn=0
    setlocal wrap
    setlocal noswapfile
    if a:feature == 'python'
        call append('$', 'Vgdb ERROR: Python interface cannot be loaded')
        call append('$', '')
        if !executable("python")
            call append('$', 'Your version of Vim appears to be installed without the Python interface. In ')
            call append('$', 'addition, you may need to install Python.')
        else
            call append('$', 'Your version of Vim appears to be installed without the Python interface.')
        endif
        call append('$', '')
        call append('$', "You are using a Unix-like operating system. Most, if not all, of the popular ")
        call append('$', "Linux package managers have Python-enabled Vim available. For example ")
        call append('$', "vim-gnome or vim-gtk on Ubuntu will get you everything you need.")
        call append('$', "")
        call append('$', "If you are compiling Vim from source, make sure you use the --enable-pythoninterp ")
        call append('$', "configure option. You will also need to install Python and the Python headers.")
        call append('$', "")
        call append('$', "If you are using OS X, MacVim will give you Python support by default.")
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
            "echohl WarningMsg | echomsg "Python " . g:Vgdb_PyVersion . " interface is not installed, using Python " . py_alternate . " instead" | echohl None
            let g:Vgdb_PyVersion = py_alternate
            if pytest == 'python3'
                let s:py = 'py3'
            else
                let s:py = 'py'
            endif
        endif
    endif
    if s:py == ''
        call vgdb#fail('python')
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
        "for line in g:query_result
        "    echohl WarningMsg | echomsg "line: " . line | echohl None
        "endfor
        echom "command run successfully: " . command
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_to_entrypoint(...)
    let command = get(a:000, 0, '')
    try
        execute s:py . ' vgdb.run_to_entrypoint()'
        echom "application started and broke at entrypoint: " . g:app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#source_python_files()
    exec s:py . "file " . s:scriptdir . "vgdb.py"
endfunction
