import os

# MongoDB Settings

MONGO_HOST = os.getenv('MONGO_HOST')


# API responses and codes

RESPONSE_STATUS = 'status'
RESPONSE_STATUS_SUCCESS = 'success'
RESPONSE_STATUS_SUCCESS_MSG = 'success_msg'
RESPONSE_STATUS_ERROR = 'error'
RESPONSE_STATUS_ERROR_MSG = 'error_msg'
RESPONSE_STATUS_SUCCESS_MSG = 'success_msg'


# Token Settings

TOKEN_TIMEOUT = 1 * 60 * 60 # 1 Hour / 3600 seconds
TOKEN_LENGTH = 42
TOKEN_KEY = 'token'
TOKEN_DATE_CREATED = 'date_created'
TOKEN_ACCESS_REVOKED = 'Token access revoked'
TOKEN_MISSING = 'No token found'
USER_NOT_FOUND_FOR_API = 'No user found for provided application ID and application secret'
MASTER_DB_UNINITIALIZED = 'Master DB not initialized'
API_CRED_MISSING = 'Missing application ID or application secret'
ACCESS_TOKEN_INVALID = 'Access token not valid'


# Database Settings

DATABASE_ID_MISSING = 'No Database ID found'
DATABASE_KEY = 'database_data'
DATABASE_ID_INVALID = 'Invalid Database ID'
DELETED_DATABASE_COUNT = 'Databases deleted'
DB_LIMIT_PER_USER = 1
USER_REACHED_DB_LIMIT = 'Maximum number of Databases ({}) have already been created'.format(DB_LIMIT_PER_USER)
DB_WITH_SAME_NAME_CREATED = 'A database with same name has already been created. Please choose a different name'
DATABASE_ID = 'db_id'
DB_CREATED = 'Database created with name {}'
DATABASE_NAME_MISSING = 'Database name is required'
DATABASE_UPDATED = 'Database {} updated'
DATABASE_NOT_FOUND = 'No Database found for given database ID'


# Table Settings

TABLE_ID_INVALID = 'Invalid Table ID'
TABLE_KEY = 'tables_data'
TABLE_NAME_MISSING = 'Table name is required'
TABLE_LIMIT_PER_DB = 3
USER_REACHED_TABLE_LIMIT = 'Maximum number of Tables ({}) have already been created'.format(TABLE_LIMIT_PER_DB)
TABLE_WITH_SAME_NAME_CREATED = 'A table with same name has already been created. Please choose a different name'
TABLE_ID = 'table_id'
TABLE_CREATED = 'Table created with name {}'
TABLE_NOT_FOUND = 'No Table found for given database ID and table ID'
TABLE_UPDATED = 'Table {} updated'
DELETED_TABLE_COUNT = 'Tables deleted'