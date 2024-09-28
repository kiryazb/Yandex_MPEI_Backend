# Напишите декоратор obfuscator
def obfuscator(func):
    def wrapper(*args, **Kwargs):
        result = func()
        name, password = list(result["name"]), list(result["password"])
        for i in range(1, len(name) - 1):
            name[i] = "*"
        for i in range(len(password)):
            password[i] = "*"
        name, password = ''.join(name), ''.join(password)
        result['name'] = name
        result['password'] = password
        return result
    return wrapper

@obfuscator
def get_credentials():
    return {
        'name': 'StasBasov',
        'password': 'iamthebest'
    }


print(get_credentials())