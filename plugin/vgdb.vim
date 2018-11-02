if exists('g:Vgdb_Loaded')
  finish
endif

command! -nargs=? -complete=shellcmd Vgdb call vgdb#start_gdb(<q-args>)
command! -nargs=? -complete=shellcmd Vgc call vgdb#run_command(<q-args>)
command! -nargs=? -complete=shellcmd Vgb call vgdb#run_command(<q-args>)
command! -nargs=? -complete=shellcmd Vgrte call vgdb#run_to_entrypoint(<q-args>)

let g:Vgdb_Loaded = 1
