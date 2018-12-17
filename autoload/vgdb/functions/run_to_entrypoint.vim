function! vgdb#functions#run_to_entrypoint#was_successful()
    if strlen(g:vg_app_entrypoint) > 0
        echom "application started and halted at entrypoint: " . g:vg_app_entrypoint
    endif
endfunction
