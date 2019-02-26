command! -nargs=? -complete=shellcmd Vgdb                call vgdb#start_gdb(<q-args>)
command! -nargs=? -complete=shellcmd VgRunConfigCommand  call vgdb#run_config_command(<q-args>)
command! -nargs=? -complete=shellcmd VgDisplayBuffer     call vg_display#display_buffer(<q-args>)
command! -nargs=? -complete=shellcmd VgClose             call vgdb#stop_gdb(<q-args>)
