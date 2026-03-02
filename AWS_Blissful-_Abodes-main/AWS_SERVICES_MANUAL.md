# 🛠️ Blissful Abodes — Manual AWS Services Setup Guide

> Step-by-step instructions to create every AWS service manually in the AWS Console.
> Region for all services: **us-east-1 (N. Virginia)**

---

## 📋 All Services Overview

| #   | Service                 | Purpose                     | Cost                   |
| --- | ----------------------- | --------------------------- | ---------------------- |
| 1   | **Amazon SNS**          | SMS / OTP / Booking alerts  | Free (1M/month)        |
| 2   | **Amazon SES**          | Booking confirmation emails | Free (62K/month)       |
| 3   | **Amazon S3**           | Room images storage         | Free (5 GB)            |
| 4   | **Amazon CloudFront**   | Fast image delivery (CDN)   | Free (1 TB/month)      |
| 5   | **Amazon DynamoDB**     | Hotel database              | Free (25 GB)           |
| 6   | **Amazon EC2**          | App server                  | Free (750 hrs/month)   |
| 7   | **Amazon Rekognition**  | ID/face verification        | ₹0.80 per 1,000 images |
| 8   | **Amazon Comprehend**   | Review sentiment analysis   | Free (50K units/month) |
| 9   | **AWS CloudWatch**      | Monitoring & alerts         | Free tier              |
| 10  | **AWS Secrets Manager** | Secure key storage          | $0.40/secret/month     |

---

## SERVICE 1 — Amazon SNS (SMS & Notifications)

Used for: **OTP login, booking SMS alerts, admin notifications**

### Step 1 — Create SNS Topic

1. Go to **AWS Console** → Search **"SNS"** → Open **Simple Notification Service**
2. Left menu → **Topics** → **Create topic**
3. Fill in:

| Field        | Value                    |
| ------------ | ------------------------ |
| Type         | **Standard**             |
| Name         | `blissful-abodes-alerts` |
| Display name | `BlissfulAbodes`         |

4. Click **Create topic**
5. Copy the **ARN** — looks like:
   ```
   arn:aws:sns:us-east-1:123456789012:blissful-abodes-alerts
   ```

### Step 2 — Subscribe Email to Topic

1. Open the topic you just created
2. Click **Create subscription**
3. Fill in:

| Field    | Value                     |
| -------- | ------------------------- |
| Protocol | **Email**                 |
| Endpoint | `info@blissfulabodes.com` |

4. Click **Create subscription**
5. Check your email → click **Confirm subscription**

### Step 3 — Enable SMS (for OTPs)

1. Left menu → **Text messaging (SMS)**
2. Click **Edit**
3. **Default message type:** `Transactional` _(higher priority)_
4. **Default sender ID:** `BLISSFUL`
5. Save changes

### Step 4 — Add to .env

```env
SNS_SENDER_ID=BLISSFUL
CLOUDWATCH_ALARM_SNS_ARN=arn:aws:sns:us-east-1:XXXXXXXXXXXX:blissful-abodes-alerts
```

### Step 5 — Test SNS

Go to **Topics** → Select topic → **Publish message**:

```
Subject: Test Alert
Message: Blissful Abodes SNS is working!
```

Click **Publish** → You should receive the email ✅

---

## SERVICE 2 — Amazon SES (Email Service)

Used for: **Booking confirmations, invoices, password reset OTPs**

### Step 1 — Open SES Console

1. Search **"SES"** → Open **Amazon Simple Email Service**
2. Make sure region is **us-east-1 (N. Virginia)**

### Step 2 — Verify Your Email Address

1. Left menu → **Verified identities** → **Create identity**
2. Choose **Email address**
3. Enter: `noreply@blissfulabodes.com`
4. Click **Create identity**
5. Check your inbox → Click the verification link ✅

### Step 3 — Verify Your Domain (Recommended)

1. **Verified identities** → **Create identity**
2. Choose **Domain**
3. Enter: `blissfulabodes.com`
4. Enable **Easy DKIM** → Select `RSA_2048_BIT`
5. Click **Create identity**
6. Copy the **CNAME records** → Add to your domain DNS provider
7. Wait 24–48 hours for verification

### Step 4 — Request Production Access

> By default SES is in **Sandbox mode** — can only send to verified emails.

1. Left menu → **Account dashboard**
2. Under **Sending limits** → click **Request production access**
3. Fill in:
   - Mail type: `Transactional`
   - Website URL: `https://blissfulabodes.com`
   - Use case: _"Booking confirmations and OTP emails for hotel guests"_
4. Submit → AWS approves in 24 hours

### Step 5 — Add to .env

```env
SES_FROM_EMAIL=noreply@blissfulabodes.com
```

---

## SERVICE 3 — Amazon S3 (Room Images Storage)

Used for: **Room photos, uploaded images, guest ID documents**

### Step 1 — Create Bucket

1. Search **"S3"** → Open **S3 Console**
2. Click **Create bucket**
3. Fill in:

| Field                   | Value                              |
| ----------------------- | ---------------------------------- |
| Bucket name             | `blissful-abodes-media`            |
| Region                  | `us-east-1`                        |
| Block all public access | ❌ **Uncheck** (for public images) |
| Versioning              | Enable (optional, for backup)      |

4. Click **Create bucket**

### Step 2 — Add Bucket Policy (Public Read)

1. Click on your bucket → **Permissions** tab
2. Scroll to **Bucket policy** → **Edit**
3. Paste:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::blissful-abodes-media/*"
    }
  ]
}
```

4. Click **Save changes**

### Step 3 — Create Folders

1. Click **Create folder**
2. Create: `rooms/`
3. Create: `uploads/`
4. Create: `invoices/`

### Step 4 — Add to .env

```env
S3_BUCKET_NAME=blissful-abodes-media
```

---

## SERVICE 4 — Amazon CloudFront (CDN for Fast Image Loading)

Used for: **Serve room images 90% faster worldwide via CDN**

### Step 1 — Create Distribution

1. Search **"CloudFront"** → Open **CloudFront Console**
2. Click **Create distribution**
3. Fill in:

| Field                  | Value                                              |
| ---------------------- | -------------------------------------------------- |
| Origin domain          | `blissful-abodes-media.s3.us-east-1.amazonaws.com` |
| Origin access          | **Public**                                         |
| Viewer protocol policy | **Redirect HTTP to HTTPS**                         |
| Allowed HTTP methods   | **GET, HEAD**                                      |
| Cache policy           | **CachingOptimized**                               |
| Price class            | **Use all edge locations**                         |

4. Click **Create distribution**
5. Wait ~10 minutes for deployment
6. Copy the **Distribution domain name**:
   ```
   d1234567890abc.cloudfront.net
   ```

### Step 2 — Add to .env

```env
CLOUDFRONT_URL=https://d1234567890abc.cloudfront.net
```

### Step 3 — Use CloudFront URL for Images

In your app, images will be served as:

```
https://d1234567890abc.cloudfront.net/rooms/101.jpg
```

Instead of slow S3 direct URLs.

---

## SERVICE 5 — Amazon DynamoDB (Hotel Database)

Used for: **All hotel data — rooms, bookings, users, reviews, etc.**

### Step 1 — Create Each Table

Go to **DynamoDB Console** → **Create table** for each:

#### Table 1: Users

| Setting       | Value                  |
| ------------- | ---------------------- |
| Table name    | `BlissfulAbodes_Users` |
| Partition key | `user_id` (String)     |
| Billing mode  | On-demand              |

#### Table 2: Rooms

| Setting       | Value                  |
| ------------- | ---------------------- |
| Table name    | `BlissfulAbodes_Rooms` |
| Partition key | `room_id` (String)     |
| Billing mode  | On-demand              |

#### Table 3: Bookings

| Setting       | Value                     |
| ------------- | ------------------------- |
| Table name    | `BlissfulAbodes_Bookings` |
| Partition key | `booking_id` (String)     |
| Billing mode  | On-demand                 |

#### Table 4: Reviews

| Setting       | Value                    |
| ------------- | ------------------------ |
| Table name    | `BlissfulAbodes_Reviews` |
| Partition key | `review_id` (String)     |
| Billing mode  | On-demand                |

#### Table 5: Coupons

| Setting       | Value                    |
| ------------- | ------------------------ |
| Table name    | `BlissfulAbodes_Coupons` |
| Partition key | `coupon_code` (String)   |
| Billing mode  | On-demand                |

#### Table 6: Wishlists

| Setting       | Value                      |
| ------------- | -------------------------- |
| Table name    | `BlissfulAbodes_Wishlists` |
| Partition key | `user_id` (String)         |
| Sort key      | `room_id` (String)         |
| Billing mode  | On-demand                  |

#### Table 7: Notifications

| Setting       | Value                          |
| ------------- | ------------------------------ |
| Table name    | `BlissfulAbodes_Notifications` |
| Partition key | `notification_id` (String)     |
| Billing mode  | On-demand                      |

### Step 2 — Seed Data (on EC2 after setup)

```bash
source venv/bin/activate
python scripts/setup_dynamodb.py   # Creates all 7 tables
python scripts/seed_rooms.py       # 100 rooms
python scripts/seed_users.py       # 5 users + 5 coupons
```

---

## SERVICE 6 — Amazon EC2 (App Server)

Used for: **Hosting the Flask app + Nginx + Gunicorn**

### Step 1 — Launch Instance

1. **EC2 Console** → **Launch Instance**

| Setting       | Value                                                      |
| ------------- | ---------------------------------------------------------- |
| Name          | `BlissfulAbodes-Server`                                    |
| AMI           | Ubuntu Server 22.04 LTS                                    |
| Instance type | `t2.micro` (free) or `t3.medium` (prod)                    |
| Key pair      | Create new → Download `.pem`                               |
| Storage       | 20 GB gp3                                                  |
| IAM Role      | `BlissfulAbodesEC2Role` (from Step 2A in Deployment Guide) |

### Step 2 — Allocate Elastic IP (Fixed IP)

> Without this, your IP changes every time you stop/start EC2.

1. **EC2 Console** → Left menu → **Elastic IPs**
2. Click **Allocate Elastic IP address** → **Allocate**
3. Select the new IP → **Actions** → **Associate Elastic IP**
4. Select your instance → **Associate**
5. This IP is **free** as long as your instance is running ✅

### Step 3 — Install App

```bash
# Connect via SSH
ssh -i "blissful-abodes.pem" ubuntu@54.197.161.36

# Install Python 3.11
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-distutils nginx -y

# Clone your project
git clone https://github.com/ajithkumar31082004-bit/hotel-booking.git
cd hotel-booking

# Setup virtual env
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## SERVICE 7 — Amazon Rekognition (Face / ID Verification)

Used for: **Verify Aadhaar/Passport uploads, face match at check-in**

### Step 1 — No Setup Required!

Rekognition is a **fully managed API** — no setup needed in the console.
Your EC2 IAM Role (`BlissfulAbodesEC2Role`) with `AmazonRekognitionFullAccess` is all that's needed.

### Step 2 — How It's Used in the App

```python
# Detect faces in uploaded ID photo
import boto3
client = boto3.client('rekognition', region_name='us-east-1')

response = client.detect_faces(
    Image={'S3Object': {'Bucket': 'blissful-abodes-media', 'Name': 'uploads/id.jpg'}},
    Attributes=['ALL']
)
```

### Step 3 — Test via AWS Console

1. **Rekognition Console** → **Face liveness** or **Label detection**
2. Upload a test image → See automatic detection results ✅

---

## SERVICE 8 — Amazon Comprehend (Sentiment Analysis)

Used for: **Automatically detect if guest reviews are Positive/Negative/Neutral**

### Step 1 — No Setup Required!

Like Rekognition, Comprehend is fully managed. Just needs `ComprehendFullAccess` in the IAM Role.

### Step 2 — How It's Used in the App

```python
import boto3
client = boto3.client('comprehend', region_name='us-east-1')

response = client.detect_sentiment(
    Text="The room was absolutely beautiful and the staff were amazing!",
    LanguageCode='en'
)
# Returns: {'Sentiment': 'POSITIVE', 'SentimentScore': {...}}
```

### Step 3 — Test via AWS Console

1. **Comprehend Console** → **Real-time analysis**
2. Paste a review text → Click **Analyze**
3. See sentiment + key phrases + entities ✅

---

## SERVICE 9 — AWS CloudWatch (Monitoring & Alerts)

Used for: **Track app errors, server CPU, booking metrics, auto-alerts**

### Step 1 — Create Dashboard

1. **CloudWatch Console** → **Dashboards** → **Create dashboard**
2. Name: `BlissfulAbodes-Dashboard`
3. Add widgets:
   - **Line chart** → EC2 → CPUUtilization
   - **Number** → DynamoDB → ConsumedReadCapacityUnits
   - **Number** → DynamoDB → ConsumedWriteCapacityUnits

### Step 2 — Create CPU Alert

1. **Alarms** → **Create alarm**
2. Select metric: `EC2 → Per-instance → CPUUtilization`
3. Select your instance
4. Conditions:
   - Threshold type: **Static**
   - Whenever CPUUtilization is: **Greater than 80**
5. Notification: Select your SNS topic `blissful-abodes-alerts`
6. Alarm name: `BlissfulAbodes-HighCPU`
7. Click **Create alarm**

You'll get an **email + SMS** if CPU goes above 80% ✅

### Step 3 — Create Log Group

```bash
# On your EC2, install CloudWatch agent
sudo apt install amazon-cloudwatch-agent -y

# Configure it
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

---

## SERVICE 10 — AWS Secrets Manager (Secure Key Storage)

Used for: **Store Razorpay keys, Flask secret key securely — NOT in .env**

### Step 1 — Create Secret for Razorpay

1. **Secrets Manager Console** → **Store a new secret**
2. Secret type: **Other type of secret**
3. Key/value pairs:

| Key          | Value                      |
| ------------ | -------------------------- |
| `key_id`     | `rzp_live_XXXXXXXXXX`      |
| `key_secret` | `XXXXXXXXXXXXXXXXXXXXXXXX` |

4. Click **Next**
5. Secret name: `blissful/razorpay`
6. Description: `Razorpay payment keys for Blissful Abodes`
7. Click **Next** → **Next** → **Store**

### Step 2 — Create Secret for Flask

1. **Store a new secret** → **Other type**

| Key          | Value                                |
| ------------ | ------------------------------------ |
| `secret_key` | `your-very-long-random-flask-secret` |

2. Secret name: `blissful/flask`
3. Click **Store**

### Step 3 — How App Reads Secrets

```python
import boto3, json

def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])

# Usage
razorpay = get_secret('blissful/razorpay')
KEY_ID     = razorpay['key_id']
KEY_SECRET = razorpay['key_secret']
```

> [!TIP]
> With Secrets Manager, your `.env` file only needs `AWS_REGION=us-east-1`.
> All sensitive keys live securely in AWS — not on your server at all.

---

## ✅ Final Checklist — All Services

```
# SNS
[ ] SNS topic created: blissful-abodes-alerts
[ ] Email subscription confirmed
[ ] SMS Sender ID set to BLISSFUL
[ ] SNS ARN added to .env

# SES
[ ] Email address verified
[ ] Domain verified (DNS CNAME records added)
[ ] Production access requested/approved

# S3
[ ] Bucket created: blissful-abodes-media
[ ] Public read bucket policy added
[ ] Folders created: rooms/, uploads/, invoices/

# CloudFront
[ ] Distribution created (origin = S3 bucket)
[ ] CloudFront URL added to .env

# DynamoDB
[ ] All 7 tables created (On-demand billing)
[ ] Tables seeded with rooms + users

# EC2
[ ] Instance launched (Ubuntu 22.04)
[ ] IAM Role attached: BlissfulAbodesEC2Role
[ ] Elastic IP allocated and associated
[ ] App running with Gunicorn + Nginx

# Rekognition
[ ] IAM Role has AmazonRekognitionFullAccess

# Comprehend
[ ] IAM Role has ComprehendFullAccess

# CloudWatch
[ ] Dashboard created
[ ] CPU alarm created (>80% → SNS alert)

# Secrets Manager
[ ] blissful/razorpay secret created
[ ] blissful/flask secret created
[ ] App reads from Secrets Manager (not .env)
```

---

_Made with ❤️ for Blissful Abodes Chennai — Marina Beach Luxury Hotel_
