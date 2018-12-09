function! vg_globals#source_globals()
    let g:vg_python_version = 0
    let g:vg_app_entrypoint = ''
    let g:vg_binary_loaded = 0
    let g:vg_symbols_loaded = 0
    let g:vg_remote_target = 0
    let g:vg_py = ''
    let g:vg_breakpoints = []
    let g:vg_config_dictionary = {}
    let g:vg_config_startup_buffers = []
    let g:vg_config_buffers = []
endfunction
