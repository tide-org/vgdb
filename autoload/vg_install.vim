if !exists('g:vg_loaded')
    runtime! plugin/*.vim
endif

function! vg_install#update_tide()
  call vg_install#uninstall_tide()
	call vg_install#install_tide()
endfunction

function vg_install#install_tide()
  if !vgdb_startup#call_bootstrap_functions()
    echom "install latest version of Tide"
    execute g:vg_py . 'from pip import main as pip; pip(["install", "tide"])'
  else
    echom "unable to bootstrap vgdb"
  endif
endfunction

function! vg_install#uninstall_tide()
  if !vgdb_startup#call_bootstrap_functions()
    echom "uninstall any old version of Tide"
    execute g:vg_py . "
    \ import pip; 
    \ import shutil; 
    \ import glob;
    \ base_path = pip.__path__[0] + '/..';
    \ path_list = glob.glob(base_path + '/tide*');
    \ [ shutil.rmtree(single_path, ignore_errors=True) for single_path in path_list ] "
  else
    echom "unable to bootstrap vgdb"
  endif
endfunction
