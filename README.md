| PYWAY_SQL_MIGRATION_SUFFIXES | | Suffix extension for migration files | .sql |
| PYWAY_TABLE | --database-table | Name of schema history table | *None* |
| PYWAY_TYPE | --database-type | Data Base Management System [`postgres`, `mysql`, `duckdb`, `sqlite`, `oracle` ] | *None* *required* |
| PYWAY_DATABASE_HOST | --database-host | Host to connect to the database (optional for Oracle TNS Names) | *None* |
| PYWAY_DATABASE_PORT | --database-port | Port to connect to the database | *None* |
| PYWAY_DATABASE_NAME | --database-name | Name of database to connect | *None* |
| PYWAY_DATABASE_USERNAME |--database-username | User to use to connect to the database (optional for Oracle Wallet) | *None* |
| PYWAY_DATABASE_PASSWORD | --database-password | Password to use to connect to the database | *None* |
| PYWAY_DATABASE_COLLATION | --database-collation | Collation type to use in the database | MySQL: utf8mb4_general_ci Postgres/Oracle: *not supported*|
| PYWAY_ORACLE_CLIENT_LIB_DIR | | Path to Oracle Instant Client library directory (Oracle only) | *None* |
| PYWAY_ORACLE_WALLET_LOCATION | | Path to Oracle Wallet directory (Oracle only) | *None* |
| PYWAY_ORACLE_USE_WALLET | | Force Oracle Wallet authentication (Oracle only) | *False* |
| PYWAY_CONFIG_FILE | -c, --config | Configuration file | .pyway.conf |
| | --schema-file | Used when importing a schema file | |
| | --checksum-file | Used when updating a checksum - *advanced use*! | |

_Oracle with TNS Names:_
```
database_type: oracle
database_username: system
database_password: oracle123
database_name: PROD_DB
database_migration_dir: schema
database_table: pyway
# Optional: Oracle Instant Client library path (if not using Thin mode)  
oracle_client_lib_dir: C:\instantclient_21_3
```

_Oracle with Wallet Authentication:_
```
database_type: oracle
database_name: PROD_DB
database_migration_dir: schema
database_table: pyway
# Oracle Wallet configuration
oracle_use_wallet: true
oracle_wallet_location: C:\oracle\wallet
oracle_client_lib_dir: C:\instantclient_21_3
```

_Oracle with Full DSN:_
```
database_type: oracle
database_name: (DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=server.company.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=orcl)))
database_username: system
database_password: oracle123
database_migration_dir: schema
database_table: pyway
oracle_client_lib_dir: C:\instantclient_21_3
```

## Oracle Client Configuration

PyWay supports multiple Oracle connection methods with flexible configuration options:

### Connection Types Supported:

| Method | Required Fields | Optional Fields | Use Case |
|--------|----------------|-----------------|----------|
| **Easy Connect** | `database_host`, `database_name`, `database_username` | `database_port`, `database_password` | Direct connection to known server |
| **TNS Names** | `database_name`, `database_username` | `database_password` | Using tnsnames.ora aliases |
| **Full DSN** | `database_name` (with full DSN), `database_username` | `database_password` | Complex connection requirements |
| **Oracle Wallet** | `database_name` | `oracle_wallet_location`, `oracle_use_wallet` | Secure environments without stored credentials |

### Client Modes:

#### Thin Mode (Default)
PyWay will attempt to use Oracle's Thin mode by default, which doesn't require Oracle Client installation. This mode works for most use cases and supports:
- Basic authentication (username/password)
- TNS Names (if `tnsnames.ora` is accessible)
- Simple connection strings

#### Thick Mode (Oracle Instant Client)
For advanced Oracle features or when Thin mode doesn't work in your environment, you can configure the Oracle Instant Client path:

1. Download Oracle Instant Client from Oracle's website
2. Extract it to a directory (e.g., `C:\instantclient_21_3`)  
3. Configure the path in your configuration file:
   ```
oracle_client_lib_dir: C:\instantclient_21_3
   ```
4. Alternatively, set the environment variable:
   ```
   set ORACLE_CLIENT_LIB_DIR=C:\instantclient_21_3
   ```

**Note:** If the `oracle_client_lib_dir` path is invalid or not found, PyWay will automatically fall back to Thin mode.

#### Oracle Wallet Authentication
PyWay supports Oracle Wallet for secure authentication without storing credentials in configuration files.

**Configuration Options:**
1. **Explicit Wallet Configuration:**
   ```
oracle_use_wallet: true
oracle_wallet_location: C:\oracle\wallet
   ```

2. **Environment Variable (TNS_ADMIN):**
   ```
   set TNS_ADMIN=C:\oracle\wallet
   ```

3. **Auto-detection:** PyWay will automatically use wallet authentication if:
   - `TNS_ADMIN` is set and no username is provided
   - `oracle_wallet_location` is configured and no username is provided

**Wallet Setup Requirements:**
- Oracle Wallet must be configured with auto-login enabled
- `tnsnames.ora` and `sqlnet.ora` must be in the wallet directory
- Connection alias must be defined in `tnsnames.ora`

### Oracle Connection Troubleshooting

#### Common Issues:

**1. Connection Hangs or Timeouts:**
- Verify TNS name exists: `tnsping YOUR_TNS_NAME`
- Check network connectivity and firewall settings
- Ensure Oracle service is running

**2. "Missing option or not valid" (ORA-00922):**
- Check SQL syntax in migration files
- Ensure files end with proper semicolon
- Verify Oracle-specific syntax (use `NUMBER` instead of `INTEGER` for primary keys)

**3. Wallet Authentication Fails:**
- Verify `TNS_ADMIN` environment variable points to wallet directory
- Ensure wallet has auto-login enabled: `mkstore -wrl /path/to/wallet -createCredential`
- Check that `sqlnet.ora` contains: `WALLET_LOCATION=(SOURCE=(METHOD=FILE)(METHOD_DATA=(DIRECTORY=/path/to/wallet)))`

**4. Oracle Client Issues:**
- Verify Oracle Instant Client path is correct
- Ensure required libraries are in the path
- PyWay will automatically fallback to Thin mode if client fails
