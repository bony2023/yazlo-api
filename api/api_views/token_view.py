from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from db_helper import *
from config import *

import datetime 

class TokenView(APIView):

    def get(self, request, *args, **kw): # create token
        app_id = request.GET.get('app_id', None)
        app_secret = request.GET.get('app_secret', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if app_id and app_secret:
            db = getDatabase()
            if db:
                users_collection = db.users
                tokens_collection = db.tokens
                user = users_collection.find_one({"application_id": app_id, "application_secret": app_secret})
                if user and user.get('email', None) != None:
                    token = tokens_collection.find_one({"author": user.get('email', None)})
                    access_token = token.get("token", None) if token else None
                    date_created = token.get("date_created", None) if token else None
                    if not access_token_valid(token):
                        access_token = getRandomToken(TOKEN_LENGTH)
                        date_created = datetime.datetime.utcnow()
                        if token and token.get('author', None) != None:
                            tokens_collection.update_one(
                                {"author": token.get('author')},
                                {
                                    "$set": {
                                        "token": access_token,
                                        "date_created": date_created
                                    }
                                }
                            )
                        else:
                            token = tokens_collection.insert_one(
                                {
                                    "author": user.get('email'),
                                    "token": access_token,
                                    "date_created": date_created
                                }
                            )
                    result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                    result[TOKEN_KEY] = access_token
                    result[TOKEN_DATE_CREATED] = date_created
                else:
                    result[RESPONSE_STATUS_ERROR_MSG] = USER_NOT_FOUND_FOR_API
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = API_CRED_MISSING
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def delete(self, request, *args, **kw): #deletes token
        access_token = request.META.get('HTTP_ACCESS_TOKEN', None)
        result = {}
        result[RESPONSE_STATUS] = RESPONSE_STATUS_ERROR
        if access_token:
            db = getDatabase()
            if db:
                tokens_collection = db.tokens
                if tokens_collection:
                    revoked = tokens_collection.delete_many(
                        {"token": access_token}
                    )
                    if revoked and revoked.deleted_count > 0:
                        result[RESPONSE_STATUS] = RESPONSE_STATUS_SUCCESS
                        result[RESPONSE_STATUS_SUCCESS_MSG] = TOKEN_ACCESS_REVOKED
                    else:
                        result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING
            else:
                result[RESPONSE_STATUS_ERROR_MSG] = MASTER_DB_UNINITIALIZED
        else:
            result[RESPONSE_STATUS_ERROR_MSG] = TOKEN_MISSING
        response = Response(result, status=status.HTTP_200_OK)
        return response