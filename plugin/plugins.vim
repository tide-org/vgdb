let s:current_file=expand("<sfile>:p:h")
let s:plugins_path=s:current_file . '/../plugins'
let s:tide_let="let $TIDE_CONFIG_LOCATION = '"
let s:tide_end="'"

command! -nargs=? -complete=shellcmd VgdbSetAssembly   execute s:tide_let . s:plugins_path . "/assembly/config/" . s:tide_end
command! -nargs=? -complete=shellcmd VgdbSetC          execute s:tide_let . s:plugins_path . "/test_c/config/" . s:tide_end
command! -nargs=? -complete=shellcmd VgdbSetGo         execute s:tide_let . s:plugins_path . "/test_go/config/" . s:tide_end
