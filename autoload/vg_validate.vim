let s:initialised = 0

function! vg_validate#fail()
    echohl WarningMsg | echomsg "Vgdb ERROR: Python interface cannot be loaded" | echohl None
    echohl WarningMsg | echomsg "Your version of Vim appears to be installed without the Python interface." | echohl None
    if !executable("python") | echohl WarningMsg | echomsg "You may also need to install Python." | echohl None | endif
endfunction

function! vg_validate#dependency_check()
    if s:initialised == 1 | return 0 | endif
    let g:vg_py = ''
    let pytest = 'python3'
    if has(pytest)
        if pytest == 'python3' | let g:vg_py = 'py3' | endif
    endif
    if g:vg_py == ''
        call vg_validate#fail()
        return 1
    endif
    return 0
endfunction

function! vg_validate#validate_startup_buffer_names()
    for l:buffer_name in g:vg_startup_buffers
        let l:vg_buffer_name = 'vg_' . l:buffer_name
        if index(g:vg_valid_buffers, l:vg_buffer_name) == -1
            echoerr "Error: buffer " . l:buffer_name . " is not a valid buffer in g:vg_startup_buffers"
            return 1
        endif
    endfor
    return 0
endfunction
