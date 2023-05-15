from typing import List, Dict, Union

from model.purchase import Purchase
from repository.book import BookRepository
from repository.purchase import PurchaseRepository
from repository.user import UserRepository

user_repository = UserRepository
book_repository = BookRepository
purchase_repository = PurchaseRepository


class PurchaseService:
    @staticmethod
    def create_purchase(id_user_token, request_data):
        user = user_repository.get_user_by_id(id_user_token)
        if not user:
            raise Exception('Authentication failed. Invalid or expired token.')

        if user.user_type_id == 1:
            raise Exception('Admin user cannot make purchases.')

        successful_purchases = []
        failed_purchases = []

        for book_data in request_data:
            book = None
            try:
                book = book_repository.get_book_by_id(book_data['id'])
                if not book:
                    raise Exception(f'Book with ID {book_data["id"]} not found.')

                book_stock = int(book.stock)

                if book_stock < book_data['quantity']:
                    raise Exception(f'Insufficient stock for book with ID {book_data["id"]}.')

                purchase = Purchase(
                    price=book_data['price'],
                    quantity=book_data['quantity'],
                    user_id=user.id,
                    book_id=book_data['id']
                )

                successful_purchases.append(purchase)

                if book_stock > book_data['quantity']:
                    book_stock -= book_data['quantity']
                    book.stock = book_stock
                    book_repository.update_book(book.id, stock=book_stock)
                else:
                    if book_stock == 1:
                        book.stock = 0
                        book_repository.update_book(book.id, stock=book.stock)

                purchase_repository.create_purchase(purchase)

                successful_purchases = [
                    {
                        'book_id': purchase.book_id,
                        'book_title': book.title if book else ''
                    }
                    for purchase in successful_purchases
                ]

            except Exception as e:
                failed_purchase = {
                    'book_id': book_data['id'],
                    'book_title': book.title if book else '',
                    'error_message': str(e)
                }
                failed_purchases.append(failed_purchase)

        return {
            'successful_purchases': successful_purchases,
            'failed_purchases': failed_purchases
        }

    @staticmethod
    def get_purchase(id_user_token):
        user = user_repository.get_user_by_id(id_user_token)
        if not user:
            raise Exception('Authentication failed. Invalid or expired token.')

        if user.user_type_id == 1:
            raise Exception('Admin user is not allowed to access purchase information.')

        purchases = purchase_repository.get_purchase_by_id_user(user.id)
        purchase_data = []

        for purchase in purchases:
            book = book_repository.get_book_by_id(purchase['book_id'])
            if book:
                purchase_info = {
                    'url_img': book.url_img,
                    'book_title': book.title,
                    'quantity': purchase['quantity'],
                    'price': purchase['price'],
                    'purchase_date': purchase['date']
                }
                purchase_data.append(purchase_info)

        return purchase_data






