import subprocess
import sys
import logging
import os
import urllib.request

# Set up logging to log to a file
# log_file = '/tmp/jupyter_lab_setup.log'
log_file = '/tmp/machine_manager_setup.log'
logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode='w', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def install_pip():
    try:
        import pip
        logging.info("Pip is already installed.")
    except ImportError:
        logging.info("Pip not found. Installing pip...")
        url = 'https://bootstrap.pypa.io/get-pip.py'
        get_pip_script = '/tmp/get-pip.py'
        urllib.request.urlretrieve(url, get_pip_script)
        try:
            subprocess.check_call([sys.executable, get_pip_script])
            logging.info("Pip installed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to install pip: {e}")
            sys.exit(1)
        finally:
            if os.path.exists(get_pip_script):
                os.remove(get_pip_script)

def install_jupyter_lab():
    logging.info("Installing Jupyter Lab...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'jupyterlab'])
        logging.info("Jupyter Lab installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to install Jupyter Lab: {e}")
        sys.exit(1)


def run_jupyter_lab(tunnel_port): 
    logging.info("Running Jupyter Lab...")
    try:
        # Run jupyter lab with specified options
        subprocess.check_call([sys.executable, '-m', 'jupyter', 'lab', '--no-browser', '--ip=0.0.0.0', f'--port={tunnel_port}', '--allow-root'])
        logging.info("Jupyter Lab started successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to start Jupyter Lab: {e}")
        sys.exit(1)

def main(tunnel_port):
    try:
        install_pip()
        install_jupyter_lab()
        run_jupyter_lab(tunnel_port)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        tunnel_port = int(sys.argv[1])
    else:
        tunnel_port = 8888
    main(tunnel_port)