# 🔐 Dual Authentication System Documentation

## Project TYRA Enhanced Security Setup

This documentation covers the implementation and usage of the dual authentication system for Project TYRA's mentor dashboard applications.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Authentication Methods](#authentication-methods)
3. [Technical Implementation](#technical-implementation)
4. [Security Features](#security-features)
5. [Setup Instructions](#setup-instructions)
6. [User Guide](#user-guide)
7. [Troubleshooting](#troubleshooting)
8. [Security Best Practices](#security-best-practices)
9. [API Reference](#api-reference)

---

## 🌟 Overview

The dual authentication system provides mentors with two secure login options:

- **🔑 Verification Code Authentication**: Traditional code-based login using pre-distributed codes
- **📧 Email OTP Authentication**: Auth0-powered passwordless email authentication

Both methods provide equivalent access to the mentor dashboard while maintaining high security standards.

### Benefits

- ✅ **User Choice**: Mentors can choose their preferred authentication method
- ✅ **Enhanced Security**: Multiple layers of protection against unauthorized access
- ✅ **Seamless Experience**: Both methods lead to the same authenticated state
- ✅ **Audit Trail**: Complete logging of all authentication attempts
- ✅ **Rate Limiting**: Protection against brute force attacks

---

## 🔐 Authentication Methods

### Method 1: Verification Code Authentication

**How it works:**
1. Mentors receive unique verification codes via email
2. Codes are stored in Google Sheets with mentor information
3. Users enter their code to access the dashboard
4. System validates against the mentor database

**Security Features:**
- Case-sensitive codes
- Input validation and sanitization
- Rate limiting (5 attempts per 5 minutes)
- Audit logging

### Method 2: Email OTP Authentication

**How it works:**
1. Mentors enter their registered email address
2. System sends 6-digit code via Auth0
3. Users verify the code within 5 minutes
4. System matches email to mentor records
5. Access granted upon successful verification

**Security Features:**
- Time-limited codes (5-minute expiration)
- Auth0's enterprise-grade security
- Email validation
- Protection against replay attacks

---

## 🛠️ Technical Implementation

### Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend UI   │    │   Streamlit      │    │  Data Sources   │
│  (Dual Login)   │◄──►│   Application    │◄──►│ (Google Sheets) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │     Auth0       │
                       │  (Email OTP)    │
                       └─────────────────┘
```

### Core Components

#### 1. Input Validation System

```python
def validate_input(input_string, input_type="general"):
    """
    Validates and sanitizes user inputs
    
    Args:
        input_string: The input to validate
        input_type: Type of validation ("verification_code", "email", "general")
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
```

**Validation Rules:**
- **Verification Code**: 6-50 characters, alphanumeric + underscore/hyphen only
- **Email**: Standard RFC-compliant email format validation
- **General**: Protection against XSS, SQL injection, and control characters

#### 2. Rate Limiting System

```python
def check_rate_limit(identifier):
    """
    Implements rate limiting for authentication attempts
    
    Args:
        identifier: Unique identifier for rate limiting
    
    Returns:
        bool: True if within limits, False if rate limited
    """
```

**Rate Limit Rules:**
- Maximum 5 attempts per 5-minute window
- Separate tracking for verification codes and email OTP
- Automatic reset after time window expires

#### 3. Session Management

```python
# Session State Variables
st.session_state.authenticated = False
st.session_state.mentor_name = None
st.session_state.mentor_data = None
st.session_state.login_method = None
st.session_state.login_time = None
```

**Session Features:**
- Unified state across authentication methods
- 1-hour automatic timeout
- Secure logout functionality
- Method tracking for audit purposes

#### 4. Auth0 Integration

```python
# OTP Send Request
POST https://{AUTH0_DOMAIN}/passwordless/start
{
    "client_id": AUTH0_CLIENT_ID,
    "connection": "email",
    "email": user_email,
    "send": "code"
}

# OTP Verification
POST https://{AUTH0_DOMAIN}/oauth/token
{
    "grant_type": "http://auth0.com/oauth/grant-type/passwordless/otp",
    "client_id": AUTH0_CLIENT_ID,
    "client_secret": AUTH0_CLIENT_SECRET,
    "username": user_email,
    "otp": verification_code,
    "realm": "email",
    "scope": "openid profile email"
}
```

---

## 🔒 Security Features

### 1. Input Protection

- **XSS Prevention**: HTML/script tag filtering
- **SQL Injection Protection**: SQL keyword detection
- **Control Character Filtering**: Removal of dangerous control characters
- **Length Validation**: Appropriate limits for each input type

### 2. Authentication Security

- **Brute Force Protection**: Rate limiting with exponential backoff
- **Session Security**: Automatic timeout and secure state management
- **Audit Logging**: Complete trail of authentication attempts
- **Token Security**: Secure handling of Auth0 access tokens

### 3. Data Protection

- **Server-side Filtering**: Minimal data exposure through targeted queries
- **Safe Downloads**: Sanitized filenames prevent path traversal
- **Error Handling**: No sensitive information in error messages
- **Secure Storage**: Credentials stored in Streamlit secrets

---

## ⚙️ Setup Instructions

### Prerequisites

1. **Streamlit Cloud Account** with secrets management
2. **Auth0 Account** with passwordless email configuration
3. **Google Sheets** with mentor data properly formatted
4. **Python Environment** with required dependencies

### 1. Auth0 Configuration

#### Create Auth0 Application

**Your Auth0 is already configured!** Your working setup uses:
- **Domain**: `dev-l6j5dixd3desex41.us.auth0.com`
- **Client ID**: `P5EMWnVXS1mKga0uGb4OthQG2A1kmKOA`
- **Application Type**: Single Page Application (already configured)

To verify your current settings:
1. Log into your Auth0 dashboard at `https://manage.auth0.com/`
2. Navigate to your existing application
3. Confirm these settings are in place:

```
Application Type: Single Page Application
Token Endpoint Authentication Method: POST
Allowed Callback URLs: http://localhost:8501
Allowed Web Origins: http://localhost:8501
Allowed Origins (CORS): http://localhost:8501
```

#### Enable Passwordless Email

**To enable the Email OTP feature** (if not already enabled):
1. Go to Authentication → Passwordless in your Auth0 dashboard
2. Toggle ON the "Email" connection
3. Configure the email template:

```html
Subject: Your Project TYRA Login Code
Body: Your verification code is: {{ code }}
This code expires in 5 minutes.
```

**Note**: If you've tested passwordless email before, this may already be configured.

#### Get Credentials

Your working credentials (already in secrets.toml):
- **Domain**: `dev-l6j5dixd3desex41.us.auth0.com`
- **Client ID**: `P5EMWnVXS1mKga0uGb4OthQG2A1kmKOA`
- **Client Secret**: `VtmmR_DM0cJ2oyRYXas_xff3FDaaGOA-c2KBHQyJIY2FL8lhZiN-QCrsIGfUUy6h`

These are already configured in your `.streamlit/secrets.toml` file and working with your prototype.

### 2. Streamlit Secrets Configuration

Your current working configuration in `.streamlit/secrets.toml`:

```toml
# Auth0 Configuration (Working Setup)
auth0_domain = "dev-l6j5dixd3desex41.us.auth0.com"
auth0_client_id = "P5EMWnVXS1mKga0uGb4OthQG2A1kmKOA"
auth0_client_secret = "VtmmR_DM0cJ2oyRYXas_xff3FDaaGOA-c2KBHQyJIY2FL8lhZiN-QCrsIGfUUy6h"
auth0_redirect_uri = "http://localhost:8501"
auth0_audience = "https://dev-l6j5dixd3desex41.us.auth0.com/userinfo"

# Google Sheets URLs (Your Existing Configuration)
mentee_response_sheet_url = "https://docs.google.com/spreadsheets/d/1kcukr9kPwohcdYNY4Tf9LIk2ftgOJsY0sMdzFNghzF0/edit?gid=1463194027"
mentor_sheet_url = "https://docs.google.com/spreadsheets/d/1kDgAl5ermaQtDNPYJJavsVt9lhG9ENmsxjRmT_tmmNQ/edit?gid=496135894"
mentor_matched_url = "https://docs.google.com/spreadsheets/d/10uWmgQWPywMLFpk8Y0X60cRNLtlnYjERz7Zrhyajltg/edit?gid=1667277099"
mentee_matched_url = "https://docs.google.com/spreadsheets/d/1P7LeoiBmSJmgLOffZRIwER-PZ7--dN6YbRxyTqKBqEQ/edit?gid=1289745482"
```

**Note**: Your Auth0 configuration is already set up and working! The enhanced app will use these existing credentials.

### 3. Google Sheets Setup

#### Mentor Data Sheet Structure

Your mentor sheet (`https://docs.google.com/spreadsheets/d/1kDgAl5ermaQtDNPYJJavsVt9lhG9ENmsxjRmT_tmmNQ/edit?gid=496135894`) should have these columns:

Required columns:
- `verification_code`: Unique verification codes (already working)
- `name`: Mentor full name
- `email`: Primary email address (**required for Email OTP**)
- `email2`: Secondary email (optional)
- `combined_mentor_id`: Unique mentor identifier

**Important**: Make sure your mentor sheet has an `email` column with valid email addresses for mentors who want to use the Email OTP login method.

#### Data Validation

Ensure your mentor data includes:
- Unique verification codes (6+ characters)
- Valid email addresses
- Proper UTF-8 encoding for Chinese characters

### 4. Dependencies Installation

```bash
pip install streamlit pandas requests urllib3
```

### 5. Application Deployment

1. **Local Testing**:
   ```bash
   streamlit run app_screening_enhanced.py
   ```

2. **Streamlit Cloud Deployment**:
   - Push code to GitHub repository
   - Connect to Streamlit Cloud
   - Configure secrets in Streamlit Cloud dashboard
   - Deploy application

---

## 👥 User Guide

### For Mentors

#### Option 1: Verification Code Login

1. **Receive Your Code**
   - Check your email for the verification code
   - Note: Codes are case-sensitive

2. **Access the Dashboard**
   - Go to the Project TYRA mentor dashboard
   - Click on "Verification Code Login"
   - Enter your code exactly as provided
   - Click "Login with Code"

3. **Dashboard Access**
   - Upon successful login, you'll see your mentor dashboard
   - Review mentee profiles and submit preferences

#### Option 2: Email OTP Login

1. **Enter Your Email**
   - Go to the Project TYRA mentor dashboard
   - Click on "Email OTP Login"
   - Enter your registered email address
   - Click "Send Login Code"

2. **Check Your Inbox**
   - Look for an email with a 6-digit code
   - Code expires in 5 minutes
   - Enter the code in the verification field

3. **Complete Login**
   - Click "Verify Code"
   - Upon success, access your mentor dashboard

### Security Tips for Users

- ✅ **Never share your verification codes**
- ✅ **Log out when finished**
- ✅ **Use a secure internet connection**
- ✅ **Check email sender authenticity**
- ❌ **Don't use public computers for sensitive access**

---

## 🔧 Troubleshooting

### Common Issues

#### 1. "Invalid verification code" Error

**Symptoms**: Error message when entering verification code
**Solutions**:
- Check for typos (codes are case-sensitive)
- Ensure you're using the latest code sent
- Contact administrator if code seems incorrect

#### 2. "Email not found" Error

**Symptoms**: Email not recognized during OTP login
**Solutions**:
- Verify email address spelling
- Check if you're using the registered email
- Try alternative email if you have multiple registered

#### 3. "Code expired" Error

**Symptoms**: OTP code no longer valid
**Solutions**:
- Request a new code (codes expire in 5 minutes)
- Check your system clock accuracy
- Ensure stable internet connection

#### 4. "Too many attempts" Error

**Symptoms**: Rate limiting triggered
**Solutions**:
- Wait 5 minutes before trying again
- Ensure you're entering correct credentials
- Contact support if issue persists

#### 5. Auth0 Configuration Issues

**Symptoms**: Email OTP not working
**Solutions**:
- Verify Auth0 credentials in secrets
- Check Auth0 application configuration
- Ensure passwordless email is enabled

### Debugging Steps

#### For Administrators

1. **Check Logs**
   ```python
   # Enable debug logging
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Verify Secrets**
   ```python
   # Test secrets availability
   try:
       auth0_domain = st.secrets["auth0_domain"]
       print("Auth0 configured correctly")
   except KeyError:
       print("Auth0 configuration missing")
   ```

3. **Test Data Sources**
   ```python
   # Verify Google Sheets access
   try:
       df = pd.read_csv(mentor_sheet_url)
       print(f"Loaded {len(df)} mentor records")
   except Exception as e:
       print(f"Data loading error: {e}")
   ```

---

## 🛡️ Security Best Practices

### For Administrators

#### 1. Regular Security Reviews

- **Monthly**: Review authentication logs for suspicious activity
- **Quarterly**: Update Auth0 configurations and rotate secrets
- **Annually**: Conduct comprehensive security audit

#### 2. Access Control

- **Principle of Least Privilege**: Grant minimal necessary permissions
- **Regular Cleanup**: Remove inactive mentor accounts
- **Audit Trail**: Maintain comprehensive logging

#### 3. Data Protection

- **Encryption**: Ensure data transmission encryption (HTTPS)
- **Backup**: Regular secure backups of mentor data
- **Privacy**: Minimal data collection and retention

#### 4. Incident Response

- **Monitoring**: Set up alerts for unusual authentication patterns
- **Response Plan**: Document steps for security incidents
- **Communication**: Prepare templates for security notifications

### For Users

#### 1. Password Hygiene

- Use strong, unique passwords for email accounts
- Enable two-factor authentication on email
- Regular password updates

#### 2. Device Security

- Keep devices updated with latest security patches
- Use reputable antivirus software
- Avoid public Wi-Fi for sensitive access

#### 3. Email Security

- Verify sender authenticity
- Report suspicious emails
- Don't click suspicious links

---

## 📚 API Reference

### Core Functions

#### `validate_input(input_string, input_type)`

Validates and sanitizes user inputs.

**Parameters:**
- `input_string` (str): Input to validate
- `input_type` (str): Validation type ("verification_code", "email", "general")

**Returns:**
- `tuple`: (is_valid: bool, error_message: str)

**Example:**
```python
is_valid, error = validate_input("test@example.com", "email")
if is_valid:
    proceed_with_authentication()
```

#### `check_rate_limit(identifier)`

Implements rate limiting for authentication attempts.

**Parameters:**
- `identifier` (str): Unique identifier for rate limiting

**Returns:**
- `bool`: True if within limits, False if rate limited

**Example:**
```python
if check_rate_limit(f"verify_{code}"):
    process_verification()
```

#### `log_access_attempt(identifier, method, success)`

Logs authentication attempts for security monitoring.

**Parameters:**
- `identifier` (str): User identifier (hashed)
- `method` (str): Authentication method used
- `success` (bool): Whether attempt was successful

**Example:**
```python
log_access_attempt(email, "email_otp", True)
```

#### `get_user_info(access_token)`

Retrieves user information from Auth0.

**Parameters:**
- `access_token` (str): Auth0 access token

**Returns:**
- `dict`: User information or None if failed

**Example:**
```python
user_info = get_user_info(token)
if user_info:
    process_user_data(user_info)
```

### Session State Variables

| Variable | Type | Description |
|----------|------|-------------|
| `authenticated` | bool | Authentication status |
| `mentor_name` | str | Mentor identifier |
| `mentor_data` | dict | Complete mentor information |
| `login_method` | str | Authentication method used |
| `login_time` | float | Login timestamp |
| `user` | dict | Auth0 user information |
| `email` | str | Email for OTP authentication |

### Configuration Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AUTH0_DOMAIN` | Auth0 tenant domain | Yes |
| `AUTH0_CLIENT_ID` | Auth0 application client ID | Yes |
| `AUTH0_CLIENT_SECRET` | Auth0 application secret | Yes |
| `AUTH0_REDIRECT_URI` | OAuth redirect URI | No |
| `AUTH0_AUDIENCE` | Auth0 API audience | No |

---

## 🔄 Version History

### v2.0.0 (Current)
- ✅ Dual authentication system implementation
- ✅ Enhanced security features
- ✅ Comprehensive audit logging
- ✅ Rate limiting and input validation

### v1.0.0 (Legacy)
- ✅ Basic verification code authentication
- ✅ Google Sheets integration
- ✅ Mentee profile viewing

---

## 📞 Support

### For Technical Issues

1. **Check this documentation first**
2. **Review troubleshooting section**
3. **Contact system administrator**
4. **Submit GitHub issue** (for bugs)

### For Security Concerns

1. **Immediate**: Contact security team
2. **Document**: Record incident details
3. **Follow-up**: Monitor for resolution

---

## 🏆 Contributors

- **Development Team**: Project TYRA Technical Team
- **Security Review**: Independent Security Consultants
- **Testing**: Mentor Community Beta Testers

---

## 📄 License

This documentation is part of the Project TYRA MMP Screening System.
For license information, see the main repository.

---

**Last Updated**: July 27, 2025  
**Version**: 2.0.0  
**Maintained by**: Project TYRA Technical Team
