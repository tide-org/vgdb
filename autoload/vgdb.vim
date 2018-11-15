if !exists('g:vg_loaded')
    runtime! plugin/vgdb.vim
endif

let s:scriptdir = expand("<sfile>:h") . '/'
let s:vgdbscriptdir = s:scriptdir . "vgdb/"
let s:ptyprocessdir = s:scriptdir . "lib/ptyprocess/ptyprocess/"
let s:initialised = 0

let g:vg_python_version = 0
let g:vg_query_result = []
let g:vg_full_query_result = []
let g:vg_session_log = []
let g:vg_app_entrypoint = ''
let g:vg_last_register_result = []
let g:vg_binary_loaded = 0
let g:vg_symbols_loaded = 0
let g:vg_valid_buffers = ['vg_registers', 'vg_session_log', 'vg_breakpoints']
let g:vg_remote_target = 0

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
    let s:py = ''
    let pytest = 'python3'
    if has(pytest)
        if pytest == 'python3'
            let s:py = 'py3'
        endif
    endif
    if s:py == ''
        call vgdb#fail()
        return 1
    endif
    call vgdb#source_python_files()
    return 0
endfunction

function! vgdb#start_gdb(...)
    let command = get(a:000, 0, '')
    if vgdb#dependency_check()
        return 0
    endif
    try
        execute s:py . ' vgdb = Vgdb()'
        execute s:py . ' vgdb.start_gdb("' . command . '")'
        echom "Vgdb started successfully"
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#start_gdb: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#run_command(...)
    let command = get(a:000, 0, '')
    try
        execute s:py . ' vgdb.run_command_with_result("' . command . '")'
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
        execute s:py . ' vgdb.run_to_entrypoint()'
        call vgdb#update_buffers()
        echom "application started and halted at entrypoint: " . g:vg_app_entrypoint
    catch a:exception
        echohl WarningMsg | echomsg "An error occurred in vgdb#run_command: " . command . ", " . a:exception | echohl None
        return 1
    endtry
endfunction

function! vgdb#update_buffers()
    call vgdb#remove_unlisted_buffers()
    call vgdb#check_update_registers()
    call vgdb#check_update_session_log()
    call vgdb#check_update_breakpoints()
endfunction

function! vgdb#check_update_registers()
    if vgdb#window_by_bufname('vg_registers', 0) != -1
        call vgdb#display_registers()
    endif
endfunction

function! vgdb#check_update_session_log()
    if vgdb#window_by_bufname('vg_session_log', 0) != -1
        call vgdb#display_session_log()
    endif
endfunction

function! vgdb#check_update_breakpoints()
    if vgdb#window_by_bufname('vg_breakpoints', 0) != -1
        call vgdb#display_breakpoints()
    endif
endfunction

function! vgdb#display_session_log(...)
    let l:current_window_num = winnr()
    call vgdb#create_split('vg_session_log')
    call vgdb#window_by_bufname('vg_session_log', 1)
    call append(line('$'), g:vg_full_query_result)
    let g:vg_full_query_result = []
    execute 'normal! G'
    execute l:current_window_num . 'wincmd w'
endfunction

function! vgdb#display_registers(...)
    let l:current_window_num = winnr()
    call vgdb#create_split('vg_registers')
    execute s:py . ' vgdb.run_command_with_result("info registers")'
    call vgdb#window_by_bufname('vg_registers', 1)
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vgdb#display_breakpoints(...)
    let l:current_window_num = winnr()
    call vgdb#create_split('vg_breakpoints')
    execute s:py . ' vgdb.run_command_with_result("info breakpoints")'
    call vgdb#window_by_bufname('vg_breakpoints', 1)
    silent 1,$d _
    call append(line('$'), g:vg_query_result)
    exec l:current_window_num . 'wincmd w'
endfunction

function! vgdb#remove_unlisted_buffers()
    let l:buffer_numbers = filter(range(1,bufnr('$')), 'bufexists(v:val)')
    for l:buffer_number in l:buffer_numbers
        if !bufloaded(l:buffer_number) && !buflisted(l:buffer_number)
            exe 'bwipeout ' . l:buffer_number
        endif
    endfor
endfunction

function! vgdb#create_split(buffer_name)
    call vgdb#remove_unlisted_buffers()
    if vgdb#window_by_bufname(a:buffer_name, 0) == -1
        if g:vg_stack_buffers
            let l:existing_window = vgdb#first_window_by_valid_buffers()
            if l:existing_window != -1
                execute l:existing_window . 'wincmd w'
                new
            else
                exec g:vg_stack_buffer_window_width . 'vnew'
            endif
        else
            exec g:vg_stack_buffer_window_width . 'vnew'
        endif
        setlocal buftype=nofile
        setlocal nonumber
        setlocal foldcolumn=0
        setlocal wrap
        setlocal noswapfile
        setlocal bufhidden=delete
        silent exec 'file ' . a:buffer_name
    endif
endfunction

function! vgdb#window_by_bufname(bufname, switch_window)
    let l:bufmap = map(range(1, winnr('$')), '[bufname(winbufnr(v:val)), v:val]')
    let l:filtered_map = filter(bufmap, 'v:val[0] =~ a:bufname')
    if len(l:filtered_map) > 0
        let l:found_window = filtered_map[0][1]
        if a:switch_window
            execute l:found_window . 'wincmd w'
        endif
        return l:found_window
    else
        return -1
    endif
endfunction

function! vgdb#first_window_by_valid_buffers()
    for buffer_name in g:vg_valid_buffers
        let l:window_number = vgdb#window_by_bufname(buffer_name, 0)
        if l:window_number != -1
            return window_number
        endif
    endfor
    return -1
endfunction

function! vgdb#source_python_files()
    exec s:py . "file " . s:vgdbscriptdir . "vgdb.py"
endfunction
