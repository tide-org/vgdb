function! run_to_entrypoint#was_successful(...)
    let l:app_entrypoint = g:vg_config_dictionary['variables']['app_entrypoint']
    if strlen(l:app_entrypoint) > 0
        echom "application started and halted at entrypoint: " . l:app_entrypoint
    endif
endfunction
