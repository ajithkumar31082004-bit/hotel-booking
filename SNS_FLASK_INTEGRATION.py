"""
Flask API Integration Examples for SNS Notifications

This file shows how to integrate SNS notifications into Flask API endpoints.
Copy these patterns into your app.py file.
"""

from datetime import datetime
from flask import request, jsonify
from sns_notifications import sns_manager

# ============================================================================
# BOOKING ENDPOINTS WITH SNS
# ============================================================================

def create_booking_with_sns():
    """
    Example: Create booking and send SNS confirmation
    
    Add to your Flask app:
    @app.route('/api/booking/create', methods=['POST'])
    def create_booking():
        ... existing booking creation logic ...
        
        # After successful booking creation:
        booking = {
            'booking_id': result['booking_id'],
            'guest_name': data['guest_name'],
            'guest_email': data['guest_email'],
            'guest_phone': data.get('guest_phone', ''),
            'room_type': room_data['room_type'],
            'room_number': room_data.get('room_number', 'TBD'),
            'check_in': data['check_in'],
            'check_out': data['check_out'],
            'num_nights': nights,
            'guest_count': data['guest_count'],
            'total_price': total_price,
            'status': 'confirmed',
            'special_requests': data.get('special_requests', '')
        }
        
        # Send SNS notification
        if sns_manager:
            sns_manager.publish_booking_confirmation(booking)
        
        return {'success': True, 'booking_id': result['booking_id']}
    """
    pass

def process_payment_with_sns():
    """
    Example: Process payment and send SNS receipt
    
    Add to your Flask app:
    @app.route('/api/booking/process-payment', methods=['POST'])
    def process_payment():
        ... existing payment processing logic ...
        
        # After successful payment:
        transaction = {
            'transaction_id': payment_result['transaction_id'],
            'amount': payment_data['amount'],
            'currency': 'USD',
            'payment_method': payment_data['payment_method'],
            'card_type': payment_result.get('card_type', 'Unknown'),
            'card_last_four': payment_result.get('card_last_four', '****'),
            'receipt_number': payment_result.get('receipt_number', ''),
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        # Send SNS notification
        if sns_manager:
            sns_manager.publish_payment_confirmation(transaction, booking_id)
        
        return {'success': True, 'transaction': transaction}
    """
    pass

# ============================================================================
# REMINDER SCHEDULER ENDPOINTS
# ============================================================================

def schedule_booking_reminders():
    """
    Example: Scheduled task to send booking reminders
    
    Add to your Flask app:
    from apscheduler.schedulers.background import BackgroundScheduler
    
    @app.route('/api/admin/send-reminders', methods=['POST'])
    def send_reminders():
        # Get bookings with check-in in 7 days
        target_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        bookings = get_bookings_for_date(target_date)  # Your DB query
        
        count = 0
        for booking in bookings:
            if sns_manager:
                sns_manager.publish_booking_reminder(booking, days_until=7)
                count += 1
        
        return {
            'success': True,
            'reminders_sent': count,
            'target_date': target_date
        }
    
    # Or schedule automatically every day at 8 AM:
    scheduler = BackgroundScheduler()
    
    def scheduled_reminders():
        send_reminders()
    
    scheduler.add_job(scheduled_reminders, 'cron', hour=8, minute=0)
    scheduler.start()
    """
    pass

# ============================================================================
# REVIEW ENDPOINTS WITH SNS
# ============================================================================

def create_review_with_sns():
    """
    Example: Create review and send SNS notification
    
    Add to your Flask app:
    @app.route('/api/reviews/create', methods=['POST'])
    def create_review():
        ... existing review creation logic ...
        
        # After successful review creation:
        review = {
            'review_id': result['review_id'],
            'booking_id': data['booking_id'],
            'guest_name': booking_data['guest_name'],
            'overall_rating': data['overall_rating'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'categories': {
                'cleanliness': data.get('cleanliness_rating'),
                'comfort': data.get('comfort_rating'),
                'location': data.get('location_rating'),
                'service': data.get('service_rating'),
                'value_for_money': data.get('value_for_money_rating')
            },
            'comment': data.get('comment', '')
        }
        
        # Send SNS notification
        if sns_manager:
            sns_manager.publish_review_notification(review)
        
        return {'success': True, 'review_id': result['review_id']}
    """
    pass

# ============================================================================
# SYSTEM ALERT ENDPOINTS
# ============================================================================

def trigger_high_booking_alert():
    """
    Example: Send alert when booking volume is high
    
    Add to your Flask app:
    @app.route('/api/admin/check-booking-status', methods=['GET'])
    def check_booking_status():
        # Get bookings in last hour
        recent_count = get_bookings_in_last_hour()
        
        # Alert if high volume
        if recent_count > 50:
            if sns_manager:
                sns_manager.publish_alert(
                    alert_type='High Booking Volume',
                    message=f'{recent_count} bookings received in the last hour. '
                            f'Consider scaling up infrastructure.',
                    severity='WARNING'
                )
        
        return {
            'status': 'ok',
            'bookings_last_hour': recent_count,
            'alert_sent': recent_count > 50
        }
    """
    pass

def trigger_payment_alert():
    """
    Example: Send alert when payment fails
    
    Add to your Flask app:
    def process_payment():
        try:
            ... payment processing ...
        except Exception as e:
            # Send alert on payment failure
            if sns_manager:
                sns_manager.publish_alert(
                    alert_type='Payment Failure',
                    message=f'Payment processing failed: {str(e)}',
                    severity='ERROR'
                )
            return {'error': 'Payment failed'}, 500
    """
    pass

def trigger_database_alert():
    """
    Example: Send alert when database operation fails
    
    Add to your Flask app:
    def save_to_database(data):
        try:
            ... database operation ...
        except Exception as e:
            if sns_manager:
                sns_manager.publish_alert(
                    alert_type='Database Error',
                    message=f'Database operation failed: {str(e)}',
                    severity='CRITICAL'
                )
            raise
    """
    pass

# ============================================================================
# SUBSCRIPTION MANAGEMENT ENDPOINTS
# ============================================================================

def manage_email_subscription():
    """
    Example: Email subscription management
    
    Add to your Flask app:
    @app.route('/api/subscribe/email', methods=['POST'])
    def subscribe_email():
        data = request.json
        email = data.get('email')
        topic = data.get('topic', 'booking-confirmations')
        
        if sns_manager:
            result = sns_manager.subscribe_email(topic, email)
            return {
                'success': result,
                'message': 'Subscription requested. Check email for confirmation.'
            }
        
        return {'success': False, 'error': 'SNS not available'}
    """
    pass

def manage_sms_subscription():
    """
    Example: SMS subscription management
    
    Add to your Flask app:
    @app.route('/api/subscribe/sms', methods=['POST'])
    def subscribe_sms():
        data = request.json
        phone = data.get('phone')  # Must be E.164 format: +1-555-0123456
        topic = data.get('topic', 'booking-confirmations')
        
        # Validate phone format
        if not phone.startswith('+'):
            return {'success': False, 'error': 'Phone must be in E.164 format'}
        
        if sns_manager:
            result = sns_manager.subscribe_sms(topic, phone)
            return {
                'success': result,
                'message': 'SMS subscription activated'
            }
        
        return {'success': False, 'error': 'SNS not available'}
    """
    pass

def unsubscribe():
    """
    Example: Unsubscribe from notifications
    
    Add to your Flask app:
    @app.route('/api/unsubscribe', methods=['POST'])
    def unsubscribe():
        data = request.json
        subscription_arn = data.get('subscription_arn')
        
        if sns_manager:
            result = sns_manager.unsubscribe(subscription_arn)
            return {
                'success': result,
                'message': 'Unsubscribed successfully'
            }
        
        return {'success': False, 'error': 'SNS not available'}
    """
    pass

# ============================================================================
# MONITORING & ADMIN ENDPOINTS
# ============================================================================

def get_topic_subscribers():
    """
    Example: Get subscribers for a topic
    
    Add to your Flask app:
    @app.route('/api/admin/subscribers/<topic>', methods=['GET'])
    def get_subscribers(topic):
        if not sns_manager:
            return {'error': 'SNS not available'}, 500
        
        subs = sns_manager.get_topic_subscriptions(topic)
        
        return {
            'topic': topic,
            'subscriber_count': len(subs),
            'subscribers': [{
                'endpoint': sub['Endpoint'],
                'protocol': sub['Protocol'],
                'status': sub['SubscriptionArn']
            } for sub in subs]
        }
    """
    pass

def get_topic_stats():
    """
    Example: Get topic statistics
    
    Add to your Flask app:
    @app.route('/api/admin/sns-stats', methods=['GET'])
    def get_sns_stats():
        if not sns_manager:
            return {'error': 'SNS not available'}, 500
        
        topics = {}
        for topic_name in ['booking-confirmations', 'payment-confirmations',
                          'booking-reminders', 'reviews-notifications', 'alerts']:
            subs = sns_manager.get_topic_subscriptions(topic_name)
            attrs = sns_manager.get_topic_attributes(topic_name)
            
            topics[topic_name] = {
                'subscriber_count': len(subs),
                'messages_published': attrs.get('MessageCount', '0'),
                'created_timestamp': attrs.get('CreateTimestamp', 'Unknown')
            }
        
        return {
            'sns_enabled': True,
            'topics': topics
        }
    """
    pass

# ============================================================================
# COMPLETE INTEGRATION EXAMPLE
# ============================================================================

complete_integration_example = """
# In your app.py, add these imports at the top:
from datetime import datetime, timedelta
from sns_notifications import initialize_sns

# Initialize SNS in your Flask app startup
app = Flask(__name__)

@app.before_request
def initialize_services():
    global sns_manager
    if not sns_manager:
        sns_manager = initialize_sns()

# Then add these endpoints to your app:

@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    '''Create booking with SNS notification'''
    data = request.json
    
    try:
        # ... existing booking creation logic ...
        
        # Build booking object
        booking = {
            'booking_id': f"BK{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'guest_name': data['guest_name'],
            'guest_email': data['guest_email'],
            'guest_phone': data.get('guest_phone', ''),
            'room_type': data['room_type'],
            'room_number': data.get('room_number', 'TBD'),
            'check_in': data['check_in'],
            'check_out': data['check_out'],
            'num_nights': calculate_nights(data['check_in'], data['check_out']),
            'guest_count': data['guest_count'],
            'total_price': data['total_price'],
            'status': 'confirmed',
            'special_requests': data.get('special_requests', '')
        }
        
        # Send SNS notification
        if sns_manager:
            try:
                sns_manager.publish_booking_confirmation(booking)
            except Exception as e:
                print(f"Warning: SNS notification failed: {e}")
                # Don't fail the booking if SNS fails
        
        return {
            'success': True,
            'booking_id': booking['booking_id'],
            'message': 'Booking confirmed. Check email for details.'
        }
    
    except Exception as e:
        # Send alert on error
        if sns_manager:
            try:
                sns_manager.publish_alert(
                    alert_type='Booking Error',
                    message=f'Failed to create booking: {str(e)}',
                    severity='ERROR'
                )
            except:
                pass
        
        return {'error': str(e)}, 500


@app.route('/api/booking/process-payment', methods=['POST'])
def process_payment():
    '''Process payment with SNS receipt'''
    data = request.json
    booking_id = data.get('booking_id')
    
    try:
        # ... existing payment processing ...
        
        transaction = {
            'transaction_id': f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'amount': data['amount'],
            'currency': 'USD',
            'payment_method': data['payment_method'],
            'card_type': 'Visa',  # From payment processor
            'card_last_four': data['card_last_four'],
            'receipt_number': f"RCP-{datetime.now().strftime('%Y%m%d')}-ABC123",
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
        
        # Send SNS notification
        if sns_manager:
            try:
                sns_manager.publish_payment_confirmation(transaction, booking_id)
            except Exception as e:
                print(f"Warning: SNS notification failed: {e}")
        
        return {
            'success': True,
            'transaction': transaction,
            'message': 'Payment processed. Receipt sent to email.'
        }
    
    except Exception as e:
        if sns_manager:
            try:
                sns_manager.publish_alert(
                    alert_type='Payment Error',
                    message=f'Payment failed: {str(e)}',
                    severity='ERROR'
                )
            except:
                pass
        
        return {'error': str(e)}, 500


@app.route('/api/admin/send-reminders', methods=['POST'])
def send_reminders():
    '''Send booking reminders for upcoming check-ins'''
    if not sns_manager:
        return {'error': 'SNS not available'}, 500
    
    target_date = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    bookings = get_bookings_by_checkin_date(target_date)  # Your DB query
    
    count = 0
    for booking in bookings:
        try:
            sns_manager.publish_booking_reminder(booking, days_until=7)
            count += 1
        except Exception as e:
            print(f"Failed to send reminder for {booking['booking_id']}: {e}")
    
    return {
        'success': True,
        'reminders_sent': count,
        'target_date': target_date
    }


@app.route('/api/reviews/create', methods=['POST'])
def create_review():
    '''Create review with SNS notification'''
    data = request.json
    
    try:
        review = {
            'review_id': f"REV{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'booking_id': data['booking_id'],
            'guest_name': data.get('guest_name', 'Guest'),
            'overall_rating': data['overall_rating'],
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
            'categories': {
                'cleanliness': data.get('cleanliness', 5),
                'comfort': data.get('comfort', 5),
                'location': data.get('location', 5),
                'service': data.get('service', 5),
                'value_for_money': data.get('value_for_money', 5)
            },
            'comment': data.get('comment', '')
        }
        
        # Send SNS notification
        if sns_manager:
            try:
                sns_manager.publish_review_notification(review)
            except Exception as e:
                print(f"Warning: SNS notification failed: {e}")
        
        return {
            'success': True,
            'review_id': review['review_id'],
            'message': 'Thank you for your review!'
        }
    
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/api/admin/sns-status', methods=['GET'])
def sns_status():
    '''Check SNS availability and stats'''
    if not sns_manager:
        return {'status': 'unavailable'}, 500
    
    stats = {}
    for topic in ['booking-confirmations', 'payment-confirmations',
                  'booking-reminders', 'reviews-notifications', 'alerts']:
        try:
            subs = sns_manager.get_topic_subscriptions(topic)
            stats[topic] = {'subscribers': len(subs)}
        except:
            stats[topic] = {'subscribers': 0, 'error': 'Unable to fetch'}
    
    return {
        'sns_enabled': True,
        'topics': stats
    }
"""

if __name__ == "__main__":
    print("SNS Flask Integration Examples")
    print(complete_integration_example)
