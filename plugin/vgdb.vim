if !exists('g:vg_loaded')
  runtime! plugin/config_settings.vim
  runtime! plugin/commands.vim
  runtime! plugin/decorations.vim
else
  finish
endif

let g:vg_loaded = 1
