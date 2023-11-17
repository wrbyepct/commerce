import os
from dotenv import load_dotenv

load_dotenv()
UPSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')

LISTING_NOT_UNIQUE = "You have created a listing with the same title and category. Please ensure they are unique."

COMMENT_SAVE_ERROR = "Failed to save a commnet instance"