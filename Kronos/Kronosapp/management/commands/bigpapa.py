from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Seeds with 3 schools.'

    def handle(self, *args, **kwargs):

        # Custom colors for self.stdout.write() 
        bold_cyan = "\033[1;36m"
        bold_magenta = "\033[1;35m"
        bold_green = "\033[1;32m"
        reset = "\033[0m"

        self.stdout.write(f"{bold_magenta}Starting big seed...\n{reset}")

        try:
            self.stdout.write(f"{bold_cyan}Deleting previous data ...\n{reset}")
            call_command('delete_all_data')
            
            self.stdout.write(f"{bold_cyan}Creating superuser ...\n{reset}")
            call_command('auto_createsuperuser')

            self.stdout.write(f"{bold_cyan}Seeding core data ...\n{reset}")
            call_command('test_core')

            self.stdout.write(f"{bold_cyan}Seeding Jesus Maria ...\n{reset}")
            call_command('seedJM')
            
            self.stdout.write(f"{bold_cyan}Seeding Lasalle ...\n{reset}")
            call_command('seedLS')

            self.stdout.write(f"{bold_cyan}Seeding Villada...\n{reset}")
            call_command('seedV')
            # <----- Add your desired scripts here :)

            self.stdout.write(f"{bold_magenta}SUCCESS:{reset} {bold_green}Big seed seeded successfully!{reset}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
