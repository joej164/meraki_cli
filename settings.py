# Settings file for the library
import yaml
import dotenv
import os

from yaml.scanner import ScannerError
from pathlib import Path


class SettingsError(Exception):
    pass


class Settings():
    def __init__(self, settings_file=None):
        if settings_file is None:
            script_dir = Path(__file__).parents[0]
            self.settings_file = script_dir / "settings.yml"
        else:
            self.settings_file = Path(settings_file)

        self.meraki_dashboard_api_key = None              # Required
        self.meraki_web_username = None                   # Required
        self.meraki_web_password = None                   # Required
        self.meraki_vmx_sku = 'VMX100'
        self.meraki_org_name = 'Taco Bell POC'

        # Override the defaults above
        self.load_settings_file()
        self.load_env_settings()

    # Load data from the settings.yml file
    def load_settings_file(self):
        try:
            with open(self.settings_file, "r") as settings_file:
                data = yaml.safe_load(settings_file)
                for k, v in data.items():
                    setattr(self, k, v)
        except FileNotFoundError:
            # If the settings.yml file is missing, means use defaults
            pass
        except AttributeError as e:
            if str(e) == "'NoneType' object has no attribute 'items'":
                # The settings.yml file exists but is empty, use defaults
                pass
            else:
                raise
        except ScannerError as e:
            raise SettingsError("You have a malformed 'settings.yml' file.  "
                                "Please fix this.  The error can be found in "
                                f"the following message: {e}")

    def load_env_settings(self):
        dotenv.load_dotenv()
        envs = os.environ
        for k, v in envs.items():
            if "MERAKI" in k:
                setattr(self, k.lower(), v)
