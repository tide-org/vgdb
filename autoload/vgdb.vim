if !exists('g:Vgdb_Loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:scriptdirpy = expand("<sfile>:h") . '/vgdb/'
let s:initialised = 0
let g:Vgdb_PyVersion = 0

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
            echohl WarningMsg | echomsg "Python " . g:Vgdb_PyVersion . " interface is not installed, using Python " . py_alternate . " instead" | echohl None
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

function! vgdb#open(...)
    let command = get(a:000, 0, '')
    let vim_startup_commands = get(a:000, 1, [])
    let return_to_current  = get(a:000, 2, 0)
    let is_buffer  = get(a:000, 3, 1)

    if !vgdb#dependency_check()
        return 0
    endif
    if s:py == ''
        echohl WarningMsg | echomsg "Vgdb requires the Python interface to be installed. See :help Vgdb for more information." | echohl None
        return 0
    endif

    try
        execute s:py . ' test("5")'
    catch
        echohl WarningMsg | echomsg "An error occurred: " . command | echohl None
        return 0
    endtry
endfunction

function! vgdb#source_python_files()
    exec s:py . "file " . s:scriptdir . "vgdb.py"
endfunction
