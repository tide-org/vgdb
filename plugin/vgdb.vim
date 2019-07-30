if !exists('g:vg_loaded') | runtime! plugin/commands.vim | else | finish | endif
if !exists('g:vg_loaded') | runtime! plugin/plugins.vim  | else | finish | endif
if !exists('g:vg_loaded') | runtime! plugin/keys.vim  | else | finish | endif

let g:vg_loaded = 1
