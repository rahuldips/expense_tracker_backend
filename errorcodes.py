# ERROR FRAMEWORK
"""
    Master Error Framework for Expense Lifecycle Tracker
"""
#! Error Keys

DATA = 'Data'
ERROR = 'Errors'
TOKEN = 'Token'
EXCEPTION = 'Exception'
CODE = 'Code'
MESSAGE = 'Message'

#! Success Cases
SUCCESS_STATUS = 200
SUCCESSCODE = '001'
SUCCESSMESSAGE = 'Success'

#! Error Codes & Error Messages [System, Information, Business & Warning]
"""
    BUSINESS ERROR
"""
BUSSINESS_EXC_STATUS = 310

BE001 = 'BE001'
BE001MESSAGE = 'Missing Mandatory Inputs.'

BE002 = 'BE002'
BE002MESSAGE = '{} not found'

BE003 = 'BE003'
BE003MESSAGE = '{} found'

BE004 = 'BE004'
BE004MESSAGE = 'Tentative Date Must Be Greater Than Today.'

BE005 = 'BE005'
BE005MESSAGE = 'Contact Date is Not Correct.'

BE006 = 'BE006'
BE006MESSAGE = 'Condition Not Satisfied.'

"""
    INFORMATIONAL ERROR
"""
INFO_EXC_STATUS = 311

IN001 = 'IN001'
IN001MESSAGE = 'Username Must be a Phone Number or an Email.'

IN002 = 'IN002'
IN002MESSAGE = 'Please Provide a Valid Primary Phone Number.'

IN0021 = 'IN0021'
IN0021MESSAGE = 'Please Provide a Valid Alternative Phone Number.'

IN003 = 'IN003'
IN003MESSAGE = 'Please Provide a Valid Email Id.'


"""
    SYSTEM ERRORS
"""
SYS_EXC_STATUS = 312

SE001 = 'SE001'
SE001MESSAGE = 'Oops!!! Something Went Wrong. Please Try Again Later.'

SE002 = 'SE002'
SE002MESSAGE = 'Operational Error'

"""
    WARNINGS
"""
WARN_EXC_STATUS = 313

WA001 = 'WA001'
WA001MESSAGE = 'OTP Expired'

WA002 = 'WA002'
WA002MESSAGE = 'Invalid OTP'

WA003 = 'WA003'
WA003MESSAGE = 'Duplicate {} Entry Found'

WA004 = 'WA004'
WA004MESSAGE = 'No OTP Found. Please Request for a New OTP'

WA005 = 'WA005'
WA005MESSAGE = 'Operation not permitted'

WA006 = 'WA006'
WA006MESSAGE = 'Unauthorized Access'

WA007 = 'WA007'
WA007MESSAGE = 'No Data Available'

WA008 = 'WA008'
WA008MESSAGE = 'User Has Been Logged Out Already.'

#! Status Codes
NO_CONTENT_EXC_STATUS = 204
OPERATIONAL_EXCEPTION = 230
DETAIL_LIST_EXCEED_ERROR = 231
TICKET_NOT_FOUND_EXCEPTION = 232
MADATORY_FIELD_NOT_FOUND_EXCEPTION = 233
GEN_EXCEPTION = 234
UNAUTHORIZE_ACCESS = 401
REQUEST_TIMEOUT = 408
UNSUPPORTED_MEDIA = 415
INTERNAL_SERVER_ERROR = 500

#! ==============================================================================================
#! ======================================== EOF =================================================
#! ==============================================================================================