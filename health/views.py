from django.shortcuts import render

# Create your views here.

# from django.http import JsonResponse
# from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from errorcodes import (CODE,DATA,ERROR,EXCEPTION,MESSAGE,TOKEN,SUCCESSCODE,SUCCESSMESSAGE,SUCCESS_STATUS,SE001,SE001MESSAGE)
from shared.error_operation import (customExceptionBuilder)
import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def HealthCheck(request):
    logger.warning('================================== START - Application Health =================================')
    response,exception,error,token,cursor,statusCode = {},False,None,None,None,SUCCESS_STATUS
    try:
        sysTimeNow = datetime.now().strftime('%d-%m-%Y, %I:%M:%S.%f %p')
        logger.info(f'Expense Tracker Health Check API - System Local Time : >>>> {sysTimeNow}')
        output = {}
        output[CODE] = SUCCESSCODE
        output['Time'] = sysTimeNow
        output['Condition'] = "OK"
        output['DjangoApp'] = "Expense Lifecycle Tracker Health Check API"
        output[MESSAGE] = SUCCESSMESSAGE
        response,statusCode = output,SUCCESS_STATUS
    except Exception as e:
        logger.exception(e)
        exc = customExceptionBuilder(SE001,SE001MESSAGE)
        logger.warning(f"{exc.error},{exc.exception},{exc.response},{exc.statusCode}")
        error,exception,response,statusCode = exc.error,exc.exception,exc.response,exc.statusCode
    finally:
        if cursor is not None :
            cursor.close()
        logger.warning('=================================== END - Application Health ==================================\n')
        return Response(status = statusCode, data = {DATA:response,EXCEPTION:exception,ERROR:error,TOKEN:token})