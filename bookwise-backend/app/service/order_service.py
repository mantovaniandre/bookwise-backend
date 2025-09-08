from model.order import Order, OrderItem, OrderStatus, PaymentStatus
from model.cart import Cart, CartItem
from model.book import Book
from configuration.database import Session
from service.payment_service import PaymentService
import logging
from decimal import Decimal

class OrderService:
    
    @staticmethod
    def create_order_from_cart(user_id, payment_method_id=None, shipping_address_id=None):
        """
        Create an order from user's active cart
        
        Args:
            user_id: User ID
            payment_method_id: Payment method ID (optional)
            shipping_address_id: Shipping address ID (optional)
            
        Returns:
            dict: Created order data or error
        """
        session = Session()
        
        try:
            # Get active cart
            cart = session.query(Cart).filter(
                Cart.user_id == user_id,
                Cart.status == 'active'
            ).first()
            
            if not cart or not cart.items:
                return {'error': 'No items in cart'}
            
            # Verify stock availability for all items
            for cart_item in cart.items:
                book = cart_item.book
                if not book.is_active:
                    return {'error': f'Book "{book.title}" is no longer available'}
                    
                if book.stock_quantity < cart_item.quantity:
                    return {'error': f'Only {book.stock_quantity} copies of "{book.title}" available'}
            
            # Calculate order amounts
            subtotal = cart.get_total_amount()
            tax_amount = OrderService._calculate_tax(subtotal)
            shipping_amount = OrderService._calculate_shipping(cart)
            total_amount = subtotal + tax_amount + shipping_amount
            
            # Create order
            order = Order(
                user_id=user_id,
                subtotal=subtotal,
                tax_amount=tax_amount,
                shipping_amount=shipping_amount,
                total_amount=total_amount
            )
            
            if payment_method_id:
                order.payment_method_id = payment_method_id
            if shipping_address_id:
                order.shipping_address_id = shipping_address_id
                
            session.add(order)
            session.flush()  # Get order ID
            
            # Create order items from cart items
            for cart_item in cart.items:
                book = cart_item.book
                order_item = OrderItem(
                    order_id=order.id,
                    book_id=cart_item.book_id,
                    book_title=book.title,
                    book_author=book.author,
                    unit_price=cart_item.unit_price,
                    quantity=cart_item.quantity
                )
                session.add(order_item)
                
                # Reserve stock
                book.reduce_stock(cart_item.quantity)
            
            # Mark cart as converted
            cart.status = 'converted'
            
            session.commit()
            session.refresh(order)
            
            return {
                'success': True,
                'order': order.to_dict()
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error creating order from cart: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def get_user_orders(user_id, status=None, page=1, per_page=10):
        """
        Get user's orders with pagination
        
        Args:
            user_id: User ID
            status: Optional status filter
            page: Page number
            per_page: Items per page
            
        Returns:
            dict: Orders data with pagination info
        """
        session = Session()
        
        try:
            query = session.query(Order).filter(Order.user_id == user_id)
            
            if status:
                query = query.filter(Order.status == status)
            
            # Order by creation date (newest first)
            query = query.order_by(Order.created_at.desc())
            
            # Calculate pagination
            total_orders = query.count()
            offset = (page - 1) * per_page
            orders = query.offset(offset).limit(per_page).all()
            
            return {
                'orders': [order.to_dict() for order in orders],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total_orders,
                    'pages': (total_orders + per_page - 1) // per_page
                }
            }
            
        except Exception as e:
            logging.error(f"Error getting user orders: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def get_order_details(order_id, user_id=None):
        """
        Get detailed order information
        
        Args:
            order_id: Order ID
            user_id: Optional user ID for ownership validation
            
        Returns:
            dict: Order details or error
        """
        session = Session()
        
        try:
            query = session.query(Order).filter(Order.id == order_id)
            
            if user_id:
                query = query.filter(Order.user_id == user_id)
            
            order = query.first()
            
            if not order:
                return {'error': 'Order not found'}
            
            return {
                'order': order.to_dict()
            }
            
        except Exception as e:
            logging.error(f"Error getting order details: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def cancel_order(order_id, user_id):
        """
        Cancel an order (if eligible)
        
        Args:
            order_id: Order ID
            user_id: User ID for ownership validation
            
        Returns:
            dict: Cancellation result
        """
        session = Session()
        
        try:
            order = session.query(Order).filter(
                Order.id == order_id,
                Order.user_id == user_id
            ).first()
            
            if not order:
                return {'error': 'Order not found'}
            
            if not order.can_be_cancelled():
                return {'error': 'Order cannot be cancelled at this stage'}
            
            # Restore stock for all items
            for item in order.items:
                book = session.query(Book).filter(Book.id == item.book_id).first()
                if book:
                    book.increase_stock(item.quantity)
            
            # Update order status
            order.status = OrderStatus.CANCELLED.value
            order.payment_status = PaymentStatus.CANCELLED.value
            
            session.commit()
            
            return {
                'success': True,
                'message': 'Order cancelled successfully'
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error cancelling order: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def update_order_status(order_id, status, tracking_number=None):
        """
        Update order status (admin function)
        
        Args:
            order_id: Order ID
            status: New status
            tracking_number: Optional tracking number
            
        Returns:
            dict: Update result
        """
        session = Session()
        
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            
            if not order:
                return {'error': 'Order not found'}
            
            order.status = status
            
            if tracking_number:
                order.tracking_number = tracking_number
            
            # Set shipped/delivered timestamps
            if status == OrderStatus.SHIPPED.value:
                from datetime import datetime
                order.shipped_at = datetime.utcnow()
            elif status == OrderStatus.DELIVERED.value:
                from datetime import datetime
                order.delivered_at = datetime.utcnow()
            
            session.commit()
            
            return {
                'success': True,
                'order': order.to_dict()
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error updating order status: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def _calculate_tax(subtotal, tax_rate=0.08):
        """Calculate tax amount"""
        return Decimal(str(subtotal)) * Decimal(str(tax_rate))
    
    @staticmethod
    def _calculate_shipping(cart, base_shipping=5.99, free_shipping_threshold=50.00):
        """Calculate shipping cost"""
        subtotal = cart.get_total_amount()
        
        if subtotal >= free_shipping_threshold:
            return Decimal('0.00')
        
        return Decimal(str(base_shipping))