def message_composer(product, type, variants = []):
    message = {}

    __set_action(message, type)
    message["sku"] = product["sku"]
    __set_message_body(message, product, type, variants)
    
    return message

def __set_action(message, type):
    if type == "to_delete":
        message["action"] = "Delete"
    elif type == "simple" or type == "configurable":
        message["action"] = "Save"

def __set_message_body(message, product, type, variants):
    message["body"] = product
    
    if type == "configurable":
        message["body"]["all_children"] = variants