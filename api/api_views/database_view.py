from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from bson.json_util import dumps
from bson.objectid import ObjectId
from db_helper import *
from config import *

class DatabaseView(APIView):

    def get(self, request, *args, **kw): # get database details
        db_id = request.GET.get('db_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                if mainDB:
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    if db_id:
                        if ObjectId.is_valid(db_id):
                            result[DATABASE_KEY] = dumps(mainDB.databases.find_one({"_id": ObjectId(db_id), "author": token['author']}))
                        else:
                            result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
                            result[RESPONSE_STATUS_ERROR_MSG] = DATABASE_ID_INVALID
                    else:
                        result[DATABASE_KEY] = dumps(mainDB.databases.find({"author": token['author']}))
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def post(self, request, *args, **kw): #creates new database
        db_name = request.GET.get('db_name', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token and db_name:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and user_total_db(mainDB, token) >= DB_LIMIT_PER_USER:
                result[RESPONSE_STATUS_ERROR_MSG] = USER_REACHED_DB_LIMIT
            elif token and access_token_valid(token):
                db_name = ''.join(db_name.split(' ')).lower()
                created_db = mainDB.databases.insert_one({"author": token["author"], "database_name": db_name})
                result[DATABASE_ID] = str(created_db.inserted_id)
                result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                result[RESPONSE_STATUS_SUCCESS_MSG] = DB_CREATED.format(db_name)
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else DATABASE_NAME_MISSING
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def put(self, request, *args, **kw): # updates the database
        db_id = request.GET.get('db_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if db_id and access_token:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                if ObjectId.is_valid(db_id):
                    database = mainDB.databases.find_one({"author": token["author"], "_id": ObjectId(db_id)})
                    if database:
                        db_name = request.GET.get('db_name', None) or database["database_name"]
                        db_name = ''.join(db_name.split(' ')).lower()
                        mainDB.databases.update_one(
                            {"_id": ObjectId(db_id), "author": token["author"]}, 
                            {
                                "$set": {
                                    "database_name": db_name,
                                }
                            }
                        )
                        result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                        result[RESPONSE_STATUS_SUCCESS_MSG] = DATABASE_UPDATED.format(db_name)
                        result[DATABASE_ID] = db_id
                    else:
                        result[RESPONSE_STATUS_ERROR_MSG] = DATABASE_NOT_FOUND
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = DATABASE_ID_INVALID
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if not access_token else DATABASE_ID_INVALID
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def delete(self, request, *args, **kw): #deletes database
        db_id = request.GET.get('db_id', None)
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token:
            mainDB = getDatabase()
            token = mainDB.tokens.find_one({"token": access_token}) if mainDB else None
            if token and access_token_valid(token):
                if mainDB:
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    if db_id:
                        if ObjectId.is_valid(db_id):
                            result[DELETED_DATABASE_COUNT] = mainDB.databases.delete_many({"_id": ObjectId(db_id), "author": token['author']}).deleted_count
                        else:
                            result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
                            result[RESPONSE_STATUS_ERROR_MSG] = DATABASE_ID_INVALID
                    else:
                        result[DELETED_DATABASE_COUNT] = mainDB.databases.delete_many({"author": token['author']}).deleted_count
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = ACCESS_TOKEN_INVALID
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING if db_id else DATABASE_ID_MISSING
        response = Response(result, status=status.HTTP_200_OK)
        return response