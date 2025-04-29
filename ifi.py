import subprocess

def get_wifi_passwords():
    try:
        # Run the command to get WiFi profiles
        profiles_output = subprocess.check_output(["netsh", "wlan", "show", "profiles"], encoding="utf-8")
        profiles = [line.split(":")[1].strip() for line in profiles_output.split("\n") if "All User Profile" in line]

        # Retrieve passwords for each profile
        wifi_passwords = {}
        for profile in profiles:
            try:
                profile_output = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"], encoding="utf-8")
                password_lines = [line.split(":")[1].strip() for line in profile_output.split("\n") if "Key Content" in line]
                password = password_lines[0] if password_lines else "No Password"
                wifi_passwords[profile] = password
            except subprocess.CalledProcessError:
                wifi_passwords[profile] = "Error Retrieving Password"

        return wifi_passwords
    except Exception as e:
        return f"An error occurred: {e}"

# Get and print WiFi passwords
wifi_passwords = get_wifi_passwords()
for wifi, password in wifi_passwords.items():
    print(f"WiFi: {wifi}, Password: {password}")