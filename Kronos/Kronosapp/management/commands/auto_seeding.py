from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Execute automatic seeding, useful for quick seeding.'

    def handle(self, *args, **kwargs):

        # Custom colors for self.stdout.write() 
        bold_cyan = "\033[1;36m"
        bold_magenta = "\033[1;35m"
        bold_green = "\033[1;32m"
        reset = "\033[0m"

        self.stdout.write(f"{bold_magenta}Starting automatic Seeding...\n{reset}")

        try:
            self.stdout.write(f"{bold_cyan}Executing delete_all_data.py ...\n{reset}")
            call_command('delete_all_data')
            
            self.stdout.write(f"{bold_cyan}Executing auto_createsuperuser.py ...\n{reset}")
            call_command('auto_createsuperuser')

            self.stdout.write(f"{bold_cyan}Executing seed.py ...\n{reset}")
            call_command('seed')
            
            # <----- Add your desired scripts here :)

            self.stdout.write(f"{bold_magenta}SUCCESS:{reset} {bold_green}Automatic seeding completed successfully!{reset}")
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {e}"))
