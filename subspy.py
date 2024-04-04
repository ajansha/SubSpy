import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

def fetch_subdomains_crtsh(domain):
    url = f"https://crt.sh/?q=%.{domain}&output=json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # We'll raise an exception for any bad response
        data = response.json()
        return set(entry.get("name_value", "") for entry in data)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching subdomains from crt.sh: {e}")
        return set()

def fetch_subdomains_nmmapper(domain):
    url = f"https://www.nmmapper.com/sys/tools/subdomainfinder/?domain={domain}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # We'll raise an exception for any bad response
        soup = BeautifulSoup(response.text, "html.parser")
        subdomains = set(tag.text.strip() for tag in soup.find_all("td", class_="copy-sub"))
        return subdomains
    except requests.exceptions.RequestException as e:
        print(f"Error fetching subdomains from NMSubdomainFinder: {e}")
        return set()

def brute_force_subdomains(domain, wordlist):
    subdomains = set()

    if wordlist:
        with open(wordlist, 'r') as file:
            for line in file:
                subdomain = line.strip()
                hostname = f"{subdomain}.{domain}"
                subdomains.add(hostname)

    return subdomains

if __name__ == "__main__":
    print("""
          


              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⡴⠚⢉⡃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣉⠛⠻⢶⢦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠖⢫⢗⣴⡿⣻⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⢰⣜⣎⣎⠷⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠞⢁⣴⢣⣫⠌⣽⢃⣀⡤⠤⠀⠀⠀⠀⠀⠀⠀⠤⠤⠤⢤⣀⣠⡟⣟⣘⠘⡆⠑⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠂⠀⡴⠃⣰⡿⣴⡧⠷⠚⠉⠁⣀⣠⠤⢤⣒⣒⣂⣀⣠⣠⣄⣠⣤⣶⣿⡟⠙⠻⢼⣾⡞⡆⠈⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡜⢁⣾⠟⠋⠙⣿⣶⣶⣶⣷⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣦⣤⣌⣙⠿⣕⡀⠿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣎⠴⠋⠀⣠⠔⣢⣼⣿⣿⣿⣿⣿⡿⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⢫⡙⠈⠳⣄⢻⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄⠀⠀⣠⠞⠁⢀⡤⣚⣵⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠈⠲⣄⠈⣳⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣶⣴⣉⣀⣴⣫⣾⣿⣿⣿⣿⣿⡟⣿⣿⠋⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⡈⢧⡈⢙⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⠇⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠙⣄⠹⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⠋⠀⡙⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣸⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⠀⠀⠘⣿⣿⣿⡿⣿⣿⣿⣿⣿⣿⡟⢿⡜⣎⢦⠙⣷⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡼⠃⢠⣯⣾⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⣻⡧⣀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⢀⣤⠶⢻⣿⣿⡷⢿⣿⣿⣿⣿⣿⣿⣴⡿⡜⣾⡇⠈⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣼⠁⢠⣿⣿⠟⠋⣽⣿⣿⣿⣿⣿⣧⠶⠚⢻⡏⠛⠲⢦⣀⠀⠀⣠⠀⠀⠀⢿⣿⠋⠀⠀⠸⣿⣿⠀⢸⣿⣿⣿⣿⣿⣿⣿⡅⠙⠀⠘⣄⠙⣧⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⠃⠀⣼⡟⠁⠀⣠⣿⣿⣿⣿⣿⣿⠁⠀⠀⠈⢇⠀⠀⠉⠈⠑⠀⠙⢦⠀⠀⢸⡏⠀⢀⣠⣶⣿⠇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀⠀⢸⠀⠸⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⠀⠀⡇⠁⠄⣰⣿⣿⣿⣿⣿⣿⣇⠀⠀⠠⣄⣿⣶⣦⣄⡄⠀⠀⢄⣿⠆⠀⠘⠃⣰⣿⣷⡿⠿⠶⣦⡀⣿⣿⢻⣿⣿⣿⣿⡝⠻⣦⣠⠀⠇⠀⢳⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⠇⠀⢁⣴⡾⠿⢻⣿⣿⣿⣿⣿⣿⠀⣠⣾⠟⠉⠠⠶⠛⠇⠀⠀⣿⠁⠀⠀⠀⠈⠛⣙⣉⣉⣀⣠⡴⠛⣿⡏⣿⣿⣿⣿⣿⡇⠀⠀⠙⠈⢡⠀⣼⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡖⣾⠄⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣟⢿⡇⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠉⠣⠘⠂⠀⣀⣐⣀⣈⣁⡤⠤⠷⠶⣟⠀⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠱⠀⣧⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠁⢯⡆⠐⡄⠀⠀⠀⣾⣿⡇⣿⣿⣿⣆⢹⣷⠞⠚⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢀⠀⠀⢀⠀⢸⢀⣿⣿⣿⣿⠹⣇⠀⠀⠀⠀⡇⠀⣸⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢸⡃⠀⢳⢰⡀⣄⠈⣿⡀⣼⣛⢻⡏⣿⠃⠀⡆⠀⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡇⠀⣸⡤⢸⢸⡿⣿⢻⣿⡄⠉⠀⠀⠀⢸⠀⢠⡏⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢧⠀⠈⣧⢷⡙⣮⢯⡧⣇⣯⣷⢹⣸⡆⠦⢽⣄⣘⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠤⠤⠒⠚⡟⠋⠹⢀⡟⡾⣾⣿⢸⠈⢻⣦⣄⣠⢄⡟⣀⡞⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢣⣤⠘⢿⡻⠈⠉⠁⠹⣜⢯⡓⢧⢳⡀⢸⡁⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⢀⡼⣽⢗⣫⢏⡞⠀⠛⠿⡿⢃⡞⠀⡞⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠳⣅⠀⠝⣆⠺⣔⢴⣬⣳⢭⣩⣦⢳⣄⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡞⣱⢗⣋⡽⢋⡀⠀⠀⡀⣠⠊⣰⡜⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠢⣄⠈⢳⣌⡛⠋⠉⠁⠀⠈⠳⢼⡷⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡾⢋⣴⡿⠉⠱⣶⠿⢟⡵⣺⠞⢁⣴⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⠤⣀⢀⠀⢦⡿⣔⠯⣷⠆⢻⣶⣬⣳⠲⠤⣄⣀⣀⣀⣤⠤⠤⢖⡻⣟⣭⣴⣿⠏⢳⣺⠴⢀⡀⢉⡜⡁⣠⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢥⣀⠉⠻⣋⠀⠀⠈⠓⢻⢎⠙⠒⠯⣄⡀⢀⣐⡶⠾⠛⠋⡽⣸⠃⠉⠀⠀⠀⢚⡩⠞⢡⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡬⠵⣶⡤⣄⡐⠦⠄⢸⢸⠀⠀⠀⠀⠉⠉⠀⠀⠀⠀⣸⠁⡏⠄⣀⣀⣤⠮⣭⣤⠚⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⢃⣴⣿⣿⣿⣿⣿⣷⣦⡟⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡏⠀⣷⣛⣉⣬⣤⣤⡈⠹⢳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣠⠴⠚⠉⠛⠒⢲⡏⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣧⠀⢻⣿⣿⣿⣿⣿⣿⣧⠈⠙⠦⣄⡤⠴⠦⣤⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⡞⢉⣴⣾⣿⣿⣷⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣰⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡀⠸⣿⣿⣿⣿⣿⣿⣿⣷⣄⣤⣤⣤⣴⣶⣭⡙⢦⡀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⠏⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢳⡀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠱⡄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡫⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢤⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⣿⡀⠀⠀⠀⠀
⠀⠀⢀⡴⠞⣡⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠻⠥⠯⢤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣤⠤⠽⠦⠭⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡞⢿⣦⡀⠀⠀
⠀⣰⠏⣡⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠉⠙⠲⢤⠀⠀⠀⠀⠤⠒⠋⠉⠁⠀⠀⠀⠀⠀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣜⠛⣆⠀
⠼⠁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠘⢆

                        
                   ____        _    ____                        
                  / ___| _   _| |__/ ___| _ __  _   _           
                  \___ \| | | | '_ \___ \| '_ \| | | |  
                   _ _) | |_| | |_) |__) | |_) | |_| |  
                  |____/ \__,_|_.__/____/| .__/ \__, |          
                                         |_|    |___/           
                                                        


+-------------------------------------------------------+
|                                                       |
|        SubSpy - Subdomain Enumeration Tool            |        
|        Author: Ajansha Shankar                        |    
|        LinkedIn: Ajansha Shankar                      |      
|        GitHub: https://github.com/ajansha             |   
+-------------------------------------------------------+
    """)

    domain = input("Enter the domain you want to find subdomains for: ")

    # We'll sneakily collect subdomains, no brute force needed, just good old fashioned stealth and strategy.
    subdomains_crtsh = fetch_subdomains_crtsh(domain)
    subdomains_nmmapper = fetch_subdomains_nmmapper(domain)

    # blend them into a master list
    all_subdomains = subdomains_crtsh.union(subdomains_nmmapper)

    # Ask user if they want to use a wordlist
    use_wordlist = input("Do you want to use a wordlist for brute force subdomain enumeration? (yes/no): ").strip().lower()
    if use_wordlist == "yes":
        wordlist = input("Enter the path to the wordlist: ")
        brute_force_subdomains_list = brute_force_subdomains(domain, wordlist)
        all_subdomains.update(brute_force_subdomains_list)

    if all_subdomains:
        # Construct the output file name with a valid format
        domain_name = domain.split("//")[-1].split("/")[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"subdomains_{domain_name}_{timestamp}.txt"

        # Write subdomains to the output file
        with open(output_file, "w") as file:
            for subdomain in all_subdomains:
                file.write(subdomain + "\n")
        print(f"Subdomains found and saved to {output_file}")
    else:
        print("No subdomains found.")
