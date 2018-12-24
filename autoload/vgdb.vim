if !exists('g:vg_loaded') | runtime! plugin/*.vim | endif

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    if vgdb#call_bootstrap_functions() | return 0 | endif
    try
        call vgdb#run_startup_commands('before')
        execute g:vg_py . ' vgdb = Vgdb()'
        execute g:vg_py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
        call vgdb#call_on_startup_functions()
        call vgdb#run_startup_commands('after')
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#call_bootstrap_functions()
    call vg_globals#source_globals()
    if vg_validate#dependency_check() | return 1 | endif
    if vg_validate#validate_startup_buffer_names() | return 1 | endif
    return 0
endfunction

function! vgdb#call_on_startup_functions()
    if g:vg_open_buffers_on_startup | call vg_display#open_startup_buffers() | endif
    if g:vg_run_command_on_startup | execute '!nohup ' . g:vg_command_to_run_on_startup . ' </dev/null >/dev/null 2>&1 &' | endif
endfunction

function! vgdb#run_startup_commands(position)
    let l:startup_commands = g:vg_config_dictionary["events"][a:position . "_startup"]
    if type(l:startup_commands) == 3
        for l:startup_command in l:startup_commands
            call vgdb#run_config_command(l:startup_command)
        endfor
    endif
endfunction

function! vgdb#run_config_command(...)
    let command = get(a:000, 0, '')
    try
        execute g:vg_py . ' vgdb.run_config_command("' . command . '")'
        echom "config command ran successfully: " . command
        call vg_display#update_buffers()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_config_command: " . command . ", " . a:exception | echohl None
    endtry
endfunction
