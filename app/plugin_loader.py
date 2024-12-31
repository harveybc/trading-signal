import pkg_resources

def load_plugin(plugin_group='trading_signal.plugins', plugin_name='default_plugin'):
    print(f"Attempting to load plugin: {plugin_name}")
    try:
        # Debugging: Print the group and plugin name being searched
        print(f"[DEBUG] Searching in plugin group: {plugin_group}")
        entry_map = pkg_resources.get_entry_map('trading_signal', plugin_group)
        print(f"[DEBUG] Available plugins in group '{plugin_group}': {list(entry_map.keys())}")

        # Check if the plugin exists in the entry map
        if plugin_name not in entry_map:
            print(f"[DEBUG] Plugin '{plugin_name}' not found in entry map.")
            raise KeyError(plugin_name)

        # Load the entry point
        entry_point = entry_map[plugin_name]
        print(f"[DEBUG] Found entry point: {entry_point}")

        # Load the plugin class
        plugin_class = entry_point.load()
        print(f"[DEBUG] Plugin class loaded: {plugin_class}")

        # Retrieve required parameters from the plugin class
        required_params = list(plugin_class.plugin_params.keys())
        print(f"Successfully loaded plugin: {plugin_name} with params: {plugin_class.plugin_params}")
        return plugin_class, required_params

    except KeyError as e:
        print(f"[ERROR] Failed to find plugin '{plugin_name}' in group '{plugin_group}', Error: {e}")
        raise ImportError(f"Plugin {plugin_name} not found.") from e

    except Exception as e:
        print(f"[ERROR] An unexpected error occurred while loading plugin '{plugin_name}', Error: {e}")
        raise


def get_plugin_params(plugin_name):
    print(f"Getting plugin parameters for: {plugin_name}")
    try:
        entry_point = pkg_resources.get_entry_map('trading_signal', 'trading_signal.plugins')[plugin_name]
        plugin_class = entry_point.load()
        print(f"Retrieved plugin params: {plugin_class.plugin_params}")
        return plugin_class.plugin_params
    except KeyError as e:
        print(f"Failed to find plugin {plugin_name}, Error: {e}")
        return {}
    except Exception as e:
        print(f"Failed to get plugin params: {plugin_name}, Error: {e}")
        return {}
