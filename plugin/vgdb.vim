if exists('g:Vgdb_Loaded')
    finish
endif

command! -nargs=? -complete=shellcmd Vgdb call vgdb#open_gdb(<q-args>)

let g:Vgdb_Loaded = 1
