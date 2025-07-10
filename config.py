import os
cloudant_config = {
    "username": os.getenv("CLOUDANT_USERNAME"),
    "apikey": os.getenv("CLOUDANT_APIKEY"),
    "url": "https://<your-cloudant-username>.cloudantnosqldb.appdomain.cloud",  # Replace with your actual Cloudant URL
    "dbname": "tasks"
}