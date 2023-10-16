import heapq
import json


class Order:
    def __init__(
        self, order_type: int = 0, price: float = 0, qty: int = 0, order_id: str = None
    ):
        self.order_type = order_type  # 1 for bid, 0 for ask
        self.price = price
        self.qty = qty
        self.order_id = order_id

    def order_from_dict(order_dict: dict):
        return Order(
            order_type=int(order_dict["order_type"]),
            price=float(order_dict["price"]),
            qty=int(order_dict["qty"]),
            order_id=order_dict["order_id"],
        )

    def __gt__(self, other):
        return self.price > other.price

    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.price == other.price

    def __repr__(self):
        return (
            "Order ID: "
            + str(self.order_id)
            + ", "
            + "Price: "
            + str(self.price)
            + ", "
            + "Quantity: "
            + str(self.qty)
            + ", "
            + "Order Type: "
            + ("buy" if self.order_type else "sell")
        )


class Order_Book:
    def __init__(self):
        self.bids = []
        self.asks = []

    def __repr__(self):
        return "Bids:\n" + str(self.bids) + "\n" + "Asks:\n" + str(self.asks)

    def add_order(self, new_order: Order):
        if new_order.order_type:  # If it's a buy order ("bid")
            if len(self.asks) != 0:
                while self.asks[0].price <= new_order.price:
                    diff = self.asks[0].qty - new_order.qty
                    self.asks[0].qty = max(diff, 0)
                    new_order.qty = abs(min(diff, 0))
                    if self.asks[0].qty == 0:
                        heapq.heappop(self.asks)
                    if new_order.qty == 0 or len(self.asks) == 0:
                        break
            if new_order.qty > 0:
                heapq.heappush(self.bids, new_order)
        else:
            if len(self.bids) != 0:
                while self.bids[0].price >= new_order.price:
                    diff = self.bids[0].qty - new_order.qty
                    self.bids[0].qty = max(diff, 0)
                    new_order.qty = abs(min(diff, 0))
                    if self.bids[0].qty == 0:
                        heapq.heappop(self.bids)
                    if new_order.qty == 0 or len(self.bids) == 0:
                        break
            if new_order.qty > 0:
                heapq.heappush(self.asks, new_order)

    def read_order_from_json(self, filename="orders.json"):
        ordersJSON = open(filename)
        orders = json.load(ordersJSON)["orders"]
        orders.reverse()

        while len(orders) > 0:
            # self.add_order(Order.order_from_dict(orders.pop()))  ehhh lets make this verbose
            order = Order.order_from_dict(orders.pop())
            print("Adding Order: ", order)
            self.add_order(order)
            print(self, "\n")


if __name__ == "__main__":
    book = Order_Book()
    book.read_order_from_json("orders.json")

# def test():
#     book = Order_Book()
#     book.add_order(Order(0, 100, 10, "1"))  # Selling 10 @ 100
#     book.add_order(Order(1, 94, 5, "2"))  # Buying 5 @ 94
#     book.add_order(Order(1, 100, 2, "3"))  # Buying 2 @ 100, Partial fill on order #1
#     print(book)
#     book.add_order(
#         Order(0, 93, 7, "4")
#     )  # Selling 7 @ 93, Full fill on order #2, order for 2 @ 93 ends up top of ask heap
#     print(book)
