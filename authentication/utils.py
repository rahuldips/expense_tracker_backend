from django.db import transaction
from datetime import datetime, timedelta
from common.utils import (Q,ParameterMaster,UserToken)
from constants import (DB_STRF_TIME)
import logging,jwt

logger = logging.getLogger(__name__)

def generateRefreshToken(token):
    try:
        with transaction.atomic():
            parameter = ParameterMaster.objects.filter(Q(parameter_key="jwt_algo") | Q(parameter_key="jwt_secret")).values_list('parameter_value', flat=True)
            logger.info(f"Parameter Values : {parameter}")
            algo = str(parameter[0])
            secret = str(parameter[1])
            
            payload = jwt.decode(token, key=secret, algorithms=algo)
            logger.info(f"Token Decode Response : {payload}")
            
            user_id = payload.get('user_id')
            user_type = payload.get('user_type')
            position_id = payload.get('position_id')
            role_id = payload.get('role_id')
            role_code = payload.get('role_code')
            
            logger.info(f"User Id : {user_id} and User Type : {user_type}")
            logger.info(f"Old Token : {token}")
            
            expire_time_delta = ParameterMaster.objects.only('parameter_value').get(parameter_key="token_expire_time").parameter_value
            expire_time_delta = int(expire_time_delta)
            logger.info(f"Expire Time Delta : {expire_time_delta}")
            
            payload = {"user_id": user_id, "position_id":position_id, "user_type" : user_type, "role_id" : role_id, "role_code" : role_code, "exp": datetime.utcnow() + timedelta(minutes=expire_time_delta), "iat": datetime.utcnow()}
            logger.info(f"Payload: {payload}")

            # jwt_token = jwt.encode(payload=payload, key=secret, algorithm=algo).decode("utf-8")
            jwt_token = jwt.encode(payload=payload, key=secret, algorithm=algo)
            logger.info(f"New Token : {jwt_token}")

            token_id_exists = UserToken.objects.filter(user_id=user_id,user_type=user_type).exists()
            if token_id_exists:
                token_update_data = {"token":jwt_token, "expiry_time": payload['exp'].strftime(f'{DB_STRF_TIME}'), "updated_on":datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), "allow_flag":1}
                UserToken.objects.filter(user_id=user_id, user_type=user_type).update(**token_update_data)
                logger.warning(f"Refresh token updated for respective User | User Type -- {user_type}")

            else:
                user_data = {"user_id" : user_id, "user_type" : user_type, "token" : jwt_token, "allow_flag" : 1, "expiry_time": payload['exp'].strftime(f'{DB_STRF_TIME}'), "updated_on": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")}
                UserToken.objects.create(**user_data)
                logger.warning(f"Refresh token created for respective User | User Type -- {user_type}")
                
            return jwt_token   
    except Exception as e:
        logger.exception(e)
        return None

#! Exclusion API List
exclusion_list = [
                #! Health API
                '/cmosvc/health/',
                
                #! Graph QL
                '/cmographql/',
                
                #! Shared API
                # '/cmosvc/shared/getmasterdata/',
                '/cmosvc/shared/uploaddocuments/',
                
                #! User API
                '/cmosvc/user/generateotp/',
                '/cmosvc/user/login/',
                
                #! CallBack API
                '/cmosvc/initiate/autoreturn/',

                #! Public Show Grievance Status
                '/cmosvc/admin/publicshowgrievancestatus/',
            ]