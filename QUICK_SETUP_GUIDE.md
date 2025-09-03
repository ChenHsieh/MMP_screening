# 🚀 Quick Setup Guide - Dual Authentication

## Ready to Deploy in 15 Minutes

This guide helps you quickly implement the dual authentication system for Project TYRA.

---

## ✅ Pre-flight Checklist

- [ ] Auth0 account access
- [ ] Streamlit Cloud deployment ready
- [ ] Google Sheets with mentor data
- [ ] Email service for verification codes

---

## 🔧 Step 1: Auth0 Setup (Already Done!) ✅

**Good news!** Your Auth0 is already configured and working with domain `dev-l6j5dixd3desex41.us.auth0.com`.

### Verify Current Configuration
1. Login to [Auth0 Dashboard](https://manage.auth0.com/)
2. Check your existing application settings
3. Ensure these are configured:

```
Application Type: Single Page Application
Token Endpoint Authentication Method: POST
Allowed Callback URLs: http://localhost:8501
Allowed Web Origins: http://localhost:8501
```

### ⚡ Quick Check: Enable Passwordless Email
1. Go to Authentication → Passwordless in Auth0 dashboard
2. If not already enabled, toggle ON "Email"
3. Configure email template:
   - Subject: `Your Project TYRA Login Code`
   - Body: `Your verification code is: {{ code }}`

### 🌐 For Production Deployment
When you deploy to Streamlit Cloud, you'll need to update:
1. **Auth0 Settings**: Add your production URL to Allowed Callback URLs
2. **Secrets**: Update `auth0_redirect_uri` to your production URL

**If passwordless email is already enabled, you're all set! Skip to Step 2.**

### Copy Credentials
```
Domain: dev-l6j5dixd3desex41.us.auth0.com
Client ID: P5EMWnVXS1mKga0uGb4OthQG2A1kmKOA
Client Secret: VtmmR_DM0cJ2oyRYXas_xff3FDaaGOA-c2KBHQyJIY2FL8lhZiN-QCrsIGfUUy6h
```

---

## 🔑 Step 2: Streamlit Secrets (Already Done!) ✅

Your `.streamlit/secrets.toml` already contains the working Auth0 configuration:

```toml
# Auth0 (Already configured and working!)
auth0_domain = "dev-l6j5dixd3desex41.us.auth0.com"
auth0_client_id = "P5EMWnVXS1mKga0uGb4OthQG2A1kmKOA"
auth0_client_secret = "VtmmR_DM0cJ2oyRYXas_xff3FDaaGOA-c2KBHQyJIY2FL8lhZiN-QCrsIGfUUy6h"
auth0_redirect_uri = "http://localhost:8501"

# Your existing Google Sheets URLs (already working)
mentee_response_sheet_url = "https://docs.google.com/spreadsheets/d/1kcukr9kPwohcdYNY4Tf9LIk2ftgOJsY0sMdzFNghzF0/edit?gid=1463194027#gid=1463194027"
mentor_sheet_url = "https://docs.google.com/spreadsheets/d/1kDgAl5ermaQtDNPYJJavsVt9lhG9ENmsxjRmT_tmmNQ/edit?gid=496135894#gid=496135894"
mentor_matched_url = "https://docs.google.com/spreadsheets/d/10uWmgQWPywMLFpk8Y0X60cRNLtlnYjERz7Zrhyajltg/edit?gid=1667277099#gid=1667277099"
mentee_matched_url = "https://docs.google.com/spreadsheets/d/1P7LeoiBmSJmgLOffZRIwER-PZ7--dN6YbRxyTqKBqEQ/edit?gid=1289745482#gid=1289745482"
```

**✨ Since your Auth0 is already configured, you can skip directly to Step 3!**

---

## 📊 Step 3: Verify Data Format (Already Done!) ✅

Your mentor sheet at:
`https://docs.google.com/spreadsheets/d/1kDgAl5ermaQtDNPYJJavsVt9lhG9ENmsxjRmT_tmmNQ/edit?gid=496135894`

Should have these columns (which you likely already have):
```
verification_code | name | email | combined_mentor_id
ABC123           | John | john@example.com | john_smith_2025
```

**✨ Since your verification code system already works, your data format is correct!**

---

## 🚀 Step 4: Deploy Enhanced App (Ready to Go!) 

**Since your Auth0 and data are already configured, you can deploy immediately:**

### Option A: Replace Existing App
```bash
# Backup current app
cp app_matching_confirmation_round_1.py app_backup.py

# Deploy enhanced version
cp app_screening_enhanced.py app_matching_confirmation_round_1.py
```

### Option B: Deploy as New App (Recommended for Testing)
```bash
# Keep both versions running
# Enhanced app is ready as app_screening_enhanced.py
streamlit run app_screening_enhanced.py
```

**🎯 Recommended**: Start with Option B to test, then switch to Option A when satisfied.

---

## ✅ Step 5: Test Both Methods (2 minutes)

### Test Verification Code (Should Work Immediately)
1. Open enhanced app → Verification Code tab
2. Enter any existing verification code from your mentor sheet
3. Verify mentor dashboard loads with existing functionality

### Test Email OTP (New Feature)
1. Open enhanced app → Email OTP tab
2. Enter a mentor email address from your mentor sheet
3. Check inbox for 6-digit code from Auth0
4. Enter code and verify access

**🔍 Troubleshooting**: If email OTP doesn't work immediately, check that passwordless email is enabled in your Auth0 dashboard at `dev-l6j5dixd3desex41.us.auth0.com`.

---

## 🔒 Security Verification

After deployment, verify these security features work:

- [ ] **Rate Limiting**: Try 6 wrong codes → should block
- [ ] **Input Validation**: Try `<script>` in code field → should reject
- [ ] **Session Timeout**: Leave idle 1+ hours → should auto-logout
- [ ] **Audit Logging**: Check logs for authentication events

---

## 🆘 Immediate Troubleshooting

### "Auth0 not configured" warning
**Fix**: Double-check `auth0_domain` in secrets.toml

### "Email not found" error
**Fix**: Verify email exists in mentor sheet `email` column

### Rate limiting too aggressive
**Fix**: Adjust time window in `check_rate_limit()` function

### OTP emails not sending
**Fix**: Check Auth0 passwordless email configuration

---

## 📋 Production Deployment Checklist

### Before Going Live
- [ ] Test both authentication methods
- [ ] Verify all mentor emails are in database
- [ ] Configure proper error monitoring
- [ ] Set up backup authentication method
- [ ] Document emergency access procedures

### Communication to Mentors
```
Subject: New Login Options Available - Project TYRA

Dear Mentors,

We've enhanced the security of our mentor dashboard with two login options:

1. **Verification Code** (same as before)
   - Use your existing verification code

2. **Email Login** (new option)
   - Enter your registered email
   - Receive a 6-digit code instantly
   - More convenient for future access

Both methods provide the same secure access to your dashboard.

Best regards,
Project TYRA Team
```

---

## 📈 Monitoring & Maintenance

### Daily Checks
- Monitor authentication success rates
- Check for security alerts in logs
- Verify email delivery rates

### Weekly Tasks
- Review failed authentication attempts
- Update mentor email database as needed
- Check Auth0 usage metrics

### Monthly Tasks
- Security review of authentication logs
- Update documentation if needed
- Mentor feedback collection

---

## 🎯 Success Metrics

Track these metrics to measure deployment success:

- **Authentication Success Rate**: Target >95%
- **User Preference**: Email vs Code usage ratio
- **Security Incidents**: Target 0 successful attacks
- **User Satisfaction**: Feedback score >4.5/5

---

## 🔄 Rollback Plan

If issues occur:

1. **Immediate**: Switch back to original app
   ```bash
   cp app_backup.py app_matching_confirmation_round_1.py
   ```

2. **Investigate**: Check logs and error reports

3. **Fix**: Address issues in enhanced version

4. **Redeploy**: When ready, switch back to enhanced version

---

## 📞 Emergency Contacts

- **Technical Issues**: System Administrator
- **Security Concerns**: Security Team (immediate)
- **Auth0 Issues**: Auth0 Support Dashboard
- **Mentor Complaints**: Project TYRA Support Team

---

**Ready to deploy? Follow steps 1-5 and you'll have dual authentication running in 15 minutes! 🚀**
