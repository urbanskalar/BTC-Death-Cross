# BTC-Death-Cross

This project detects the upcoming Bitcoin (BTC) Death Cross and sends notifications via [ntfy.sh](https://ntfy.sh). A Death Cross occurs when the 50-day moving average (MA) crosses below the 200-day MA, often interpreted as a bearish market signal. The script can also predict a Death Cross a few days in advance.​

## Features

- **Daily Monitoring**: Automatically checks for Death Cross occurrences.
- **Advance Prediction**: Forecasts potential Death Cross events up days ahead.
- **Notifications**: Sends alerts via [ntfy.sh](https://ntfy.sh) when a Death Cross is detected or predicted.
- **Dockerized**: Easily deployable using Docker and Docker Compose.
- **Cron Integration**: Scheduled execution using cron within the Docker container.
- **Backtesting**: Supports backtesting by specifying a historical date.​

---

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository**:
```
git clone <https://github.com/urbanskalar/BTC-Death-Cross.git>
cd BTC-Death-Cross
```
2. **Set up `ntfy.sh`**:

Ensure you have a topic set up on [ntfy.sh](https://ntfy.sh). Replace the NTFY_TOPIC in deathCross.py with your chosen topic name.

3. **Build and run the Docker container**:
```
docker-compose up --build -d
```

This command builds the Docker image and starts the container in detached mode.

---

## Usage

### Daily Execution

The script is scheduled to run daily at 8:00 AM UTC inside the Docker container using cron.​

### Manual Execution

To run the script manually inside the container:​

docker exec -it btc_death_cross python3 /app/deathCross.py

### Backtesting

To perform a backtest for a specific date:​
```
docker exec -it btc_death_cross python3 /app/deathCross.py --date YYYY-MM-DD
```
Replace YYYY-MM-DD with the desired date.​

---

## Project Structure
```
BTC-Death-Cross/
├── Dockerfile # Defines the Docker image
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt # Python dependencies
├── deathCross.py # Main script for detecting Death Cross
├── crontab # Cron schedule configuration
└── README.md # Project documentation
```

---

## Configuration
- **NTFY_TOPIC**: Set your ntfy.sh topic in deathCross.py.
- **ADVANCE_NOTICE_DAYS**: Number of days in advance to predict a Death Cross (default is 3).
- **SYMBOL**: The trading pair symbol to monitor (default is BTC-USD).​
