import sys
import os

from pyway.settings import Settings
from pyway.settings import ConfigFile
from pyway.info import Info
from pyway.log import logger
from pyway.migrate import Migrate
from pyway.validate import Validate
from pyway.import_ import Import
from pyway.checksum import Checksum
from pyway.helpers import Utils
from pyway.version import __version__

def migrate(config: ConfigFile) -> None:
    # Validate first
    validate(config, skip_errors=True)

    logger.info('Starting migration process...')
    output = Migrate(config).run()
    logger.info(output)
    logger.info('Migration completed.')

def validate(config: ConfigFile, skip_errors: bool = False) -> None:
    logger.info('Starting validation process')
    output = Validate(config).run(skip_initial_check=True)
    logger.info(output)
    logger.info('Validation completed.')

def info(config: ConfigFile) -> None:
    logger.info('Gathering info...')
    tbl = Info(config).run()
    logger.info(tbl)

def import_(config: ConfigFile) -> None:
    logger.info("Importing schema...")
    migration_name = Import(config).run()
    logger.info(f"{migration_name} Imported")

def checksum(config: ConfigFile) -> None:
    logger.info("Updating checksum...")
    name, checksum = Checksum(config).run()
    logger.info(f"{name} checksum updated to {checksum}")

def cli() -> None:
    logger.info(f"PyWay {__version__}")

    config = Settings.parse_arguments()
    config_file = Settings.parse_config_file(config.config)
    config.merge(config_file)

    # --- DIFF LOGIC FOR ORACLE ---
    required_vars = ["database_type", "database_table", "database_name"]

    if config.database_type == "oracle":
        oracle_use_wallet = getattr(config, 'oracle_use_wallet', False)
        wallet_location = getattr(config, 'oracle_wallet_location', None) or os.getenv('TNS_ADMIN')
        has_username = getattr(config, 'database_username', None)

        if not oracle_use_wallet and not wallet_location and not has_username:
            required_vars.append("database_username")
    else:
        required_vars.extend(["database_host", "database_username"])
    # Validate required vars
    Utils.check_required_vars(required_vars, config)
    # --- END DIFF LOGIC ---

    if config.cmd == "info":
        info(config)
    elif config.cmd == "validate":
        validate(config)
    elif config.cmd == "migrate":
        migrate(config)
    elif config.cmd == "import":
        import_(config)
    elif config.cmd == "checksum":
        checksum(config)
    else:
        logger.error(f"Command '{config.cmd}' not recognized, exiting!")
        sys.exit(1)

if __name__ == '__main__':
    cli()