from chatbot.bot import Bot

bot_duoc = Bot("Post_callout.json")
text_response = bot_duoc.next_sentence("alo")
resp = ""
for token in text_response:
    resp += token + "."
print(resp)
text_response = bot_duoc.next_sentence("a địa chỉ riêng ")
resp = ""
for token in text_response:
    resp += token + "."
print(resp)