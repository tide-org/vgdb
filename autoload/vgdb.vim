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
        execute g:vg_py . 'vgdb = Tide("vim81")'
        execute g:vg_py . 'vgdb.start(startup_commands="' . command . '")'
        echom "Tide started successfully"
        call vg_display#open_startup_buffers()
        call vgdb#run_config_command('')
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
        call vg_display#check_update_config_buffers()
        echom "config command ran successfully: " . l:command
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_config_command: " . l:command . ", " . a:exception | echohl None
    endtry
endfunction
