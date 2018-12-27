if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_helpers#is_value_true(test_value)
    let l:to_test = substitute(tolower(string(a:test_value)), "'", '', 'g')
    let l:true_list = [ "true", "1", "yes", "y" ]
    for l:true_item in l:true_list
        if l:true_item ==? l:to_test
           return 1
        endif
    endfor
    return 0
endfunction
