if exists('g:vg_loaded')
  finish
endif

if !exists('g:vg_load_disassembly_on_start')
    let g:vg_load_disassembly_on_start = 0
endif

if !exists('g:vg_use_session_log_file')
    let g:vg_use_session_log_file = 1
endif

if !exists('g:vg_session_log_filename')
    let g:vg_session_log_filename = 'vgdb_session.log'
endif

if !exists('g:vg_stack_buffers')
    let g:vg_stack_buffers = 1
endif

command! -nargs=? -complete=shellcmd Vgdb call vgdb#start_gdb(<q-args>)

command! -nargs=? -complete=shellcmd Vgc call vgdb#run_command(<q-args>)

command! -nargs=? -complete=shellcmd Vgb call vgdb#run_command(<q-args>)

command! -nargs=? -complete=shellcmd Vgrte call vgdb#run_to_entrypoint(<q-args>)

command! -nargs=? -complete=shellcmd Vgreg call vgdb#display_registers(<q-args>)

command! -nargs=? -complete=shellcmd Vgsl call vgdb#display_session_log(<q-args>)

command! -nargs=? -complete=shellcmd Vgbp call vgdb#display_breakpoints(<q-args>)

command! -nargs=? -complete=shellcmd Vgdis call vgdb#show_disassembly(<q-args>)

let g:vg_loaded = 1
