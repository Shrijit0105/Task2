import os
import paramiko


VM_HOST = "host"
VM_PORT = 0000
VM_USER = "user12344"

PRIVATE_KEY_PATH = os.path.expanduser("~/.ssh/id")


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print("[+] Loading private key...")

        private_key = paramiko.Ed25519Key.from_private_key_file(
            PRIVATE_KEY_PATH
        )

        print(f"[+] Connecting to {VM_USER}@{VM_HOST}:{VM_PORT}...")

        client.connect(
            hostname=VM_HOST,
            port=VM_PORT,
            username=VM_USER,
            pkey=private_key,
            timeout=10
        )

        print("[+] SSH key-based authentication successful!")
        print("[+] Connected to Ubuntu VM.")
        print()

        commands = [
            "hostname",
            "whoami",
            "pwd",
            "uname -r",
            "df -h /"
        ]

        for command in commands:
            print(f"=== Running: {command} ===")

            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            if output:
                print(output)

            if error:
                print("[Error]:", error)

            print()

    except paramiko.AuthenticationException:
        print("[!] SSH authentication failed.")

    except paramiko.SSHException as error:
        print("[!] SSH error:", error)

    except Exception as error:
        print("[!] Connection failed:", error)

    finally:
        client.close()
        print("[+] SSH connection closed.")


if __name__ == "__main__":
    main()