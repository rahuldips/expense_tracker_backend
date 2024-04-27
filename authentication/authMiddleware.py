from django.http import HttpResponse
from django.contrib.auth.backends import BaseBackend
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import get_authorization_header
from datetime import (datetime,timedelta)
from administration.models import (ParameterMaster,UserToken,UserLoginActivity)
from .utils import (generateRefreshToken,exclusion_list)
from errorcodes import (CODE,MESSAGE,TOKEN)
from constants import (ACTIVE,INACTIVE,OPS_STRF_TIME)
import logging, jwt, json

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseBackend):
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # self.auth(request)
        auth_resp = self.auth(request)
        logger.info(f"Auth Response : {auth_resp}")
        if auth_resp is True:
            return self.get_response(request)
        else:
            # code = auth_resp['code']
            # message = auth_resp['message']
            code = auth_resp[CODE]
            message = auth_resp[MESSAGE]
            resp_data = None
            if code == 408:
                logger.info("<=========== Response Code 408 =========>")
                # new_token = auth_resp['token']
                new_token = auth_resp[TOKEN]
                logger.info(f"New Auth Token : {new_token}")
                # resp_data = {"message" : message, "token" : new_token}
                resp_data = {MESSAGE : message, TOKEN : new_token}
                resp_data = json.dumps(resp_data)
            else:
                logger.info("<=========== Response Code 403 =============>")
                # resp_data = {"message" : message}
                resp_data = {MESSAGE : message}
                resp_data = json.dumps(resp_data)
            logger.info(f"Resp Data : {resp_data}")
            resp = HttpResponse(resp_data, status=code, content_type ="application/json")
            return resp

    def auth(self,request):
        logger.warning(f"Request Path: {request.path}")
        if request.path not in exclusion_list:
            user_id = None
            user_type = None
            token = None
            try:
                #! Unauthorized Access
                # payload_admin_user_id = None
                # logger.warning(f'{request.method} Request Recieved at {datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')} in Authentication Module ------> {request}')
                
                # if request.method == "POST":
                #     # payload_admin_user_id = request.data['admin_user_id']   # if request.data.get('admin_user_id') else None
                #     payload_admin_user_id = request.POST['admin_user_id']     # if request.POST.get('admin_user_id') else None
                #     # payload_admin_user_id = daTa['admin_user_id'] if daTa.get('admin_user_id') else None
                #     logger.warning(f'Admin User ID Received in Payload -> {payload_admin_user_id}')
                # if request.method == "GET":
                #     payload_admin_user_id = request.GET.get("id")
                #     logger.warning(f'Admin User ID Received in Payload -> {payload_admin_user_id}')
                # #! ============================
                
                token = get_authorization_header(request).decode("utf-8")
                logger.info(f"Token received from client : {token}")
                
                with transaction.atomic():
                    products = ParameterMaster.objects.filter(Q(parameter_key="jwt_algo") | Q(parameter_key="jwt_secret")).values_list('parameter_value', flat=True)
                    algo = str(products[0])
                    secret = str(products[1])

                    payload = jwt.decode(token, key=secret, algorithms=algo)
                    logger.warning(f"Token Decode Response : {payload}")
                    
                    user_id = payload.get('user_id')
                    user_type = payload.get('user_type')
                    exp = payload.get('exp')
                    iat = payload.get('iat')
                    token_position_id = payload.get('position_id')

                    # #! Unauthorized Access
                    # if payload_admin_user_id not in (None,'',' ','null','None'):
                    #     logger.warning(f'Received Admin User ID -> {payload_admin_user_id} | Token User ID -> {user_id}')
                    #     if int(user_id) != int(payload_admin_user_id):
                    #         logger.error("Unauthorized Access")
                    #         # unauthorized_response = {"code" : status.HTTP_401_UNAUTHORIZED, "message" : "Unauthorized"}
                    #         unauthorized_response = {CODE : status.HTTP_401_UNAUTHORIZED, MESSAGE : "Unauthorized Access"}
                    #         return unauthorized_response
                    # else:
                    #     pass
                    # #! ===========================
                    
                    token_created_at = datetime.utcfromtimestamp(iat)
                    logger.warning(f"Token Created Time : {token_created_at} {iat}")
                    
                    expiry_time = datetime.utcfromtimestamp(exp)
                    logger.warning(f"Expire Time : {expiry_time}")
                    
                    val_time_delta = ParameterMaster.objects.only('parameter_value').get(parameter_key="token_validation_time").parameter_value
                    val_time_delta = int(val_time_delta)
                    logger.warning(f"Validation Time Delta : {val_time_delta}")
                    
                    validation_time = expiry_time - timedelta(minutes=val_time_delta)
                    logger.warning(f"Validation Time : {validation_time}")
                    
                    current_time = datetime.utcnow()
                    logger.warning(f"Current Time : {current_time}")
                    
                    userObj = UserToken.objects.get(user_id=user_id, user_type=user_type)
                    logger.info(f"userObj = {userObj}")
                    
                    if validation_time < current_time < expiry_time:
                        jwt_token = generateRefreshToken(token)
                        logger.error("Refresh Token Generate")
                        # expired_response = {"code" : status.HTTP_408_REQUEST_TIMEOUT, "message" : "Refresh Token Generate", "token" : jwt_token}
                        expired_response = {CODE : status.HTTP_408_REQUEST_TIMEOUT, MESSAGE : "Refresh Token Generate", TOKEN : jwt_token}
                        return expired_response
                    elif current_time > expiry_time:
                        logger.error("Token Expired. Updating User's Current Logged in activity to INACTIVE")
                        
                        #! Updating User Current Login Activy after token expired.
                        UserLoginActivity.objects.filter(admin_user_id=user_id,position_id=token_position_id,active_status=ACTIVE).update(logout_time=datetime.utcnow().strftime(f'{OPS_STRF_TIME}'),active_status=INACTIVE,updated_on=datetime.utcnow().strftime(f'{OPS_STRF_TIME}'))
                        logger.error('Current login activity set to INACTIVE after token expiry.')
                        
                        #! Invalidate Existing Token
                        token_id_exists = UserToken.objects.filter(user_id=user_id,user_type=user_type,token=token, allow_flag=1).exists()
                        if token_id_exists:
                            token_id = UserToken.objects.filter(user_id=user_id,user_type=user_type,token=token).get().token_id
                            # UserToken.objects.filter(token_id=token_id).update(updated_on=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),allow_flag=0)
                            UserToken.objects.filter(token_id=token_id).delete()
                            logger.info("Expired Token Deleted.")
                        
                        # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "Token Expired"}
                        expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "Token Expired"}
                        return expired_response
                    else:
                        user_token = userObj.token
                        logger.info(f"DB Token : {user_token}")
                        logger.info(f"Token : {token}")
                        if token == user_token:
                            return True
                        else:
                            logger.error("Token Mismatch")
                            # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "Token Missmatch"}
                            expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "Token Missmatch"}
                            return expired_response
            except jwt.DecodeError as d:
                logger.warning("<================= Token Decode Error ================>\n")
                logger.error(d)
                # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "JWT Decode Error"}
                expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "JWT Decode Error"}
                return expired_response
            except jwt.ExpiredSignatureError as x:
                logger.warning("<================= Token is Expired ================>\n")
                logger.error(x)
                logger.info(f"Expired Token :: {token}")
                # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "Token Time Out Error"}
                expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "Token Time Out Error"}
                return expired_response
            except jwt.InvalidTokenError as i:
                logger.warning("<================= Invalid Token Error ================>\n")
                logger.error(i)
                # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "Invalid Token Error"}
                expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "Invalid Token Error"}
                return expired_response
            except Exception as e:
                logger.warning("<================= Generic Exception ================>\n")
                logger.error(e)
                # expired_response = {"code" : status.HTTP_403_FORBIDDEN, "message" : "Generic Exception"}
                expired_response = {CODE : status.HTTP_403_FORBIDDEN, MESSAGE : "Generic Exception"}
                return expired_response
        else:
            return True