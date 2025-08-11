from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from products.models import Product
from offers.models import Offer
from session_cart.api.serializers import CartAddSerializer, CartUpdateSerializer


class CartView(APIView):
    """
    Retrieve the full cart with product/offer details (UUID-based).
    """
    @swagger_auto_schema(
        operation_summary="Get detailed cart contents",
        operation_description="Returns all items in the cart with type, uuid, name, price, quantity, and total price."
    )
    def get(self, request):
        cart = request.session.get("cart", [])
        detailed_cart = []

        for item in cart:
            if "product_uuid" in item:
                try:
                    product = Product.objects.get(uuid=item["product_uuid"])
                    detailed_cart.append({
                        "type": "product",
                        "uuid": str(product.uuid),
                        "name": product.name,
                        "price": product.final_price,
                        "quantity": item["quantity"],
                        "total": product.final_price * item["quantity"],
                    })
                except Product.DoesNotExist:
                    continue
            elif "offer_uuid" in item:
                try:
                    offer = Offer.objects.get(uuid=item["offer_uuid"])
                    price = offer.price_after_discount or offer.price
                    detailed_cart.append({
                        "type": "offer",
                        "uuid": str(offer.uuid),
                        "name": offer.name,
                        "price": price,
                        "quantity": item["quantity"],
                        "total": price * item["quantity"],
                    })
                except Offer.DoesNotExist:
                    continue

        return Response(detailed_cart)


class CartAddView(APIView):
    """
    Add an item to the cart using UUIDs.
    """
    @swagger_auto_schema(
        operation_summary="Add item to cart",
        operation_description="Add a product or an offer to the cart using its UUID. If it already exists, quantity will be increased.",
        request_body=CartAddSerializer
    )
    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.validated_data

        # ✅ Convert UUID objects to strings before storing
        if item.get("product_uuid"):
            item["product_uuid"] = str(item["product_uuid"])
        if item.get("offer_uuid"):
            item["offer_uuid"] = str(item["offer_uuid"])

        cart = request.session.get("cart", [])

        found = False
        for entry in cart:
            if item.get("product_uuid") and entry.get("product_uuid") == item["product_uuid"]:
                entry["quantity"] += item["quantity"]
                found = True
            elif item.get("offer_uuid") and entry.get("offer_uuid") == item["offer_uuid"]:
                entry["quantity"] += item["quantity"]
                found = True

        if not found:
            cart.append(item)

        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Item added to cart."}, status=status.HTTP_201_CREATED)


class CartUpdateView(APIView):
    """
    Update the quantity of an item in the cart using UUIDs.
    """
    @swagger_auto_schema(
        operation_summary="Update cart item quantity",
        operation_description="Update quantity for a product or offer already in the cart using its UUID.",
        request_body=CartUpdateSerializer
    )
    def patch(self, request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # ✅ Convert UUIDs to strings
        if data.get("product_uuid"):
            data["product_uuid"] = str(data["product_uuid"])
        if data.get("offer_uuid"):
            data["offer_uuid"] = str(data["offer_uuid"])

        cart = request.session.get("cart", [])
        for entry in cart:
            if data.get("product_uuid") and entry.get("product_uuid") == data["product_uuid"]:
                entry["quantity"] = data["quantity"]
            elif data.get("offer_uuid") and entry.get("offer_uuid") == data["offer_uuid"]:
                entry["quantity"] = data["quantity"]

        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Cart updated."})


class CartRemoveView(APIView):
    """
    Remove an item from the cart using UUIDs.
    """
    @swagger_auto_schema(
        operation_summary="Remove cart item",
        operation_description="Remove a product or offer from the cart using UUID query parameters.",
        manual_parameters=[
            openapi.Parameter('product_uuid', openapi.IN_QUERY, description="UUID of the product to remove", type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
            openapi.Parameter('offer_uuid', openapi.IN_QUERY, description="UUID of the offer to remove", type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID)
        ]
    )
    def delete(self, request):
        product_uuid = request.query_params.get("product_uuid")
        offer_uuid = request.query_params.get("offer_uuid")
        cart = request.session.get("cart", [])
        cart = [item for item in cart if not (
            (product_uuid and str(item.get("product_uuid")) == product_uuid) or
            (offer_uuid and str(item.get("offer_uuid")) == offer_uuid)
        )]
        request.session["cart"] = cart
        request.session.modified = True
        return Response({"detail": "Item removed from cart."})


class CartTotalView(APIView):
    """
    Get the total price of all items in the cart (UUID-based).
    """
    @swagger_auto_schema(
        operation_summary="Get cart total price",
        operation_description="Returns the sum of (price * quantity) for all items, using UUID lookups."
    )
    def get(self, request):
        cart = request.session.get("cart", [])
        total = 0
        for item in cart:
            if "product_uuid" in item:
                try:
                    product = Product.objects.get(uuid=item["product_uuid"])
                    total += product.final_price * item["quantity"]
                except Product.DoesNotExist:
                    continue
            elif "offer_uuid" in item:
                try:
                    offer = Offer.objects.get(uuid=item["offer_uuid"])
                    price = offer.price_after_discount or offer.price
                    total += price * item["quantity"]
                except Offer.DoesNotExist:
                    continue
        return Response({"total": total})


class CartCountView(APIView):
    """
    Get the total quantity of all items in the cart (UUID-based).
    """
    @swagger_auto_schema(
        operation_summary="Get cart item count",
        operation_description="Returns the total number of items (sum of quantities) in the cart."
    )
    def get(self, request):
        cart = request.session.get("cart", [])
        return Response({"count": sum(item["quantity"] for item in cart)})
