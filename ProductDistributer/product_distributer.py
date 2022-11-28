class ProductDistributer:
    """"
    Responsible for dividing the products to products to delete, configurable products, and simple products
    """
    def distribute(self, products_list):
        products_sets = {"to_delete": [],
                        "configurable": [],
                        "simple": []}

        for product in products_list:
            action = self.__get_product_action(product)

            products_sets[action].append(product)
        

        return products_sets

    def __get_product_action(self, product):
        if product["status"] == 2 or product["visibility"] == 1:
            return "to_delete"

        if product["type_id"] == "configurable":
            return "configurable"

        return "simple"