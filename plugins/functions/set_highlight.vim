function! set_highlight#for_breakpoint_and_diff(...)
    let l:breakpoint_highlight_color = get(g:vg_config_dictionary["variables"], "breakpoint_highlight_color", "red")
    execute "highlight breakpoint_pos cterm=NONE ctermbg=" . l:breakpoint_highlight_color . " guibg=" . l:breakpoint_highlight_color
    let l:diff_highlight_color = get(g:vg_config_dictionary["variables"], "diff_highlight_color", "red")
    execute "highlight diff_line cterm=NONE ctermbg=" . l:diff_highlight_color . " guibg=" . l:diff_highlight_color
    sign define wholeline_breakpoint linehl=breakpoint_pos
    sign define wholeline_diff linehl=diff_line
    sign define piet text=>> texthl=Search
endfunction
