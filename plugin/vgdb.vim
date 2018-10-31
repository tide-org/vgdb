if exists('g:Vgdb_Loaded')
  finish
endif

command! -nargs=? -complete=shellcmd Vgdb call vgdb#start_gdb(<q-args>)

let g:Vgdb_Loaded = 1
