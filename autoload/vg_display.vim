if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

function! vg_display#open_startup_buffers()
    for l:buffer_name in g:vg_startup_buffers
        execute 'call vg_display#display_' . l:buffer_name . '()'
    endfor
endfunction

function! vg_display#update_buffers()
    call vg_buffer#remove_unlisted_buffers()
    call vg_display#check_update_registers()
    call vg_display#check_update_session_log()
    call vg_display#check_update_breakpoints()
endfunction

function! vg_display#check_update_registers()
    if vg_buffer#window_by_bufname('vg_registers') != -1
        call vg_display#display_vg_registers()
    endif
endfunction

function! vg_display#check_update_session_log()
    if vg_buffer#window_by_bufname('vg_session_log') != -1
        call vg_display#display_vg_session_log()
    endif
endfunction

function! vg_display#check_update_breakpoints()
    if vg_buffer#window_by_bufname('vg_breakpoints') != -1
        call vg_display#display_vg_breakpoints()
    endif
endfunction

function! vg_display#display_vg_session_log(...)
    let l:current_window_num = winnr()
    call vg_buffer#create_split('vg_session_log')
    call vg_buffer#window_by_bufname('vg_session_log', 1)
    setlocal modifiable
    call append(line('$'), g:vg_full_query_result)
    setlocal nomodifiable
    let g:vg_full_query_result = []
    execute 'normal! G'
    execute l:current_window_num . 'wincmd w'
endfunction

function! vg_display#display_vg_registers(...)
    call vg_buffer#default_display_buffer('vg_registers', 'info registers')
endfunction

function! vg_display#display_vg_breakpoints(...)
    call vg_buffer#default_display_buffer('vg_breakpoints', 'info breakpoints')
endfunction

function! vg_display#display_vg_disassembly(...)
    let l:current_window_num = winnr()
    call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split('vg_disassembly', 'asm')
    execute g:vg_py . ' vgdb.display_disassembly()'
    call vg_buffer#window_by_bufname('vg_disassembly', 1)
    setlocal modifiable
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    setlocal nomodifiable
    exec l:current_window_num . 'wincmd w'
endfunction
