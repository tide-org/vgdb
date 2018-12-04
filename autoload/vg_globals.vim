function! vg_globals#source_globals()
    let g:vg_python_version = 0
    let g:vg_query_result = []
    let g:vg_full_query_result = []
    let g:vg_session_log = []
    let g:vg_app_entrypoint = ''
    let g:vg_last_register_result = []
    let g:vg_binary_loaded = 0
    let g:vg_symbols_loaded = 0
    let g:vg_filtered_buffers = ['vg_breakpoints', 'vg_disassembly']
    let g:vg_remote_target = 0
    let g:vg_py = ''
    let g:vg_current_frame_address = ''
    let g:vg_breakpoints = []
    let g:vg_config_dictionary = {}
    let g:vg_config_startup_buffers = []
    let g:vg_config_buffers = []
endfunction
