if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "vgdb/"
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    if vgdb#call_bootstrap_functions() | return 0 | endif
    try
        execute g:vg_py . ' vgdb = Vgdb()'
        execute g:vg_py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
        call vgdb#call_on_startup_functions()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#call_bootstrap_functions()
    call vg_globals#source_globals()
    if vg_validate#dependency_check() | return 1 | endif
    call vgdb#source_python_files()
    if vg_validate#validate_startup_buffer_names() | return 1 | endif
    return 0
endfunction

function! vgdb#call_on_startup_functions()
    if g:vg_open_buffers_on_startup
        call vg_display#open_startup_buffers()
    endif
    if g:vg_run_command_on_startup
        execute '!nohup ' . g:vg_command_to_run_on_startup . ' </dev/null >/dev/null 2>&1 &'
    endif
    if g:vg_connect_to_remote_on_startup
        call vgdb#run_command("target remote " . g:vg_remote_address)
        call vgdb#run_to_entrypoint()
    endif
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
