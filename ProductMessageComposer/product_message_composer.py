def message_composer(product, type, variants = []):
    message = {}

    message["action"] = __set_action(message, type)

    message["sku"] = product["sku"]

    if type != "to_delete":
        message["body"] = __set_message_body(message, product, type, variants)
    
    return message

def __set_action(message, type):
    if type == "to_delete":
        return "Delete"
    elif type == "simple" or type == "configurable":
        return "Save"

def __set_message_body(message, product, type, variants):
    body = product
    
    if type == "configurable":
        body["all_children"] = variants

    return body