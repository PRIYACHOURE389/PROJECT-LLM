import yaml

def user_authentication(username, password, config_file):
    """Authenticate a user based on provided username and password."""
    try:
        with open(config_file, 'r') as file:
            users = yaml.safe_load(file).get('users', [])
            for user in users:
                if user['username'] == username and user['password'] == password:
                    return True
        return False
    except Exception as e:
        print(f"Error loading user configuration: {e}")
        return False
