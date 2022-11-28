
from Database.data_retrival import DataRetrival
from ProductDistributer.product_distributer import ProductDistributer
from ProductMessageComposer.product_message_composer import message_composer
from QueuingWrapper.queuing_wrapper import SQSWrapper

def create_variants_configurale_map(items):
    variants_configurables_map = {}
    variants_ids = []

    for _idx, item in enumerate(items):
        if ("type_id" not in item or item["type_id"] != "configurable"):
            continue

        if ("extension_attributes" not in item or "configurable_product_links" not in item[
            "extension_attributes"] or len(item["extension_attributes"]["configurable_product_links"]) == 0):
            continue

        variant_product_ids = item["extension_attributes"]["configurable_product_links"]
        variants_ids += variant_product_ids
        for _id in variant_product_ids:
            variants_configurables_map[_id] = _idx

    return variants_configurables_map, variants_ids

def create_configurale_child_map(variants_ids, variants_configurables_map, lang):
    variants_data_retrival = DataRetrival(lang, variants_ids)

    configurables_variants_map = {}

    data = variants_data_retrival.get_prducts_data(variants_ids)
    
    for product in data:
        product_id = product["id"]
        child_info = product

        configurable_idx = variants_configurables_map[product_id]
        if (configurable_idx in configurables_variants_map):
            configurables_variants_map[configurable_idx].append(child_info)
        else:
            configurables_variants_map[configurable_idx] = [child_info]

    return configurables_variants_map

def prepare_configurable_products_variants(items, lang):
    variants_ids = []

    variants_configurables_map, variants_ids = create_variants_configurale_map(items)

    return create_configurale_child_map(variants_ids, variants_configurables_map, lang)

def create_products_messages(products_sets, configurables_variants_map):
    messages = []
    
    #1- append simple products
    for prouct in products_sets["simple"]:
        messages.append(message_composer(prouct, "simple"))

    #2- append configurabe
    for idx, product in enumerate(products_sets["configurable"]):
        messages.append(message_composer(product, "configurable", configurables_variants_map[idx]))

    #3- append messages to delete
    for idx, product in enumerate(products_sets["to_delete"]):
        messages.append(message_composer(product, "to_delete"))

    return messages


def run(lang, products_ids):
    products_retrival = DataRetrival(lang, products_ids)
    product_distributer = ProductDistributer()
    sqs_wrapper = SQSWrapper(lang)

    #1- catch products
    products = products_retrival.get_prducts_data(products_ids)

    #2- distribute products
    products_sets = product_distributer.distribute(products)

    #3- get configurable variants
    configurables_variants_map = prepare_configurable_products_variants(products_sets["configurable"], lang=lang)

    #3- create products messages
    messages = create_products_messages(products_sets, configurables_variants_map)

    #4- push messages to products sqs
    sqs_wrapper.write_bulk_messages(messages)
    