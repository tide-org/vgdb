- There is a default config that is called regardless.
- Either the ENV VAR or the config_location.yml file will determine the base config file.

- the vase config file can have a settings.plugins.config_path that specifies a config to be loaded before the base config is loaded. this config can in turn call another config file to be called before it is called.

- The config files are then all merged, starting with the default config file, followed by the last in the config chain all the way up to the config file that was referenced by env var or the config_location.yaml file.

- Then for all the different plugins, the same order for loading is done. 

- For things like functions, it pays not to have the same name as a name in a base class as the base version will be called first (may change this).

-All the plugin_paths in the config are first checked as absolute (or relative to the calling path) and then relative to the config that it was declared in. The merge process on config files does not affect the plugin paths in settings.plugins.<plugin>_path.

