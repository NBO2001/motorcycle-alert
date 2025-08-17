# Motorcycle Alert System

A Domain-Driven Design (DDD) application for monitoring motorcycle status and sending alerts via Telegram when status changes occur.

## Features

- **Real-time Monitoring**: Continuously monitors motorcycle status from external API
- **Telegram Notifications**: Sends formatted alerts when status changes
- **Secure Configuration**: No hardcoded tokens or sensitive data
- **Clean Architecture**: Follows DDD principles with proper separation of concerns
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Graceful Shutdown**: Handles shutdown signals properly

## Architecture

The application follows Domain-Driven Design principles:

```
motorcycle_alert/
├── domain/           # Core business logic
│   ├── models.py     # Domain entities (MotorcycleStatus, AlertMessage)
│   └── services.py   # Domain services and abstractions
├── application/      # Use cases and application logic
│   └── use_cases.py  # Monitoring use case
└── infrastructure/   # External concerns
    ├── api_client.py     # HTTP API integration
    ├── storage.py        # File-based storage
    ├── notifications.py  # Telegram integration
    └── config.py         # Configuration management
```

## Security Improvements

- **Environment Variables**: All sensitive data moved to environment variables
- **No Hardcoded Tokens**: API keys, cookies, and tokens must be provided via environment
- **Validation**: Configuration validation ensures required variables are present
- **Separation of Concerns**: Infrastructure details separated from business logic

## Setup

### 1. Install Dependencies

```bash
poetry install
```

### 2. Configure Environment Variables

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your actual values:

```env
# Telegram Configuration
TELEGRAM_API_KEY=your_telegram_bot_api_key_here
TELEGRAM_USER_ID=your_telegram_user_id_here

# API Configuration
API_BASE_URL=https://servidormapa.com
OBJECT_ID=your_object_id_here
API_COOKIE=your_api_cookie_here
API_CSRF_TOKEN=your_api_csrf_token_here

# Application Configuration
CHECK_INTERVAL=60
STATUS_FILE_PATH=status.txt
```

### 3. Get Required Credentials

#### Telegram Bot
1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Get your bot's API key
3. Get your Telegram user ID (use [@userinfobot](https://t.me/userinfobot))

#### API Credentials
1. Log into the motorcycle tracking website
2. Open browser developer tools (F12)
3. Go to Network tab and make a request
4. Copy the `Cookie` header value for `API_COOKIE`
5. Copy the `X-CSRF-TOKEN` header value for `API_CSRF_TOKEN`

## Usage

### Run the Application

```bash
python main.py
```

### Run with Custom Parameters

```bash
python main.py --check-interval 30 --status-file /tmp/status.txt
```

### Development Commands

Format code:
```bash
make format
```

Run linting:
```bash
make lint
```

Run tests:
```bash
make test
```

Run all checks:
```bash
make format && make lint && make test
```

## Configuration Options

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `TELEGRAM_API_KEY` | Telegram bot API key | Required |
| `TELEGRAM_USER_ID` | Your Telegram user ID | Required |
| `API_BASE_URL` | Base URL for motorcycle API | `https://servidormapa.com` |
| `OBJECT_ID` | Motorcycle object ID | `your_object_id_here` |
| `API_COOKIE` | Cookie header for API authentication | Required |
| `API_CSRF_TOKEN` | CSRF token for API requests | Required |
| `CHECK_INTERVAL` | Check interval in seconds | `60` |
| `STATUS_FILE_PATH` | Path to status persistence file | `status.txt` |

## Domain Models

### MotorcycleStatus
Represents the current state of the motorcycle:
- `icon_color`: Visual indicator color
- `alimentation`: Power supply status
- `blocked`: Whether the motorcycle is blocked
- `ignition`: Ignition status
- `time`: Last update time
- `stop_duration`: Duration stopped
- `speed`: Current speed
- `additional_sensors`: Any other sensor data

### AlertMessage
Formatted notification message containing:
- `status`: The motorcycle status
- `timestamp`: When the alert was generated

## Logging

The application logs to both console and `motorcycle_alert.log` file:
- `INFO`: General application flow
- `DEBUG`: Detailed debugging information
- `ERROR`: Error conditions
- `WARNING`: Warning conditions

## Error Handling

- **Configuration Errors**: Application fails fast if required environment variables are missing
- **API Errors**: HTTP errors are logged and re-raised
- **File Errors**: Storage errors are handled gracefully
- **Network Errors**: Temporary network issues are logged and retried on next cycle

## Contributing

1. Follow the existing DDD architecture
2. Add tests for new functionality
3. Ensure all make commands pass
4. Update documentation as needed

## License

This project is licensed under the MIT License.