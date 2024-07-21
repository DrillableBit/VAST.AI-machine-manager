import re

def parse_ssh_url(ssh_url):
    """
    Parses an SSH URL in the format ssh://user@host:port and returns the user, host, and port.
    """
    match = re.match(r'ssh://(.*)@(.*):(\d+)', ssh_url)
    if not match:
        raise ValueError(f"Invalid SSH URL format: {ssh_url}")
    
    user = match.group(1)
    host = match.group(2)
    port = match.group(3)
    return user, host, port