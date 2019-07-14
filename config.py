MODE = 'client'

CALL_CENTERS = [
    # (phone, name, type)
    #('18001111', 'Dược Call In', 0),
    ('18002222', 'Dược Call Out', 1),
    ('18003333', 'Pizza Call In', 0),
    #('18004444', 'Pizza Call Out', 1)
]

CLIENTS = [
    # (id, name, token)
    ('cuongdm' , 'Đinh Mạnh Cường', 'cOvYK92IIko:APA91bH-Bt1w0vYH8xDT3a6BiOEnM7wqIwoWa-YvnE4XsIcZ-fjfr_DBQGTNw_O9vmeQRQDYa7ShiEjuHsxXX50V700XaV_OmIr0u0K82gfaLxK9-jqB_Wo4IXXjG5fIrJbK0ziUcTyP'),
    ('duytk', 'Triệu Khương Duy', 'dWRTiG7Immk:APA91bFJGDMzu4VLjo1BiUnwKpdmzYK-Rt03TL7fhJPDIDFO9dMzIC6_rniq79EuWTxGNb9u8N36hkvA_2g30hPiXo0NOnmTmq4XmAmS1NxxTREP_Im4vDDIKxRqGdVUTUK4EWiqhq-A'),
    ('chiendb', 'Đặng Bảo Chiến', 'dj3evCalvSs:APA91bHZmHbU7_LbtEPWUlzLuwVdN8fYc2_NlHP-ihSsEMtkx2JKGLwGcHRoYsm84peZFOfUc-wPDdj4wwYQu8VA2bejMeWHuPZCD02QUWrw24VWAapa97k0L79ct1pvizQtndGQLO53'),
    ('baonq', 'Nguyễn Quốc Bảo', 'egi4MbrOBtM:APA91bEWBvHjnehtvpQxukIrKg8MEUpFXGIOwWhL_LPtPCBPtXxwjk_cOzxeSYVP0ubxXHkuC_MdKfYQRVLb1eX7lDWt6oge6sa8JWaXvUfILrwR6s-haRvRE1VgO242TyDrBzOsXvU6'),
]
FCM_APIKEY = 'AAAAMDfbpUs:APA91bFx3HK2UvyhzwZLEad_9N5J8leH5dK81uzzJJVt7oXHbNrKgdtryLbjp8bc4yP5MhSpH5xG0OPn6LfRKOBCAqDo53G8K1xGnLQ9fgnAQV_hrLT_1gKwlnOHTtl9gCC6XISNv7Rk'

ASR_URI = '123.31.18.120:50050'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

TTS_URL = 'https://merlin-tts.kiki.laban.vn/api/end2end/path'
TTS_CACHE = 'https://merlin-tts.kiki.laban.vn/api/end2end/cache'
TTS_TIMEOUT = 3

CHATBOT_URI = 'localhost:50052'

if MODE == 'server':
    ASR_URI = 'localhost:50050'
