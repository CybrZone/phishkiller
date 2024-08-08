from colorama import Fore, Back, Style
import string

def header():
    header = f'''
    

        {Fore.RED}    ██████╗ ██╗  ██╗██╗███████╗██╗  ██╗██╗  ██╗██╗██╗     ██╗     ███████╗██████╗ 
            ██╔══██╗██║  ██║██║██╔════╝██║  ██║██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗
            ██████╔╝███████║██║███████╗███████║█████╔╝ ██║██║     ██║     █████╗  ██████╔╝
            ██╔═══╝ ██╔══██║██║╚════██║██╔══██║██╔═██╗ ██║██║     ██║     ██╔══╝  ██╔══██╗
            ██║     ██║  ██║██║███████║██║  ██║██║  ██╗██║███████╗███████╗███████╗██║  ██║
            ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝ {Fore.RESET}
    '''
    header += f' {Fore.GREEN}      +------------------------------------------------------------------------------+{Fore.RESET}'
    header += f'''
                            [{Fore.GREEN}+{Fore.RESET}] Author: CybrZone
                            [{Fore.GREEN}+{Fore.RESET}] Github: https://github.com/CybrZone/phishkiller
                            \n\n
                '''.center(25, "\t")
    print(header)