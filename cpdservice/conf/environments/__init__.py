CONFIG_MAP = {
    'prod': 'production',
    'dev': 'development'
}

def get_config(env):
    return '.'.join(['cpdservice', 'conf', 'environments',
                     CONFIG_MAP.get(env, env), 'Config'])
