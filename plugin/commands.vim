command! -nargs=? -complete=shellcmd Vgdb               call vgdb#start_gdb(<q-args>)
command! -nargs=? -complete=shellcmd Vgc                call vgdb#run_command(<q-args>)
command! -nargs=? -complete=shellcmd Vgb                call vgdb#run_command(<q-args>)
command! -nargs=? -complete=shellcmd Vgrte              call vgdb#run_to_entrypoint(<q-args>)
command! -nargs=? -complete=shellcmd Vgdis              Vgdisplaybuff 'vg_disassembly'
command! -nargs=? -complete=shellcmd VgRunConfigCommand call vgdb#run_config_command(<q-args>)
command! -nargs=? -complete=shellcmd Vgcont             call vgdb#run_continue(<q-args>)
command! -nargs=? -complete=shellcmd Vgdisplaybuff      call vg_display#display_buffer(<q-args>)
