let s:initialised = 0
let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "vgdb/"
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"

function! vg_validate#fail()
    echohl WarningMsg | echomsg "Vgdb ERROR: Python interface cannot be loaded" | echohl None
    echohl WarningMsg | echomsg "Your version of Vim appears to be installed without the Python interface." | echohl None
    if !executable("python") | echohl WarningMsg | echomsg "You may also need to install Python." | echohl None | endif
endfunction

function! vg_validate#dependency_check()
    if s:initialised == 1 | return 0 | endif
    if has('python3')
        let g:vg_py = 'py3 '
        let g:vg_pyfile = 'py3file '
    else
        call vg_validate#fail()
        return 1
    endif
    call vg_validate#source_python_files()
    return 0
endfunction

function! vg_validate#validate_startup_buffer_names()
    if has_key(g:vg_config_dictionary, "buffers")
        let l:config_buffers = keys(g:vg_config_dictionary["buffers"])
        for l:buffer_name in l:config_buffers
            if index(l:config_buffers, l:buffer_name) == -1
                echoerr "Error: buffer " . l:buffer_name . " is not a valid buffer"
                return 1
            endif
        endfor
    endif
    return 0
endfunction

function! vg_validate#source_python_files()
    exec g:vg_pyfile . s:vgdbscriptdir . "vgdb.py"
endfunction
