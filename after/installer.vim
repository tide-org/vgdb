if !exists('g:vg_loaded')
    runtime! plugin/*.vim
endif

echom "Vgdb post-install commands:"

call vg_install#update_tide()
