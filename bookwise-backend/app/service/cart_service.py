from model.cart import Cart, CartItem
from model.book import Book
from model.user import User
from configuration.database import Session
import logging

class CartService:
    
    @staticmethod
    def get_or_create_cart(user_id):
        """
        Get user's active cart or create a new one
        
        Args:
            user_id: User ID
            
        Returns:
            Cart: User's active cart
        """
        session = Session()
        
        try:
            # Try to get existing active cart
            cart = session.query(Cart).filter(
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            # Create new cart if none exists
            if not cart:
                cart = Cart(user_id=user_id)
                session.add(cart)
                session.commit()
                session.refresh(cart)
            
            return cart
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error getting/creating cart: {e}")
            raise e
        finally:
            session.close()
    
    @staticmethod
    def add_item_to_cart(user_id, book_id, quantity=1):
        """
        Add item to user's cart
        
        Args:
            user_id: User ID
            book_id: Book ID to add
            quantity: Quantity to add
            
        Returns:
            dict: Result of adding item
        """
        session = Session()
        
        try:
            # Get or create cart
            cart = CartService.get_or_create_cart(user_id)
            
            # Get book details
            book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                return {'error': 'Book not found'}
            
            if not book.is_active:
                return {'error': 'Book is not available'}
            
            if book.stock_quantity < quantity:
                return {'error': f'Only {book.stock_quantity} items available in stock'}
            
            # Check if item already exists in cart
            existing_item = session.query(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.book_id == book_id
            ).first()
            
            if existing_item:
                # Update quantity
                new_quantity = existing_item.quantity + quantity
                if book.stock_quantity < new_quantity:
                    return {'error': f'Only {book.stock_quantity} items available in stock'}
                    
                existing_item.quantity = new_quantity
                cart_item = existing_item
            else:
                # Create new cart item
                cart_item = CartItem(
                    cart_id=cart.id,
                    book_id=book_id,
                    quantity=quantity,
                    unit_price=book.price
                )
                session.add(cart_item)
            
            session.commit()
            session.refresh(cart_item)
            
            return {
                'success': True,
                'cart_item': cart_item.to_dict(),
                'cart_total': float(cart.get_total_amount())
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding item to cart: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def update_cart_item(user_id, cart_item_id, quantity):
        """
        Update cart item quantity
        
        Args:
            user_id: User ID
            cart_item_id: Cart item ID to update
            quantity: New quantity
            
        Returns:
            dict: Result of updating item
        """
        session = Session()
        
        try:
            # Get cart item
            cart_item = session.query(CartItem).join(Cart).filter(
                CartItem.id == cart_item_id,
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            if not cart_item:
                return {'error': 'Cart item not found'}
            
            # Check stock availability
            book = cart_item.book
            if book.stock_quantity < quantity:
                return {'error': f'Only {book.stock_quantity} items available in stock'}
            
            # Update quantity
            cart_item.quantity = quantity
            session.commit()
            
            return {
                'success': True,
                'cart_item': cart_item.to_dict(),
                'cart_total': float(cart_item.cart.get_total_amount())
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating cart item: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def remove_cart_item(user_id, cart_item_id):
        """
        Remove item from cart
        
        Args:
            user_id: User ID
            cart_item_id: Cart item ID to remove
            
        Returns:
            dict: Result of removing item
        """
        session = Session()
        
        try:
            # Get cart item
            cart_item = session.query(CartItem).join(Cart).filter(
                CartItem.id == cart_item_id,
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            if not cart_item:
                return {'error': 'Cart item not found'}
            
            cart = cart_item.cart
            session.delete(cart_item)
            session.commit()
            
            return {
                'success': True,
                'cart_total': float(cart.get_total_amount()),
                'total_items': cart.get_total_items()
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error removing cart item: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def clear_cart(user_id):
        """
        Clear all items from user's cart
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Result of clearing cart
        """
        session = Session()
        
        try:
            # Get active cart
            cart = session.query(Cart).filter(
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            if not cart:
                return {'error': 'No active cart found'}
            
            # Delete all cart items
            session.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
            session.commit()
            
            return {
                'success': True,
                'message': 'Cart cleared successfully'
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error clearing cart: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def get_cart_contents(user_id):
        """
        Get user's cart contents
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Cart contents
        """
        session = Session()
        
        try:
            cart = session.query(Cart).filter(
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            if not cart:
                # Return empty cart structure
                return {
                    'cart': {
                        'id': None,
                        'items': [],
                        'total_amount': 0.0,
                        'total_items': 0
                    }
                }
            
            return {
                'cart': cart.to_dict()
            }
            
        except Exception as e:
            logging.error(f"Error getting cart contents: {e}")
            return {'error': str(e)}
        finally:
            session.close()