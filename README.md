## AI Insights - Sentiment Analysis

AI Insights is a project aimed at measuring public sentiment towards AI topics using Twitter as the dataset. The project leverages a microservices architecture to collect, analyze, and display sentiment data.

### Features

- **Microservices Architecture**: Decoupled services for data collection, analysis, and presentation.
- **Message Queue**: Uses RabbitMQ to handle communication between services.
- **CI/CD Pipeline**: Automated deployment using GitHub Actions.
- **Containerization**: Services are containerized using Docker and orchestrated with Docker Compose.
- **Data Visualization**: Utilizes D3.js for interactive charts and visualizations.

### Technologies Used

- **Python**: The primary programming language.
- **Flask**: For building the web service and API.
- **SQLAlchemy**: ORM for database interaction.
- **Flask-Smorest**: For creating REST APIs.
- **Marshmallow**: For object serialization and deserialization.
- **D3.js**: For data visualization.
- **RabbitMQ**: For message queuing between services.
- **Docker**: To containerize the application.
- **Docker Compose**: For container orchestration.
- **GitHub Actions**: For continuous integration and deployment.
- **AWS EC2**: Hosting the application.
- **Google Cloud Natural Language API**: For sentiment analysis.
- **PostgreSQL**: Database for storing tweet data.

### Microservices

- **Data Collector Service**: 
  - Reaches out to the Twitter API and pulls in recent tweets related to AI.
  - Sends the tweets to a RabbitMQ message queue.

- **Data Analyzer Service**:
  - Receives tweets from RabbitMQ.
  - Uses Google Cloud Natural Language Processing service to analyze the sentiment.
  - Persists analyzed tweets to a PostgreSQL database.

- **Web Service**:
  - A Flask app providing the backend API.
  - Uses Flask, SQLAlchemy, Flask-Smorest, and Marshmallow.
  - Serves static content utilizing D3.js for visualizations.

### Production Environment

The services are containerized using Docker, with Docker Compose for orchestration. GitHub Actions handles the CI/CD pipeline, deploying the containerized application to an AWS EC2 Ubuntu instance. This setup ensures seamless updates and scalability.

### Live Demo

You can view the live version of the project [here](https://ai.stephenkilgore.com).

### GitHub Repository

The source code for AI Insights is available on GitHub. Feel free to explore the repository, open issues, or contribute to the project [here](https://github.com/StephenKilgore/ai-insights).

This project demonstrates the effective use of a microservices architecture, message queuing, and modern DevOps practices including CI/CD and containerization.
