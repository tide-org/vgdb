if !exists('g:vg_loaded')
    runtime! plugin/*.vim
endif

function! vgdb_startup#call_bootstrap_functions()
    call vg_globals#source_globals()
    if vg_validate#dependency_check()
        return 1
    endif
    if vg_validate#validate_startup_buffer_names()
        return 1
    endif
    return 0
endfunction

function! vgdb_startup#call_on_startup_functions()
    if has_key(g:vg_config_dictionary, "settings")
        let l:open_buffers_on_startup = vg_helpers#is_value_true(g:vg_config_dictionary['settings']['buffers']['open_buffers_on_startup'])
        if l:open_buffers_on_startup
            call vg_display#open_startup_buffers()
        endif
        if g:vg_config_dictionary['settings']['process']['run_command_on_startup']
            execute '!nohup ' . g:vg_config_dictionary['settings']['process']['command_to_run_on_startup'] . ' </dev/null >/dev/null 2>&1 &'
        endif
    endif
endfunction

function! vgdb_startup#run_startup_commands(position)
    if has_key(g:vg_config_dictionary, "events")
        let l:startup_commands = g:vg_config_dictionary["events"][a:position . "_startup"]
        if type(l:startup_commands) == 3
            for l:startup_command in l:startup_commands
                call vgdb#run_config_command(l:startup_command)
            endfor
        endif
    endif
endfunction
