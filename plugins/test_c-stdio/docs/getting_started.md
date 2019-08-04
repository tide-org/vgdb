# General notes:

the file to run is in the `gdb_settings.yaml` file under `commands.load_file.steps[0].run_command_command`

this could be extracted to a separate variable or allow a file to be called from the vim terminal line

the gdb debugger needs to be from the brew batch `gdb_tim`

# to start:

:Vgdb

# to set a breakpoint:

e.g. for line 6 of the current `vg_code` buffer:

```
:VgRunConfigCommand set_breakpoint 6
```
