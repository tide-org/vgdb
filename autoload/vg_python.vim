if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_python#check_run_python_command(python_command)
    if len(a:python_command) > 0
        execute g:vg_py . a:python_command
    endif
endfunction

function! vg_python#get_python_command_for_event(command_name, buffer_name, event_name)
    if len(a:command_name) > 0
        let l:return_string = 'vgdb.run_config_command("' . a:command_name . '", "'. a:buffer_name . '", "' . a:event_name . '")'
        return l:return_string
    endif
    return ''
endfunction

function! vg_python#set_python_command(command, buffer_name)
    if len(a:command) > 0
        return 'vgdb.run_config_command("' . a:command . '", "'. a:buffer_name .'")'
    endif
    return ''
endfunction
