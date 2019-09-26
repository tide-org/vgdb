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

function! vgdb_startup#run_after_startup_commands()
    if has_key(g:vg_config_dictionary, "events")
        let l:startup_commands = get(g:vg_config_dictionary["events"], "after_startup", [])
        if type(l:startup_commands) == 3
            for l:startup_command in l:startup_commands
                call vgdb#run_config_command(l:startup_command)
            endfor
        endif
    endif
endfunction
