from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from offers.models import Offer
from session_cart.api.serializers import CartAddSerializer, CartUpdateSerializer

class CartView(APIView):
    def get(self, request):
        cart = request.session.get("cart", [])
        detailed_cart = []

        for item in cart:
            if "product_id" in item:
                try:
                    product = Product.objects.get(id=item["product_id"])
                    detailed_cart.append({
                        "type": "product",
                        "id": product.id,
                        "name": product.name,
                        "price": product.final_price,
                        "quantity": item["quantity"],
                        "total": product.final_price * item["quantity"],
                    })
                except Product.DoesNotExist:
                    continue
            elif "offer_id" in item:
                try:
                    offer = Offer.objects.get(id=item["offer_id"])
                    price = offer.price_after_discount or offer.price
                    detailed_cart.append({
                        "type": "offer",
                        "id": offer.id,
                        "name": offer.name,
                        "price": price,
                        "quantity": item["quantity"],
                        "total": price * item["quantity"],
                    })
                except Offer.DoesNotExist:
                    continue

        return Response(detailed_cart)

class CartAddView(APIView):
    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data

        cart = request.session.get("cart", [])

        # Check if item already in cart
        found = False
        for entry in cart:
            if item.get("product_id") and entry.get("product_id") == item["product_id"]:
                entry["quantity"] += item["quantity"]
                found = True
            elif item.get("offer_id") and entry.get("offer_id") == item["offer_id"]:
                entry["quantity"] += item["quantity"]
                found = True

        if not found:
            cart.append(item)

        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Item added to cart."}, status=status.HTTP_201_CREATED)

class CartUpdateView(APIView):
    def patch(self, request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        cart = request.session.get("cart", [])
        for entry in cart:
            if data.get("product_id") and entry.get("product_id") == data["product_id"]:
                entry["quantity"] = data["quantity"]
            elif data.get("offer_id") and entry.get("offer_id") == data["offer_id"]:
                entry["quantity"] = data["quantity"]

        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Cart updated."})

class CartRemoveView(APIView):
    def delete(self, request):
        product_id = request.query_params.get("product_id")
        offer_id = request.query_params.get("offer_id")
        cart = request.session.get("cart", [])
        cart = [item for item in cart if not (
            (product_id and str(item.get("product_id")) == product_id) or
            (offer_id and str(item.get("offer_id")) == offer_id)
        )]
        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Item removed from cart."})

class CartTotalView(APIView):
    def get(self, request):
        cart = request.session.get("cart", [])
        total = 0
        for item in cart:
            if "product_id" in item:
                try:
                    product = Product.objects.get(id=item["product_id"])
                    total += product.final_price * item["quantity"]
                except Product.DoesNotExist:
                    continue
            elif "offer_id" in item:
                try:
                    offer = Offer.objects.get(id=item["offer_id"])
                    price = offer.price_after_discount or offer.price
                    total += price * item["quantity"]
                except Offer.DoesNotExist:
                    continue
        return Response({"total": total})

class CartCountView(APIView):
    def get(self, request):
        cart = request.session.get("cart", [])
        return Response({"count": sum(item["quantity"] for item in cart)})
