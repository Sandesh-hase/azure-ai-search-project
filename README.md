# Azure AI Search Crash Course

This project is a crash course on using Azure AI Search to build intelligent search applications. The course demonstrates how to integrate Azure Cognitive Search with a Python Flask application to create a powerful and customizable search experience.

## Features
- **Flask Web Application**: A lightweight web framework for building the search interface.
- **Azure Cognitive Search Integration**: Leverage Azure's powerful search capabilities, including filtering, sorting, and faceted navigation.
- **Environment Configuration**: Use `.env` files to securely manage sensitive credentials.
- **Customizable Search Queries**: Modify search parameters such as filters, sort orders, and facets.

## Prerequisites
1. **Azure Subscription**: Ensure you have an active Azure subscription.
2. **Azure Cognitive Search Service**: Set up a search service in the Azure portal.
3. **Python Environment**: Install Python 3.8 or later.
4. **Dependencies**: Install required Python packages using `pip install -r requirements.txt`.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd AI-Search-Crash-Course/code
   ```
2. Create a `.env` file in the project root and add the following variables:
   ```env
   SEARCH_SERVICE_ENDPOINT=<your-search-service-endpoint>
   SEARCH_SERVICE_QUERY_KEY=<your-query-key>
   SEARCH_INDEX_NAME=<your-index-name>
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```

## File Structure
- `app.py`: Main Flask application file.
- `templates/`: HTML templates for the web interface.
- `static/`: Static assets like CSS and images.
- `requirements.txt`: Python dependencies.
- `.env`: Environment variables for Azure Cognitive Search credentials.

## Learn More
- [Azure Cognitive Search Documentation](https://learn.microsoft.com/en-us/azure/search/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## License
This project is licensed under the MIT License.