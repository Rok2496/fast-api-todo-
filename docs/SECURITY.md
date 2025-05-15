# Security Considerations

This document outlines the security measures implemented in the FAST TODO API and provides recommendations for securing your deployment.

## Current Security Measures

### Authentication

1. **Password Hashing**
   - Passwords are hashed using bcrypt with salt
   - No plaintext passwords are stored

2. **JWT Authentication**
   - JSON Web Tokens (JWT) for stateless authentication
   - Short expiry time (60 minutes by default)
   - Secret key should be kept secure

3. **Two-Factor Authentication (2FA)**
   - Time-based One-Time Password (TOTP) implementation
   - Compatible with standard authenticator apps (Google Authenticator, Authy, etc.)
   - 2FA secrets are stored securely in the database

4. **One-Time Login Codes**
   - Secure random 6-digit codes for passwordless login
   - Codes have a short expiry time (10 minutes)
   - Limited to one use only

### API Security

1. **Input Validation**
   - All inputs are validated using Pydantic schemas
   - Type checking and constraint validation

2. **Database Security**
   - Parameterized queries to prevent SQL injection
   - SQLAlchemy ORM for secure database interactions

3. **CORS Configuration**
   - Cross-Origin Resource Sharing (CORS) middleware
   - Should be restricted to trusted domains in production

### Google Calendar Integration

1. **OAuth 2.0 Flow**
   - Industry-standard OAuth 2.0 for Google API authentication
   - Only stores refresh tokens, not access tokens
   - Uses the minimal required permissions (scopes)

2. **State Parameter**
   - Prevents CSRF attacks during OAuth flow
   - Contains user ID for secure callback processing

## Security Recommendations for Production

### Environment Variables

1. **Change Default Values**
   - Use strong, unique values for all secrets
   - Do not rely on default values

2. **Secure Storage**
   - Use a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault)
   - Do not store secrets in code or source control

### API Protection

1. **Rate Limiting**
   - Implement rate limiting for all endpoints
   - Special attention to authentication endpoints

2. **HTTPS**
   - Always use HTTPS in production
   - Configure proper SSL/TLS certificates

3. **CORS Configuration**
   - Restrict to specific origins
   - Update the CORS settings in main.py:
     ```python
     app.add_middleware(
         CORSMiddleware,
         allow_origins=["https://your-frontend-domain.com"],
         allow_credentials=True,
         allow_methods=["*"],
         allow_headers=["*"],
     )
     ```

### JWT Configuration

1. **Secure Secret Key**
   - Use a strong, randomly generated secret key
   - Rotate keys periodically

2. **JWT Settings**
   - Consider reducing token expiry time
   - Implement refresh token mechanism if needed

### Database Security

1. **Limited Privileges**
   - Database user should have minimum required permissions
   - Different users for different environments

2. **Database Encryption**
   - Enable at-rest encryption for database
   - Use SSL/TLS for database connections

### Email Security

1. **SPF and DKIM**
   - Configure proper email authentication
   - Prevent email spoofing

2. **Secure SMTP**
   - Use TLS for SMTP connections
   - Use application-specific passwords or OAuth for SMTP authentication

### Monitoring and Logging

1. **Security Logging**
   - Log authentication attempts (successful and failed)
   - Log sensitive operations

2. **Intrusion Detection**
   - Monitor for suspicious activities
   - Implement alerting for security events

## Security Vulnerability Reporting

If you discover a security vulnerability, please do not disclose it publicly. Instead, send details to security@example.com.

We take security seriously and will respond to verified reports as quickly as possible. 