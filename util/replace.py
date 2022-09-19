import datetime
def replace_text(data, text):
    for key, value in data.items():
        placeholder = '{{' + key + '}}'
        if isinstance(value, datetime.datetime):
            value = value.strftime("%d.%m.%Y")
        text = text.replace(placeholder, value)
    return text