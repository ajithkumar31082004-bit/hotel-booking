"""
SNS Integration Test Script
Tests AWS SNS notifications with sample data
"""

import os
import sys
from datetime import datetime
from sns_notifications import SNSNotificationManager

def print_header(text):
    """Print formatted header"""
    print(f"\n{'='*50}")
    print(f"  {text}")
    print(f"{'='*50}\n")

def test_sns_initialization():
    """Test SNS manager initialization"""
    print_header("TEST 1: SNS Manager Initialization")
    
    try:
        manager = SNSNotificationManager()
        print("✓ SNS Manager initialized successfully")
        print(f"✓ Region: {manager.region}")
        print(f"✓ Topics initialized: {len(manager.topics)}")
        
        for topic_name, topic_arn in manager.topics.items():
            print(f"  - {topic_name}: {topic_arn}")
        
        return manager
    except Exception as e:
        print(f"✗ Failed to initialize SNS: {e}")
        return None

def test_booking_confirmation(manager):
    """Test booking confirmation notification"""
    print_header("TEST 2: Booking Confirmation")
    
    booking = {
        'booking_id': 'TEST-BK-001',
        'guest_name': 'Test Guest',
        'guest_email': 'test@example.com',
        'guest_phone': '+1-555-0100',
        'room_type': 'Deluxe Suite',
        'room_number': 'D-101',
        'check_in': '2024-03-20',
        'check_out': '2024-03-22',
        'num_nights': 2,
        'guest_count': 2,
        'total_price': 240.00,
        'status': 'confirmed',
        'special_requests': 'High floor, near elevator'
    }
    
    try:
        result = manager.publish_booking_confirmation(booking)
        print("✓ Booking confirmation published successfully")
        print(f"  Booking ID: {booking['booking_id']}")
        print(f"  Guest: {booking['guest_name']}")
        print(f"  Check-in: {booking['check_in']}")
        print(f"  Total: ${booking['total_price']:.2f}")
        return True
    except Exception as e:
        print(f"✗ Failed to publish booking confirmation: {e}")
        return False

def test_payment_confirmation(manager):
    """Test payment confirmation notification"""
    print_header("TEST 3: Payment Confirmation")
    
    transaction = {
        'transaction_id': 'TEST-TXN-001',
        'amount': 240.00,
        'currency': 'USD',
        'payment_method': 'credit_card',
        'card_type': 'Visa',
        'card_last_four': '4242',
        'receipt_number': f'RCP-{datetime.now().strftime("%Y%m%d")}-TEST',
        'timestamp': datetime.now().isoformat(),
        'status': 'completed'
    }
    
    try:
        result = manager.publish_payment_confirmation(transaction, 'TEST-BK-001')
        print("✓ Payment confirmation published successfully")
        print(f"  Transaction ID: {transaction['transaction_id']}")
        print(f"  Amount: ${transaction['amount']:.2f}")
        print(f"  Receipt: {transaction['receipt_number']}")
        print(f"  Status: {transaction['status'].upper()}")
        return True
    except Exception as e:
        print(f"✗ Failed to publish payment confirmation: {e}")
        return False

def test_booking_reminder(manager):
    """Test booking reminder notification"""
    print_header("TEST 4: Booking Reminder (7 days before)")
    
    booking = {
        'booking_id': 'TEST-BK-001',
        'guest_name': 'Test Guest',
        'guest_email': 'test@example.com',
        'guest_phone': '+1-555-0100',
        'room_type': 'Deluxe Suite',
        'room_number': 'D-101',
        'check_in': '2024-03-20',
        'check_out': '2024-03-22',
        'num_nights': 2
    }
    
    try:
        result = manager.publish_booking_reminder(booking, days_until=7)
        print("✓ Booking reminder published successfully")
        print(f"  Booking ID: {booking['booking_id']}")
        print(f"  Days until check-in: 7")
        print(f"  Check-in date: {booking['check_in']}")
        return True
    except Exception as e:
        print(f"✗ Failed to publish booking reminder: {e}")
        return False

def test_review_notification(manager):
    """Test review notification"""
    print_header("TEST 5: Review Notification")
    
    review = {
        'review_id': 'TEST-REV-001',
        'booking_id': 'TEST-BK-001',
        'guest_name': 'Test Guest',
        'overall_rating': 5,
        'status': 'pending',
        'created_at': datetime.now().isoformat(),
        'categories': {
            'cleanliness': 5,
            'comfort': 5,
            'location': 4,
            'service': 5,
            'value_for_money': 5
        },
        'comment': 'Excellent service and clean rooms! Would definitely come back.'
    }
    
    try:
        result = manager.publish_review_notification(review)
        print("✓ Review notification published successfully")
        print(f"  Review ID: {review['review_id']}")
        print(f"  Overall Rating: {review['overall_rating']}/5")
        print(f"  Status: {review['status'].upper()}")
        return True
    except Exception as e:
        print(f"✗ Failed to publish review notification: {e}")
        return False

def test_alert(manager):
    """Test system alert"""
    print_header("TEST 6: System Alert")
    
    try:
        result = manager.publish_alert(
            alert_type='High Booking Volume',
            message='Booking rate exceeded 50/hour. Consider scaling up infrastructure.',
            severity='WARNING'
        )
        print("✓ System alert published successfully")
        print(f"  Alert Type: High Booking Volume")
        print(f"  Severity: WARNING")
        print(f"  Timestamp: {datetime.now().isoformat()}")
        return True
    except Exception as e:
        print(f"✗ Failed to publish alert: {e}")
        return False

def test_subscriptions(manager):
    """Test get subscriptions"""
    print_header("TEST 7: Topic Subscriptions")
    
    topics_to_check = [
        'booking-confirmations',
        'alerts'
    ]
    
    try:
        for topic in topics_to_check:
            subs = manager.get_topic_subscriptions(topic)
            print(f"\n  Topic: {topic}")
            print(f"  Subscriptions: {len(subs)}")
            
            for sub in subs:
                protocol = sub.get('Protocol', 'N/A')
                endpoint = sub.get('Endpoint', 'N/A')
                status = sub.get('SubscriptionArn', 'N/A')
                
                print(f"    - {protocol.upper()}: {endpoint}")
        
        print("\n✓ Subscriptions retrieved successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to retrieve subscriptions: {e}")
        return False

def test_topic_attributes(manager):
    """Test get topic attributes"""
    print_header("TEST 8: Topic Attributes")
    
    try:
        attrs = manager.get_topic_attributes('booking-confirmations')
        print("✓ Topic attributes retrieved successfully")
        print(f"\n  Topic: booking-confirmations")
        
        for key, value in attrs.items():
            if len(str(value)) > 50:
                print(f"  - {key}: {str(value)[:50]}...")
            else:
                print(f"  - {key}: {value}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to retrieve topic attributes: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*50)
    print("  AWS SNS Integration Tests")
    print("="*50)
    print("\nStarting SNS notification tests...\n")
    
    # Initialize
    manager = test_sns_initialization()
    if not manager:
        print("\n✗ Cannot continue without SNS manager")
        return False
    
    # Run tests
    tests = [
        ("Booking Confirmation", test_booking_confirmation),
        ("Payment Confirmation", test_payment_confirmation),
        ("Booking Reminder", test_booking_reminder),
        ("Review Notification", test_review_notification),
        ("System Alert", test_alert),
        ("Topic Subscriptions", test_subscriptions),
        ("Topic Attributes", test_topic_attributes)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func(manager)
        except Exception as e:
            print(f"\n✗ {test_name} failed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All SNS tests passed!")
        print("\nNext steps:")
        print("1. Check your email for SNS notifications")
        print("2. Confirm email subscriptions if needed")
        print("3. Monitor AWS SNS Console for message delivery")
        print("4. Integrate with Flask API endpoints")
        return True
    else:
        print(f"\n✗ {total - passed} test(s) failed")
        print("\nTroubleshooting:")
        print("- Verify AWS credentials are set (aws sts get-caller-identity)")
        print("- Ensure SNS topics were created (bash sns_setup.sh)")
        print("- Check CloudWatch logs for error details")
        print("- Review SNS_INTEGRATION_GUIDE.md for troubleshooting")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
