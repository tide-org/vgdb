let s:initialised = 0
let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "lib/vgdb/"

function! vg_validate#dependency_check()
    if s:initialised == 1 | return 0 | endif
    if vg_validate#validate_python() && has('signs')
        call vg_validate#source_python_files()
        return 0
    endif
    return 1
endfunction

function! vg_validate#validate_python()
    if has('python3')
        call vg_validate#set_python_globals()
        return 1
    endif
    call vg_validate#fail()
    return 0
endfunction

function! vg_validate#set_python_globals()
    let g:vg_py = 'py3 '
    let g:vg_pyfile = 'py3file '
endfunction

function! vg_validate#fail()
    echohl WarningMsg | echomsg "Vgdb ERROR: Python interface cannot be loaded" | echohl None
    echohl WarningMsg | echomsg "The version of Vim appears to be installed without the Python interface." | echohl None
    if !executable("python") | echohl WarningMsg | echomsg "You may also need to install Python." | echohl None | endif
    if !has("signs") | echohl WarningMsg | echomsg "The version of Vim install is also missing '+signs'" | echohl None | endif
endfunction

function! vg_validate#validate_startup_buffer_names()
    if has_key(g:vg_config_dictionary, "buffers")
        let l:config_buffers = keys(g:vg_config_dictionary["buffers"])
        for l:buffer_name in l:config_buffers
            if index(l:config_buffers, l:buffer_name) == -1
                echoerr "error: buffer " . l:buffer_name . " is not a valid buffer"
                return 1
            endif
        endfor
    endif
    return 0
endfunction

function! vg_validate#source_python_files()
    exec g:vg_pyfile . s:vgdbscriptdir . "vgdb.py"
endfunction
