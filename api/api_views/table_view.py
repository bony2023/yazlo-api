from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bson.json_util import dumps
from bson.objectid import ObjectId
from db_helper import *
from config import *


class TableView(APIView):

    def get(self, request, *args, **kw): # get table details
        db_id = request.GET.get('db_id', None)
        table_id = request.GET.get('table_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token and db_id:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                if mainDB:
                    if ObjectId.is_valid(db_id):
                        if table_id:
                            if ObjectId.is_valid(table_id):
                                result[TABLE_KEY] = dumps(mainDB.tables.find_one({"database_id": ObjectId(db_id), "_id": ObjectId(table_id), "author": token['author']}))
                                result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                            else:
                                result[RESPONSE_STATUS_ERROR_MSG] = TABLE_ID_INVALID
                        else:
                            result[TABLE_KEY] = dumps(mainDB.tables.find({"database_id": ObjectId(db_id), "author": token['author']}))
                            result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    else:
                        result[RESPONSE_STATUS_ERROR_MSG] = DATABASE_ID_INVALID
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else DATABASE_ID_INVALID
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kw): #creates new table
        db_id = request.GET.get('db_id', None)
        table_name = request.GET.get('table_name', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token and db_id and ObjectId.is_valid(db_id) and table_name:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and user_total_tables(mainDB, ObjectId(db_id), token) >= TABLE_LIMIT_PER_DB:
                result[RESPONSE_STATUS_ERROR_MSG] = USER_REACHED_TABLE_LIMIT
            elif token and access_token_valid(token):
                table_name = ''.join(table_name.split(' ')).lower()
                table_created_same_name = mainDB.tables.find({"author": token["author"], "database_id": ObjectId(db_id), "table_name": table_name})
                if table_created_same_name.count() == 0:
                    table_data = request.data.get('table_data', None)
                    created_table = mainDB.tables.insert_one({"author": token["author"], "database_id": ObjectId(db_id), "table_name": table_name, "data": table_data})
                    result[TABLE_ID] = str(created_table.inserted_id)
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    result[RESPONSE_STATUS_SUCCESS_MSG] = TABLE_CREATED.format(table_name)
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = TABLE_WITH_SAME_NAME_CREATED
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else (DATABASE_ID_INVALID if (not db_id or not ObjectId.is_valid(db_id)) else TABLE_NAME_MISSING)
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def put(self, request, *args, **kw): # updates the table
        db_id = request.GET.get('db_id', None)
        table_id = request.GET.get('table_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if db_id and ObjectId.is_valid(db_id) and table_id and ObjectId.is_valid(table_id) and access_token:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                table = mainDB.tables.find_one({"author": token["author"], "database_id": ObjectId(db_id), "_id": ObjectId(table_id)})
                if table:
                    table_name = request.data.get('table_name', None) or table["table_name"]
                    table_name = ''.join(table_name.split(' ')).lower()
                    table_data = request.data.get('table_data', None) or table['data']
                    mainDB.tables.update_one(
                        {"_id": ObjectId(table_id), "author": token["author"], "database_id": ObjectId(db_id)}, 
                        {
                            "$set": {
                                "table_name": table_name,
                                "data": table_data
                            }
                        }
                    )
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    result[RESPONSE_STATUS_SUCCESS_MSG] = TABLE_UPDATED.format(table_name)
                    result[TABLE_ID] = table_id
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = TABLE_NOT_FOUND
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else (DATABASE_ID_INVALID if (not db_id or not ObjectId.is_valid(db_id)) else TABLE_ID_INVALID)
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def delete(self, request, *args, **kw): #deletes table
        db_id = request.data.get('db_id', None)
        table_id = request.data.get('table_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if db_id and ObjectId.is_valid(db_id) and access_token:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                if mainDB:
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    if table_id:
                        if ObjectId.is_valid(table_id):
                            result[DELETED_TABLE_COUNT] = mainDB.tables.delete_one({"_id": ObjectId(table_id), "author": token['author'], "database_id": ObjectId(db_id)}).deleted_count
                        else:
                            result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
                            result[RESPONSE_STATUS_ERROR_MSG] = TABLE_ID_INVALID
                    else:
                        result[DELETED_TABLE_COUNT] = mainDB.tables.delete_many({"author": token['author'], "database_id": ObjectId(db_id)}).deleted_count
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else DATABASE_ID_INVALID
        response = Response(result, status=status.HTTP_200_OK)
        return response