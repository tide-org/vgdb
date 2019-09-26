if !exists('g:vg_loaded')
    runtime! plugin/*.vim
endif

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    if vgdb_startup#call_bootstrap_functions()
        return 0
    endif
    try
        echom "starting Tide"
        execute g:vg_py . 'from tide import Tide'
        execute g:vg_py . 'vgdb = Tide()'
        execute g:vg_py . 'vgdb.start("' . command . '")'
        echom "Tide started successfully"
        call vg_display#open_startup_buffers()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#stop_gdb(...)
    call vg_buffer_do#close_all_buffers()
    execute g:vg_py . 'vgdb.stop()'
    execute g:vg_py . 'del vgdb'
    unlet g:vg_loaded
    unlet g:vg_config_dictionary
endfunction

function! vgdb#run_config_command(...)
    let l:command = join(a:000, ' ')
    try
        execute g:vg_py . 'vgdb.run_config_command("' . l:command . '")'
        echom "config command ran successfully: " . l:command
        call vg_display#run_buffer_commands()
        call vgdb#check_update_buffers(l:command)
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_config_command: " . l:command . ", " . a:exception | echohl None
    endtry
endfunction

function! vgdb#check_update_buffers(command)
    let l:command_buffer = vgdb#get_command_from_string(a:command)
    let l:commands = get(g:vg_config_dictionary, "commands", {})
    if len(l:commands) > 0
        let l:should_update = get(l:commands[l:command_buffer], "update_buffer", 1)
        if vg_helpers#is_value_true(l:should_update)
            call vg_display#check_update_config_buffers()
        endif
    endif
endfunction

function! vgdb#get_command_from_string(command)
    if a:command =~ " "
        return split(a:command, " ")[0]
    endif
    return a:command
endfunction
