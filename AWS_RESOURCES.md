# AWS Resources - Hotel Booking System

## Account Information

| Property | Value |
|----------|-------|
| **AWS Account ID** | `491694398940` |
| **Region** | `us-east-1` (N. Virginia) |
| **Created** | March 8, 2026 |

## IAM Configuration

### Role

```
Role Name: hotel_booking_role
Role ARN: arn:aws:iam::491694398940:role/hotel_booking_role
```

**Permissions needed:**
- DynamoDB: Read/Write on all booking tables
- S3: Read/Write on static assets bucket
- SNS: Publish to hotel_booking_sns topic
- CloudWatch: PutMetricAlarm, PutLogs
- SES: SendEmail (optional for emails)

## SNS Configuration

### Main Topic

```
Topic Name: hotel_booking_sns
Topic ARN: arn:aws:sns:us-east-1:491694398940:hotel_booking_sns
```

**Purpose:** Central notification hub for all notification types
- Booking confirmations
- Payment confirmations  
- Pre-arrival reminders
- Review notifications
- System alerts

**Subscriptions:** Add email/SMS endpoints as needed

## EC2 Instance

### Connection Details

```
Public IP: 44.208.253.176
Region: us-east-1 (N. Virginia)
OS: Ubuntu 22.04 LTS
Instance Type: t2.micro or t3.small (free tier eligible)
```

### Application URLs

```
Website: http://44.208.253.176:5000
API: http://44.208.253.176:5000/api
SSH: ssh -i your-key.pem ubuntu@44.208.253.176
```

### Security Group

**Required Open Ports:**
- 22 (SSH) - Restrict to your IP
- 80 (HTTP) - Open to 0.0.0.0/0  
- 443 (HTTPS) - Open to 0.0.0.0/0

## DynamoDB Tables

```
Database Type: DynamoDB (serverless)
Billing Model: PAY_PER_REQUEST
```

### Tables to Create

1. **hotel_users**
   - Primary Key: user_id (String)
   - GSI: email (String)

2. **hotel_rooms**
   - Primary Key: room_id (String)
   - GSI: room_type (String)

3. **hotel_bookings**
   - Primary Key: booking_id (String)
   - GSI: user_id (String), check_in_date (String)

4. **hotel_reviews**
   - Primary Key: review_id (String)
   - GSI: room_id (String)

**Setup command:**
```bash
python dynamodb_setup.py
```

## S3 Bucket

```
Bucket Name: hotel-booking-static-XXXXXX
Region: us-east-1
Static Files: CSS, JavaScript, images
CloudFront: CDN distribution
```

## Environment Configuration

All values below are configured in `.env` file:

```bash
# AWS Credentials
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<your-access-key>
AWS_SECRET_ACCESS_KEY=<your-secret-key>
AWS_IAM_ROLE_ARN=arn:aws:iam::491694398940:role/hotel_booking_role

# SNS Topics (All pointing to single topic)
SNS_ENABLED=True
SNS_REGION=us-east-1
SNS_BOOKING_CONFIRMATIONS_TOPIC_ARN=arn:aws:sns:us-east-1:491694398940:hotel_booking_sns
SNS_PAYMENT_CONFIRMATIONS_TOPIC_ARN=arn:aws:sns:us-east-1:491694398940:hotel_booking_sns
SNS_BOOKING_REMINDERS_TOPIC_ARN=arn:aws:sns:us-east-1:491694398940:hotel_booking_sns
SNS_REVIEWS_NOTIFICATIONS_TOPIC_ARN=arn:aws:sns:us-east-1:491694398940:hotel_booking_sns
SNS_ALERTS_TOPIC_ARN=arn:aws:sns:us-east-1:491694398940:hotel_booking_sns

# Application URLs
FRONTEND_URL=http://44.208.253.176:5000
API_URL=http://44.208.253.176:5000/api
EC2_IP=44.208.253.176
EC2_DOMAIN=your-domain.com

# Database
AWS_DYNAMODB_TABLE_USERS=hotel_users
AWS_DYNAMODB_TABLE_ROOMS=hotel_rooms
AWS_DYNAMODB_TABLE_BOOKINGS=hotel_bookings
AWS_DYNAMODB_TABLE_REVIEWS=hotel_reviews
```

## Deployment Steps

### 1. Connect to EC2

```bash
ssh -i your-key.pem ubuntu@44.208.253.176
```

### 2. Clone Repository

```bash
git clone https://github.com/your-username/hotel-booking.git
cd hotel-booking
```

### 3. Setup Environment

```bash
# Copy environment file
cp .env.example .env

# Edit with actual values (AWS credentials)
nano .env
```

### 4. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install boto3  # For SNS
```

### 5. Create DynamoDB Tables

```bash
python dynamodb_setup.py
```

### 6. Start Application

```bash
# Development (manual)
python app.py

# Production (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Background service
sudo systemctl start hotel-booking
sudo systemctl status hotel-booking
```

## Testing Connectivity

### Check EC2 Accessibility

```bash
# From local machine
curl http://44.208.253.176:5000

# Expected: Flask application home page
```

### Test SNS Integration

```bash
# On EC2 instance
source venv/bin/activate
python test_sns.py

# Expected: ✓ All tests pass
```

### Test DynamoDB Access

```bash
# On EC2 instance
python -c "import boto3; print(boto3.client('dynamodb').list_tables())"
```

## AWS Console Links

- **EC2:** https://console.aws.amazon.com/ec2/
- **DynamoDB:** https://console.aws.amazon.com/dynamodb/
- **SNS:** https://console.aws.amazon.com/sns/
- **S3:** https://console.aws.amazon.com/s3/
- **CloudWatch:** https://console.aws.amazon.com/cloudwatch/
- **IAM:** https://console.aws.amazon.com/iam/

## Monitoring

### CloudWatch Logs

```bash
# View application logs
tail -f /var/log/hotel-booking/app.log

# View system logs (on EC2)
sudo journalctl -u hotel-booking -f
```

### SNS Delivery Status

1. AWS Console → SNS → Topics → hotel_booking_sns
2. Check "Activity" section for message delivery status
3. View "Subscriptions" to see active subscribers

## Cost Estimation

| Service | Free Tier | Monthly Cost |
|---------|-----------|---|
| **EC2 t2.micro** | 12 months free | $0 |
| **EC2 t3.small** | Not included | $10-15 |
| **DynamoDB** | 25 GB storage free | $0-5 |
| **SNS** | 1,000 emails free | ~$1 (if over limit) |
| **S3** | 5 GB free | ~$1-3 |
| **Route 53** | First 50 queries/month free | ~$0.50 |
| **Total (Free Tier)** | - | **$0-20** |

## Troubleshooting

### Issue: Cannot SSH to EC2

```bash
# Check security group allows port 22 from your IP
# Check key file permissions:
chmod 400 your-key.pem

# Try again:
ssh -i your-key.pem ubuntu@44.208.253.176
```

### Issue: SNS Publish Fails

```bash
# Verify IAM role has SNS:Publish permission
# Check SNS topic ARN in .env matches:
# arn:aws:sns:us-east-1:491694398940:hotel_booking_sns

# Test manually:
python test_sns.py
```

### Issue: DynamoDB Tables Not Found

```bash
# Check tables exist:
python -c "import boto3; dt=boto3.client('dynamodb'); print([t['Name'] for t in dt.list_tables()['TableNames']])"

# Create if missing:
python dynamodb_setup.py
```

### Issue: Application Won't Start

```bash
# Check logs:
sudo journalctl -u hotel-booking -n 50

# Check dependencies:
source venv/bin/activate
pip list

# Check port 5000 is available:
sudo lsof -i :5000
```

## Security Checklist

- [ ] SSH key stored securely (never commit to Git)
- [ ] Security group restricts SSH to your IP
- [ ] IAM role follows principle of least privilege
- [ ] .env file is in .gitignore
- [ ] HTTPS certificate installed (Let's Encrypt or AWS ACM)
- [ ] SNS topic policy restricts publishers
- [ ] DynamoDB encryption enabled
- [ ] S3 bucket has public access blocked
- [ ] CloudWatch alarms configured for anomalies
- [ ] Backups enabled for critical data

## Quick Commands

```bash
# SSH to EC2
ssh -i your-key.pem ubuntu@44.208.253.176

# View application status
curl http://44.208.253.176:5000/health

# Restart application
sudo systemctl restart hotel-booking

# View logs
sudo journalctl -u hotel-booking -f

# Update code from Git
cd hotel-booking && git pull origin main

# Install new dependencies
source venv/bin/activate
pip install -r requirements.txt

# Test SNS
python test_sns.py

# Create/update databases
python dynamodb_setup.py
```

## Next Steps

1. ✅ SSH into EC2 instance
2. ✅ Install application dependencies
3. ✅ Create DynamoDB tables
4. ✅ Configure .env with credentials
5. ✅ Start Flask application
6. ✅ Test API endpoints
7. ✅ Set up SNS subscriptions
8. ✅ Configure HTTPS/SSL
9. ✅ Connect custom domain
10. ✅ Set up monitoring and alerts

## Support

For issues or questions:
- Check `.env` file values match this document
- Review AWS Console for resource status
- Check CloudWatch logs for errors
- Run `test_sns.py` to verify SNS
- Ensure security group allows required ports
