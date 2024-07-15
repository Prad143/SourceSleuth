# SourceSleuth: Innovative Product Exploration Tool

SourceSleuth is an advanced tool designed to explore various online platforms and uncover cutting-edge B2B products. By leveraging multiple data sources and intelligent processing, SourceSleuth provides valuable insights into emerging technologies and innovative solutions.

## Table of Contents

- [Features](#features)
- [Data Sources](#data-sources)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- Multi-source data extraction from various platforms
- Intelligent B2B product filtering using AI
- Real-time data processing and storage
- Scalable architecture using Apache Kafka and MongoDB
- Automated scraping and data collection

## Data Sources

SourceSleuth extracts data from the following platforms:

1. **G2.com**: Primary source for existing B2B products
2. **BetaList**: Emerging startups and innovations
3. **TechCrunch**: In-depth articles on startups and tech trends
4. **Reddit**: Discussions on technology and startups5.
5. **Product Hunt**: Trending products across diverse categories

## Architecture

SourceSleuth uses a distributed architecture for efficient data processing:

1. **Data Extraction**: Multiple scrapers collect data from various sources
2. **Apache Kafka**: Handles real-time data streaming between components
3. **AI Processing**: Uses Google's Gemini AI for B2B classification and information extraction
4. **MongoDB**: Stores processed B2B product information

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/SourceSleuth.git
cd SourceSleuth
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Set up environment variables:
   Create a `.env` file in the project root and add the following variables:
```
KAFKA_BOOTSTRAP_SERVERS=your_kafka_servers
KAFKA_USERNAME=your_kafka_username
KAFKA_PASSWORD=your_kafka_password
MONGODB_URI=your_mongodb_uri
MONGODB_DB_NAME=your_db_name
MONGODB_COLLECTION_NAME=your_collection_name
API_ENDPOINT=your_g2_api_endpoint
API_KEY=your_g2_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=your_reddit_user_agent
GOOGLE_API_KEY=your_google_api_key
```




## Usage

To run SourceSleuth:
```
python main.py
```


This will start the main process, which includes:

1. G2.com data extraction
2. Running various scrapers (BetaList, TechCrunch, Reddit, Product Hunt)
3. Processing data through Kafka
4. Storing B2B products in MongoDB

## Configuration

You can configure various aspects of SourceSleuth in the `config.py` file:
```
import os
from dotenv import load_dotenv
load_dotenv()
KAFKA_CONFIG = {
'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
'security.protocol': 'SASL_SSL',
'sasl.mechanisms': 'PLAIN',
'sasl.username': os.getenv('KAFKA_USERNAME'),
'sasl.password': os.getenv('KAFKA_PASSWORD')
}
MONGODB_URI = os.getenv('MONGODB_URI')
MONGODB_DB_NAME = os.getenv('MONGODB_DB_NAME')
MONGODB_COLLECTION_NAME = os.getenv('MONGODB_COLLECTION_NAME')
API_ENDPOINT = os.getenv('API_ENDPOINT')
API_KEY = os.getenv('API_KEY')
KAFKA_TOPIC_API = 'api_product_data'
KAFKA_TOPIC_BETALIST = 'betalist_product_data'
KAFKA_TOPIC_MISC = 'misc_product_data'
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
```

## Contributing

Contributions to SourceSleuth are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-branch-name`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

SourceSleuth empowers businesses to stay ahead of the curve by providing a comprehensive view of the B2B product landscape. By leveraging multiple data sources and intelligent processing, it offers valuable insights into emerging technologies and innovative solutions.

> [!NOTE]
> This project is currently in active development. Features and documentation may change frequently.

