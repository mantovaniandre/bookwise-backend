import stripe
from configuration.secret_key import Config
from model.payment_method import PaymentMethod
from model.order import Order, OrderStatus, PaymentStatus
from configuration.database import Session
import logging

# Configure Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

class PaymentService:
    
    @staticmethod
    def create_payment_intent(amount, currency='usd', metadata=None):
        """
        Create a Stripe Payment Intent
        
        Args:
            amount: Amount in cents (e.g., $10.00 = 1000)
            currency: Currency code (default: 'usd')
            metadata: Additional metadata for the payment
            
        Returns:
            dict: Payment intent data
        """
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency,
                metadata=metadata or {},
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            return {
                'client_secret': intent.client_secret,
                'payment_intent_id': intent.id,
                'amount': intent.amount,
                'status': intent.status
            }
            
        except stripe.error.StripeError as e:
            logging.error(f"Stripe error: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def confirm_payment(payment_intent_id, payment_method_id=None):
        """
        Confirm a payment intent
        
        Args:
            payment_intent_id: Stripe payment intent ID
            payment_method_id: Optional payment method ID
            
        Returns:
            dict: Payment confirmation result
        """
        try:
            confirm_params = {}
            if payment_method_id:
                confirm_params['payment_method'] = payment_method_id
                
            intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                **confirm_params
            )
            
            return {
                'status': intent.status,
                'payment_intent_id': intent.id,
                'amount_received': intent.amount_received,
                'charges': intent.charges.data if intent.charges else []
            }
            
        except stripe.error.StripeError as e:
            logging.error(f"Payment confirmation error: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def create_customer(email, name=None, metadata=None):
        """
        Create a Stripe customer
        
        Args:
            email: Customer email
            name: Customer name
            metadata: Additional metadata
            
        Returns:
            dict: Customer data
        """
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name,
                metadata=metadata or {}
            )
            
            return {
                'customer_id': customer.id,
                'email': customer.email,
                'created': customer.created
            }
            
        except stripe.error.StripeError as e:
            logging.error(f"Customer creation error: {e}")
            return {'error': str(e)}
    
    @staticmethod
    def save_payment_method(user_id, payment_method_id, set_as_default=False):
        """
        Save a tokenized payment method for a user
        
        Args:
            user_id: User ID
            payment_method_id: Stripe payment method ID
            set_as_default: Whether to set as default payment method
            
        Returns:
            PaymentMethod: Saved payment method object
        """
        session = Session()
        
        try:
            # Retrieve payment method details from Stripe
            payment_method = stripe.PaymentMethod.retrieve(payment_method_id)
            
            # Extract card details for display
            card_data = payment_method.card if payment_method.type == 'card' else {}
            
            # Create payment method record
            db_payment_method = PaymentMethod(
                user_id=user_id,
                stripe_payment_method_id=payment_method_id,
                payment_type=payment_method.type,
                last_four=card_data.get('last4'),
                brand=card_data.get('brand'),
                exp_month=card_data.get('exp_month'),
                exp_year=card_data.get('exp_year'),
                is_default=set_as_default
            )
            
            # If setting as default, unset other defaults
            if set_as_default:
                session.query(PaymentMethod).filter(
                    PaymentMethod.user_id == user_id,
                    PaymentMethod.is_default == True
                ).update({'is_default': False})
            
            session.add(db_payment_method)
            session.commit()
            
            return db_payment_method
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error saving payment method: {e}")
            raise e
        finally:
            session.close()
    
    @staticmethod
    def process_order_payment(order_id, payment_method_id=None):
        """
        Process payment for an order
        
        Args:
            order_id: Order ID to process payment for
            payment_method_id: Optional specific payment method
            
        Returns:
            dict: Payment processing result
        """
        session = Session()
        
        try:
            order = session.query(Order).filter(Order.id == order_id).first()
            if not order:
                return {'error': 'Order not found'}
            
            # Create payment intent
            payment_result = PaymentService.create_payment_intent(
                amount=order.total_amount,
                metadata={
                    'order_id': order_id,
                    'user_id': order.user_id
                }
            )
            
            if 'error' in payment_result:
                return payment_result
            
            # Update order with payment intent
            order.stripe_payment_intent_id = payment_result['payment_intent_id']
            order.payment_status = PaymentStatus.PROCESSING.value
            
            session.commit()
            
            return {
                'client_secret': payment_result['client_secret'],
                'payment_intent_id': payment_result['payment_intent_id'],
                'order_id': order_id,
                'amount': float(order.total_amount)
            }
            
        except Exception as e:
            session.rollback()
            logging.error(f"Error processing order payment: {e}")
            return {'error': str(e)}
        finally:
            session.close()
    
    @staticmethod
    def handle_payment_webhook(payload, sig_header):
        """
        Handle Stripe webhook events
        
        Args:
            payload: Webhook payload
            sig_header: Webhook signature header
            
        Returns:
            dict: Webhook processing result
        """
        endpoint_secret = Config.STRIPE_WEBHOOK_SECRET
        
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return {'error': 'Invalid payload'}
        except stripe.error.SignatureVerificationError:
            return {'error': 'Invalid signature'}
        
        # Handle payment intent events
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            PaymentService._handle_payment_success(payment_intent)
            
        elif event['type'] == 'payment_intent.payment_failed':
            payment_intent = event['data']['object']
            PaymentService._handle_payment_failure(payment_intent)
        
        return {'status': 'success'}
    
    @staticmethod
    def _handle_payment_success(payment_intent):
        """Handle successful payment"""
        session = Session()
        
        try:
            order_id = payment_intent['metadata'].get('order_id')
            if order_id:
                order = session.query(Order).filter(Order.id == order_id).first()
                if order:
                    order.payment_status = PaymentStatus.SUCCEEDED.value
                    order.status = OrderStatus.CONFIRMED.value
                    session.commit()
                    
                    # Here you could trigger email notifications, inventory updates, etc.
                    logging.info(f"Payment succeeded for order {order_id}")
                    
        except Exception as e:
            session.rollback()
            logging.error(f"Error handling payment success: {e}")
        finally:
            session.close()
    
    @staticmethod
    def _handle_payment_failure(payment_intent):
        """Handle failed payment"""
        session = Session()
        
        try:
            order_id = payment_intent['metadata'].get('order_id')
            if order_id:
                order = session.query(Order).filter(Order.id == order_id).first()
                if order:
                    order.payment_status = PaymentStatus.FAILED.value
                    session.commit()
                    
                    logging.warning(f"Payment failed for order {order_id}")
                    
        except Exception as e:
            session.rollback()
            logging.error(f"Error handling payment failure: {e}")
        finally:
            session.close()