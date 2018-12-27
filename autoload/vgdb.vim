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

function! vgdb#stop_gdb(...)
    call vg_buffer#close_all_buffers()
    execute g:vg_py . ' vgdb.stop_gdb()'
    execute g:vg_py . ' del vgdb'
    unlet g:vg_loaded
    unlet g:vg_config_dictionary
endfunction

function! vgdb#call_bootstrap_functions()
    call vg_globals#source_globals()
    if vg_validate#dependency_check() | return 1 | endif
    if vg_validate#validate_startup_buffer_names() | return 1 | endif
    return 0
endfunction

function! vgdb#call_on_startup_functions()
    if has_key(g:vg_config_dictionary, "settings")
        let l:open_buffers_on_startup = g:vg_config_dictionary['settings']['buffers']['open_buffers_on_startup']
        if l:open_buffers_on_startup | call vg_display#open_startup_buffers() | endif
        if g:vg_config_dictionary['settings']['process']['run_command_on_startup'] | execute '!nohup ' . g:vg_config_dictionary['settings']['process']['command_to_run_on_startup'] . ' </dev/null >/dev/null 2>&1 &' | endif
    endif
endfunction

function! vgdb#run_startup_commands(position)
    if has_key(g:vg_config_dictionary, "events")
        let l:startup_commands = g:vg_config_dictionary["events"][a:position . "_startup"]
        if type(l:startup_commands) == 3
            for l:startup_command in l:startup_commands
                call vgdb#run_config_command(l:startup_command)
            endfor
        endif
    endif
endfunction

function! vgdb#run_config_command(...)
    let l:command = join(a:000, ' ')
    try
        execute g:vg_py . ' vgdb.run_config_command("' . l:command . '")'
        echom "config command ran successfully: " . l:command
        call vgdb#check_update_buffers(l:command)
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_config_command: " . l:command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#check_update_buffers(command)
    if a:command =~ " "
        let l:command_buffer = split(a:command, " ")[0]
    else
        let l:command_buffer = a:command
    endif
    let l:should_update = get(g:vg_config_dictionary["commands"][l:command_buffer], "update_buffer", 1)
    if vg_helpers#is_value_true(l:should_update)
        call vg_display#update_buffers()
    endif
endfunction
