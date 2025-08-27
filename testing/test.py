ALLOWED_IPS = {"127.0.0.1", "192.168.1.100", "203.0.113.50"}  # Replace with your IPs

def ip_whitelist(f):
    def decorated_function(*args, **kwargs):
        client_ip = "127.0.0.11"
        if client_ip not in ALLOWED_IPS:
            print("failed")
        print('passed')
        return f(*args, **kwargs)
    return decorated_function

@ip_whitelist
def secure_data():
    return "You have access to this route."


if __name__=='__main__':
    print(secure_data())