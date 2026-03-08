"""
AWS SNS Integration for Hotel Booking System
Handles SMS, Email, and Push notifications via AWS SNS
"""

import boto3
import json
import os
from typing import Dict, List, Any
from datetime import datetime


class SNSNotificationManager:
    """Manages all SNS notifications (SMS, Email, Push)"""
    
    def __init__(self, region: str = None):
        self.region = region or os.getenv('AWS_REGION', 'us-east-1')
        self.sns_client = boto3.client('sns', region_name=self.region)
        self.topics = {}
        self._initialize_topics()
    
    def _initialize_topics(self):
        """Initialize SNS topics for different notification types"""
        topic_names = [
            'booking-confirmations',
            'payment-confirmations',
            'booking-reminders',
            'reviews-notifications',
            'alerts'
        ]
        
        for topic_name in topic_names:
            try:
                response = self.sns_client.create_topic(Name=topic_name)
                self.topics[topic_name] = response['TopicArn']
                print(f"[OK] SNS Topic initialized: {topic_name}")
            except Exception as e:
                print(f"[WARNING] Could not create SNS topic {topic_name}: {e}")
    
    def subscribe_email(self, topic_name: str, email: str) -> bool:
        """Subscribe email address to SNS topic"""
        try:
            if topic_name not in self.topics:
                return False
            
            response = self.sns_client.subscribe(
                TopicArn=self.topics[topic_name],
                Protocol='email',
                Endpoint=email
            )
            print(f"✓ Email {email} subscribed to {topic_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to subscribe email: {e}")
            return False
    
    def subscribe_sms(self, topic_name: str, phone_number: str) -> bool:
        """Subscribe phone number to SNS topic for SMS"""
        try:
            if topic_name not in self.topics:
                return False
            
            response = self.sns_client.subscribe(
                TopicArn=self.topics[topic_name],
                Protocol='sms',
                Endpoint=phone_number
            )
            print(f"✓ Phone {phone_number} subscribed to {topic_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to subscribe SMS: {e}")
            return False
    
    def subscribe_sqs(self, topic_name: str, queue_arn: str) -> bool:
        """Subscribe SQS queue to SNS topic"""
        try:
            if topic_name not in self.topics:
                return False
            
            response = self.sns_client.subscribe(
                TopicArn=self.topics[topic_name],
                Protocol='sqs',
                Endpoint=queue_arn
            )
            print(f"✓ SQS queue subscribed to {topic_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to subscribe SQS: {e}")
            return False
    
    def publish_booking_confirmation(self, booking: Dict[str, Any]) -> bool:
        """Publish booking confirmation notification"""
        try:
            subject = f"Booking Confirmation - {booking['booking_id']}"
            
            message = f"""
Dear {booking['guest_name']},

Your booking has been confirmed!

Booking Details:
- Confirmation Number: {booking['booking_id']}
- Room Type: {booking['room_type']}
- Room Number: {booking['room_number']}
- Check-in: {booking['check_in']}
- Check-out: {booking['check_out']}
- Number of Nights: {booking['num_nights']}
- Guest Count: {booking['guest_count']}
- Total Price: ${booking['total_price']:.2f}
- Status: {booking['status'].upper()}

Special Requests: {booking.get('special_requests', 'None')}

A confirmation email has also been sent to: {booking['guest_email']}
Phone: {booking['guest_phone']}

Thank you for choosing our hotel!

Best regards,
Hotel Booking System
"""
            
            # Publish to SNS topic
            response = self.sns_client.publish(
                TopicArn=self.topics['booking-confirmations'],
                Subject=subject,
                Message=message,
                MessageAttributes={
                    'booking_id': {'DataType': 'String', 'StringValue': booking['booking_id']},
                    'guest_email': {'DataType': 'String', 'StringValue': booking['guest_email']},
                    'guest_phone': {'DataType': 'String', 'StringValue': booking['guest_phone']},
                    'notification_type': {'DataType': 'String', 'StringValue': 'booking_confirmation'}
                }
            )
            
            print(f"✓ Booking confirmation published: {booking['booking_id']}")
            return True
        except Exception as e:
            print(f"✗ Failed to publish booking confirmation: {e}")
            return False
    
    def publish_payment_confirmation(self, transaction: Dict[str, Any], booking_id: str) -> bool:
        """Publish payment confirmation notification"""
        try:
            subject = f"Payment Confirmation - Order {transaction['transaction_id']}"
            
            message = f"""
Dear Valued Guest,

Your payment has been successfully processed!

Payment Details:
- Transaction ID: {transaction['transaction_id']}
- Booking ID: {booking_id}
- Amount: ${transaction['amount']:.2f}
- Currency: {transaction['currency']}
- Payment Method: {transaction['payment_method'].replace('_', ' ').title()}
- Card: {transaction['card_type']} ending in {transaction['card_last_four']}
- Receipt Number: {transaction['receipt_number']}
- Timestamp: {transaction['timestamp']}
- Status: {transaction['status'].upper()}

A receipt has been sent to the email address associated with your account.

For questions or to modify your booking, please contact our support team.

Thank you!

Hotel Booking System
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topics['payment-confirmations'],
                Subject=subject,
                Message=message,
                MessageAttributes={
                    'transaction_id': {'DataType': 'String', 'StringValue': transaction['transaction_id']},
                    'booking_id': {'DataType': 'String', 'StringValue': booking_id},
                    'amount': {'DataType': 'Number', 'StringValue': str(transaction['amount'])},
                    'notification_type': {'DataType': 'String', 'StringValue': 'payment_confirmation'}
                }
            )
            
            print(f"✓ Payment confirmation published: {transaction['transaction_id']}")
            return True
        except Exception as e:
            print(f"✗ Failed to publish payment confirmation: {e}")
            return False
    
    def publish_booking_reminder(self, booking: Dict[str, Any], days_until: int) -> bool:
        """Publish pre-arrival booking reminder"""
        try:
            subject = f"Reminder: Your stay at our hotel in {days_until} days"
            
            message = f"""
Dear {booking['guest_name']},

This is a friendly reminder about your upcoming stay!

Booking Reminder:
- Confirmation Number: {booking['booking_id']}
- Room Type: {booking['room_type']}
- Check-in Date: {booking['check_in']}
- Check-in Time: 3:00 PM (or later)
- Check-out Time: 11:00 AM
- Number of Nights: {booking['num_nights']}

Preparation Checklist:
☐ Review special requests (if any)
☐ Pack necessary items
☐ Arrange transportation to the hotel
☐ Review cancellation policy

Check-in Information:
- Front Desk Hours: 24/7
- Early Check-in: Available upon request (subject to availability)
- Late Check-in: Notify us in advance
- Contact: +1-800-HOTEL-99

Questions? Contact our team:
- Email: support@hotel.com
- Phone: +1-800-HOTEL-99
- Website: https://www.hotel.com

We look forward to welcoming you!

Best regards,
Hotel Booking System
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topics['booking-reminders'],
                Subject=subject,
                Message=message,
                MessageAttributes={
                    'booking_id': {'DataType': 'String', 'StringValue': booking['booking_id']},
                    'guest_email': {'DataType': 'String', 'StringValue': booking['guest_email']},
                    'days_until': {'DataType': 'Number', 'StringValue': str(days_until)},
                    'notification_type': {'DataType': 'String', 'StringValue': 'booking_reminder'}
                }
            )
            
            print(f"✓ Booking reminder published: {booking['booking_id']}")
            return True
        except Exception as e:
            print(f"✗ Failed to publish booking reminder: {e}")
            return False
    
    def publish_review_notification(self, review: Dict[str, Any]) -> bool:
        """Publish review submission notification"""
        try:
            subject = f"Thank you for your review!"
            
            message = f"""
Dear {review['guest_name']},

Thank you for taking the time to share your feedback about your stay!

Review Details:
- Booking ID: {review['booking_id']}
- Overall Rating: {review['overall_rating']} / 5 stars
- Status: {review['status'].upper()}
- Submitted: {review['created_at']}

Your feedback helps us:
✓ Improve our services
✓ Train our staff
✓ Maintain high standards
✓ Serve future guests better

Category Ratings:
- Cleanliness: {review['categories'].get('cleanliness', 'N/A')} / 5
- Comfort: {review['categories'].get('comfort', 'N/A')} / 5
- Location: {review['categories'].get('location', 'N/A')} / 5
- Service: {review['categories'].get('service', 'N/A')} / 5
- Value for Money: {review['categories'].get('value_for_money', 'N/A')} / 5

Your review: {review['comment'][:200]}...

Your feedback is valuable to us. Thank you again!

Best regards,
Hotel Management
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topics['reviews-notifications'],
                Subject=subject,
                Message=message,
                MessageAttributes={
                    'review_id': {'DataType': 'String', 'StringValue': str(review['review_id'])},
                    'booking_id': {'DataType': 'String', 'StringValue': review['booking_id']},
                    'rating': {'DataType': 'Number', 'StringValue': str(review['overall_rating'])},
                    'notification_type': {'DataType': 'String', 'StringValue': 'review_notification'}
                }
            )
            
            print(f"✓ Review notification published: {review['review_id']}")
            return True
        except Exception as e:
            print(f"✗ Failed to publish review notification: {e}")
            return False
    
    def publish_alert(self, alert_type: str, message: str, severity: str = 'INFO') -> bool:
        """Publish system alert"""
        try:
            subject = f"[{severity}] Alert: {alert_type}"
            
            full_message = f"""
Alert Type: {alert_type}
Severity: {severity}
Timestamp: {datetime.now().isoformat()}

Message:
{message}

---
Hotel Booking System Alerts
"""
            
            response = self.sns_client.publish(
                TopicArn=self.topics['alerts'],
                Subject=subject,
                Message=full_message,
                MessageAttributes={
                    'alert_type': {'DataType': 'String', 'StringValue': alert_type},
                    'severity': {'DataType': 'String', 'StringValue': severity},
                    'notification_type': {'DataType': 'String', 'StringValue': 'system_alert'}
                }
            )
            
            print(f"✓ Alert published: {alert_type} ({severity})")
            return True
        except Exception as e:
            print(f"✗ Failed to publish alert: {e}")
            return False
    
    def publish_bulk_message(self, topic_name: str, subject: str, message: str, 
                            message_attributes: Dict = None) -> bool:
        """Publish custom message to topic"""
        try:
            if topic_name not in self.topics:
                return False
            
            response = self.sns_client.publish(
                TopicArn=self.topics[topic_name],
                Subject=subject,
                Message=message,
                MessageAttributes=message_attributes or {}
            )
            
            print(f"✓ Message published to {topic_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to publish message: {e}")
            return False
    
    def get_topic_subscriptions(self, topic_name: str) -> List[Dict]:
        """Get all subscriptions for a topic"""
        try:
            if topic_name not in self.topics:
                return []
            
            response = self.sns_client.list_subscriptions_by_topic(
                TopicArn=self.topics[topic_name]
            )
            
            return response.get('Subscriptions', [])
        except Exception as e:
            print(f"✗ Failed to get subscriptions: {e}")
            return []
    
    def unsubscribe(self, subscription_arn: str) -> bool:
        """Unsubscribe from a topic"""
        try:
            self.sns_client.unsubscribe(SubscriptionArn=subscription_arn)
            print(f"✓ Unsubscribed: {subscription_arn}")
            return True
        except Exception as e:
            print(f"✗ Failed to unsubscribe: {e}")
            return False
    
    def get_topic_attributes(self, topic_name: str) -> Dict:
        """Get topic attributes"""
        try:
            if topic_name not in self.topics:
                return {}
            
            response = self.sns_client.get_topic_attributes(
                TopicArn=self.topics[topic_name]
            )
            
            return response.get('Attributes', {})
        except Exception as e:
            print(f"✗ Failed to get topic attributes: {e}")
            return {}


# Initialize global SNS manager (similar to other notification systems)
sns_manager = None

def initialize_sns():
    """Initialize SNS notification manager"""
    global sns_manager
    try:
        sns_manager = SNSNotificationManager()
        print("[OK] SNS Notification Manager initialized")
        return sns_manager
    except Exception as e:
        print(f"[WARNING] SNS initialization failed: {e}")
        return None


if __name__ == "__main__":
    # Test SNS integration
    print("Testing SNS Notification Manager...\n")
    
    manager = SNSNotificationManager()
    
    # Test booking confirmation
    test_booking = {
        'booking_id': 'BK1001',
        'guest_name': 'John Doe',
        'guest_email': 'john@example.com',
        'guest_phone': '+1-555-0123',
        'room_type': 'Deluxe',
        'room_number': 'D101',
        'check_in': '2024-03-15',
        'check_out': '2024-03-18',
        'num_nights': 3,
        'guest_count': 2,
        'total_price': 360.00,
        'status': 'confirmed',
        'special_requests': 'High floor preferred'
    }
    
    manager.publish_booking_confirmation(test_booking)
    
    # Test payment confirmation
    test_transaction = {
        'transaction_id': 'TXN5001',
        'amount': 360.00,
        'currency': 'USD',
        'payment_method': 'credit_card',
        'card_type': 'Visa',
        'card_last_four': '4242',
        'receipt_number': 'RCP-20260308-ABC123',
        'timestamp': datetime.now().isoformat(),
        'status': 'completed'
    }
    
    manager.publish_payment_confirmation(test_transaction, test_booking['booking_id'])
    
    # Test reminder
    manager.publish_booking_reminder(test_booking, 7)
    
    print("\n✓ SNS integration test complete!")
