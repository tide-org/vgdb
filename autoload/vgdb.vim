if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "vgdb/"
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0

function! vgdb#fail()
    echohl WarningMsg | echomsg "Vgdb ERROR: Python interface cannot be loaded" | echohl None
    echohl WarningMsg | echomsg "Your version of Vim appears to be installed without the Python interface." | echohl None
    if !executable("python")
        echohl WarningMsg | echomsg "You may also need to install Python." | echohl None
    endif
endfunction

function! vgdb#dependency_check()
    if s:initialised == 1
        return 0
    endif
    let g:vg_py = ''
    let pytest = 'python3'
    if has(pytest)
        if pytest == 'python3'
            let g:vg_py = 'py3'
        endif
    endif
    if g:vg_py == ''
        call vgdb#fail()
        return 1
    endif
    call vgdb#source_python_files()
    return 0
endfunction

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    call vg_globals#source_globals()
    if vgdb#dependency_check()
        return 0
    endif
    try
        execute g:vg_py . ' vgdb = Vgdb()'
        execute g:vg_py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_command(...)
    let command = get(a:000, 0, '')
    try
        execute g:vg_py . ' vgdb.run_command_with_result("' . command . '")'
        echom "command ran successfully: " . command
        call vgdb#update_buffers()
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_to_entrypoint(...)
    let command = get(a:000, 0, '')
    try
        execute g:vg_py . ' vgdb.run_to_entrypoint()'
        call vgdb#update_buffers()
        echom "application started and halted at entrypoint: " . g:vg_app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#update_buffers()
    call vg_buffer#remove_unlisted_buffers()
    call vgdb#check_update_registers()
    call vgdb#check_update_session_log()
    call vgdb#check_update_breakpoints()
endfunction

function! vgdb#check_update_registers()
    if vg_buffer#window_by_bufname('vg_registers') != -1
        call vgdb#display_registers()
    endif
endfunction

function! vgdb#check_update_session_log()
    if vg_buffer#window_by_bufname('vg_session_log') != -1
        call vgdb#display_session_log()
    endif
endfunction

function! vgdb#check_update_breakpoints()
    if vg_buffer#window_by_bufname('vg_breakpoints') != -1
        call vgdb#display_breakpoints()
    endif
endfunction

function! vgdb#display_session_log(...)
    let l:current_window_num = winnr()
    call vg_buffer#create_split('vg_session_log')
    call vg_buffer#window_by_bufname('vg_session_log', 1)
    call append(line('$'), g:vg_full_query_result)
    let g:vg_full_query_result = []
    execute 'normal! G'
    execute l:current_window_num . 'wincmd w'
endfunction

function! vgdb#display_registers(...)
    call vg_buffer#default_display_buffer('vg_registers', 'info registers')
endfunction

function! vgdb#display_breakpoints(...)
    call vg_buffer#default_display_buffer('vg_breakpoints', 'info breakpoints')
endfunction

function! vgdb#display_disassembly(...)
    let l:current_window_num = winnr()
    call vg_buffer#switch_to_existing_buffer_or_set_empty_buffer_or_split('vg_disassembly', 'asm')
    execute g:vg_py . ' vgdb.display_disassembly()'
    call vg_buffer#window_by_bufname('vg_disassembly', 1)
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vgdb#source_python_files()
    exec g:vg_py . "file " . s:vgdbscriptdir . "vgdb.py"
endfunction
