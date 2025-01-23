# FastAPI Application

This is a FastAPI application that provides APIs for managing activities, incidents, maintenance, services, and public pages.

## Setup

Follow these steps to set up and run the application:

### Prerequisites

- Python 3.10 or higher
- MongoDB
- pip (Python package installer)

### Installation

1. Clone the repository:

    ```sh
    git clone <https://github.com/AkshatSinghRajput/plivo-backend>
    cd plivo-backend
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required packages:

    ```sh
    pip install -r requirements.txt
    ```

5. Set up environment variables:

    Create a [.env] file in the root directory and add the following variables:

    ```env
    CLERK_PUBLISHABLE_KEY=<your-clerk-publishable-key>
    CLERK_SECRET_KEY=<your-clerk-secret-key>
    CLERK_FRONTEND_API=<your-clerk-frontend-api>
    DATABASE_URL=<your-database-url>
    SIGNING_SECRET=<your-signing-secret>
    ```

### Running the Application

1. Start the FastAPI application:

    ```sh
    python run.py
    ```

2. The application will be available at `http://0.0.0.0:8000`.

### API Documentation

You can access the API documentation at `http://0.0.0.0:8000/docs`.

## Logging

Logs are configured to be written to [app.log](http://_vscodecontentref_/2) and also displayed in the console.

## License

This project is licensed under the MIT License
