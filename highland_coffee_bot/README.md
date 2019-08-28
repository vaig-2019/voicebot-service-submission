## Kịch bản

BOT: Kính chào quý khách, high land bot của hệ thống nhà hàng high land coffee có thể giúp gì anh chị ạ

> anh muốn order em ơi

BOT: Vâng ạ, vậy quý khách muốn đặt loại gì vậy

> cho anh trà sen vàng em ạ

BOT: Quý khách muốn mua cỡ lớn, nhỏ hay vừa vậy ạ

> cho anh size lớn

BOT: Quý khách muốn đặt mấy cốc trà sen vàng

> cho anh 1 thôi

BOT: Quý khách cho high land bot xin địa chỉ nhận hàng ạ

> gửi cho anh tới số 29 cầu giấy nha em

BOT: Cho em hỏi thông tin đơn hàng: 1 cốc trà sen vàng cỡ lớn chuyển tới 29 cầu giấy đúng không ạ

> ok đúng rồi em

BOT: Đơn hàng của quý khách đã được xác nhận, bên high land bot sẽ cho người đi giao hàng cho quý khách ngay.Cảm ơn quý khách đã tin tưởng sử dụng sản phẩm của hệ thống nhà hàng high land coffee. Chúc quý khách ngon miệng


## Deploy

Copy file `highland-coffee-bot.py` và file `knowledge/bot_data.json` tới nơi cài đặt

```text
from highland-coffee-bot import HighLandCoffeeBot

bot = HighLandCoffeeBot()

# lấy lời chào đầu tiên của bot
bot_mess = bot.interactive()

# lấy phản hồi của bot từ mess của user
bot_mess = bot.interactive(user_message=<your_mess>)

# end signal
END_SIGNAL = "_END_."

```