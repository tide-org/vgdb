if !exists('g:Vgdb_Loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:scriptdirpy = expand("<sfile>:h") . '/vgdb/'

" Display various error messages
function! vgdb#fail(feature) " {{{

    " create a new buffer
    new
    setlocal buftype=nofile
    setlocal nonumber
    setlocal foldcolumn=0
    setlocal wrap
    setlocal noswapfile

    " missing vim features
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
endfunction " }}}

function! vgdb#dependency_check()
    " don't recheck the second time 'round
    if s:initialized == 1
        return 1
    endif

    " choose a python version
    let s:py = ''
    if g:Vgdb_PyVersion == 3
        let pytest = 'python3'
    else
        let pytest = 'python'
        let g:Vgdb_PyVersion = 2
    endif

    " first test the requested version
    if has(pytest)
        if pytest == 'python3'
            let s:py = 'py3'
        else
            let s:py = 'py'
        endif

    " otherwise use the other version
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

    " test if we actually found a python version
    if s:py == ''
        call vgdb#fail('python')
        return 0
    endif

    call vgdb#load_python()
    return 1
endfunction

function! vgdb#open_gdb(...)
    let command_string = get(a:000, 0, '')
    let gdb_command = 'gdb ' . command_string
    let params = [gdb_command] + a:000[1:]
    call vgdb#print_list(params)
    echo join(params, "...")
    call call("vgdb#open", params )
endfunction

function! vgdb#print_list(...)
    echo a:0 . " items:"
    for s in a:000
        echon ' ' . join(s, "...")
    endfor
endfunction

function! vgdb#open(...)
    let command = get(a:000, 0, '')
    let vim_startup_commands = get(a:000, 1, [])
    let return_to_current  = get(a:000, 2, 0)
    let is_buffer  = get(a:000, 3, 1)

    if !vgdb#dependency_check()
        return 0
    endif

    " switch to buffer if needed
    if is_buffer && return_to_current
      let save_sb = &switchbuf
      sil set switchbuf=usetab
      let current_buffer = bufname("%")
    endif

    " bare minimum validation
    if s:py == ''
        echohl WarningMsg | echomsg "Vgdb requires the Python interface to be installed. See :help Vgdb for more information." | echohl None
        return 0
    endif
    if empty(command)
        echohl WarningMsg | echomsg "Invalid usage: no program path given. Use :Vgdb YOUR PROGRAM, e.g. :Vgdb ./testapp" | echohl None
        return 0
    else
        let cmd_args = split(command, '[^\\]\@<=\s')
        let cmd_args[0] = substitute(cmd_args[0], '\\ ', ' ', 'g')
        if !executable(cmd_args[0])
            echohl WarningMsg | echomsg "Not an executable: " . cmd_args[0] | echohl None
            return 0
        endif
    endif

    try
        execute s:py . ' ' . g:Vgdb_Var . ' = .Initialias()'
        execute s:py . ' ' . g:Vgdb_Var . ".Run()"
    catch
        echohl WarningMsg | echomsg "An error occurred: " . command | echohl None
        return 0
    endtry
endfunction

function! vgdb#load_python()
    exec s:py . "file " . s:scriptdirpy . "entrypoint.py"
"    exec s:py . "file " . s:scriptdirpy . "example.py"
endfunction
