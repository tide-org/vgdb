let s:current_file=expand("<sfile>:p:h")
let s:plugins_path=s:current_file . '/../plugins'

command! -nargs=? -complete=shellcmd VgdbSetAssembly   execute "let $TIDE_CONFIG_LOCATION = '" . s:plugins_path . "/assembly/config/'"
command! -nargs=? -complete=shellcmd VgdbSetC          execute "let $TIDE_CONFIG_LOCATION = '" . s:plugins_path . "/test_c/config/'"
command! -nargs=? -complete=shellcmd VgdbSetGo         execute "let $TIDE_CONFIG_LOCATION = '" . s:plugins_path . "/test_go/config/'"
