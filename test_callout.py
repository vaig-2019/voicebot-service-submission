from pyfcm import FCMNotification
import config
call_center_code = '18002222'
registration_ids = ['cOvYK92IIko:APA91bH-Bt1w0vYH8xDT3a6BiOEnM7wqIwoWa-YvnE4XsIcZ-fjfr_DBQGTNw_O9vmeQRQDYa7ShiEjuHsxXX50V700XaV_OmIr0u0K82gfaLxK9-jqB_Wo4IXXjG5fIrJbK0ziUcTyP']

push_service = FCMNotification(api_key='AAAAMDfbpUs:APA91bFx3HK2UvyhzwZLEad_9N5J8leH5dK81uzzJJVt7oXHbNrKgdtryLbjp8bc4yP5MhSpH5xG0OPn6LfRKOBCAqDo53G8K1xGnLQ9fgnAQV_hrLT_1gKwlnOHTtl9gCC6XISNv7Rk')
result = push_service.notify_multiple_devices(
    registration_ids=registration_ids,
    data_message={'phoneNumber': call_center_code})
print(result)