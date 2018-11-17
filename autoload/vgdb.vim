if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "vgdb/"
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0

function! vgdb#fail()
    echohl WarningMsg | echomsg "Vgdb ERROR: Python interface cannot be loaded" | echohl None
    echohl WarningMsg | echomsg "Your version of Vim appears to be installed without the Python interface." | echohl None
    if !executable("python") | echohl WarningMsg | echomsg "You may also need to install Python." | echohl None | endif
endfunction

function! vgdb#dependency_check()
    if s:initialised == 1 | return 0 | endif
    let g:vg_py = ''
    let pytest = 'python3'
    if has(pytest)
        if pytest == 'python3' | let g:vg_py = 'py3' | endif
    endif
    if g:vg_py == ''
        call vgdb#fail()
        return 1
    endif
    call vgdb#source_python_files()
    return 0
endfunction

function! vgdb#validate_startup_buffer_names()
    for l:buffer_name in g:vg_startup_buffers
        let l:vg_buffer_name = 'vg_' . l:buffer_name
        if index(g:vg_valid_buffers, l:vg_buffer_name) == -1
            echoerr "Error: buffer " . l:buffer_name . " is not a valid buffer in g:vg_startup_buffers"
            return 1
        endif
    endfor
    return 0
endfunction

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    call vg_globals#source_globals()
    if vgdb#dependency_check() | return 0 | endif
    if vgdb#validate_startup_buffer_names() | return 0 | endif
    try
        execute g:vg_py . ' vgdb = Vgdb()'
        execute g:vg_py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
        if g:vg_open_buffers_on_startup
            call vg_display#open_startup_buffers()
        endif
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#run_command(...)
    let command = get(a:000, 0, '')
    try
        execute g:vg_py . ' vgdb.run_command_with_result("' . command . '")'
        echom "command ran successfully: " . command
        call vg_display#update_buffers()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#run_to_entrypoint(...)
    let command = get(a:000, 0, '')
    try
        execute g:vg_py . ' vgdb.run_to_entrypoint()'
        call vg_display#update_buffers()
        echom "application started and halted at entrypoint: " . g:vg_app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#source_python_files()
    exec g:vg_py . "file " . s:vgdbscriptdir . "vgdb.py"
endfunction
