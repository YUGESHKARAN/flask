from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)

CORS(app, supports_credentials=True)

# Global variable to store the DataFrame
global_df = None

# Load secrets from a local JSON file
# def load_secrets(file_path):
#     """Function to load secrets from a JSON file."""
#     try:
#         with open(file_path, 'r') as f:
#             return json.load(f)
#     except FileNotFoundError:
#         print(f"Error: {file_path} not found.")
#         return None
#     except json.JSONDecodeError:
#         print("Error: Failed to decode JSON from the file.")
#         return None

# Function to convert DynamoDB items from Decimal to float
# def convert_dynamodb_items(items):
#     """Recursively convert Decimal values in DynamoDB items to float."""
#     if isinstance(items, list):
#         return [convert_dynamodb_items(item) for item in items]
#     elif isinstance(items, dict):
#         return {k: convert_dynamodb_items(v) for k, v in items.items()}
#     elif isinstance(items, Decimal):
#         return float(items)
#     else:
#         return items
    
@app.route('/', methods=['GET'])
def home_page():
   return "Welocme to home egg"

@app.route('/product-analysis', methods=['GET'])
def sales_prediction():
    global global_df  # Declare the global DataFrame variable
    
    # Load secrets from the secrets.json file
    # secrets = load_secrets('secrets.json')  # Ensure 'secrets.json' is in the same directory
    
    # if secrets is None:
    #     return jsonify({"error": "Could not load secrets from the JSON file"}), 500

    # # Extract the credentials and region from the secrets file
    # aws_access_key = secrets.get('aws_access_key_id')
    # aws_secret_key = secrets.get('aws_secret_access_key')
    # region = secrets.get('region', 'us-east-1')  # Default to 'us-east-1' if region is not provided

    try:
        # Initialize DynamoDB client with loaded credentials
        # dynamodb_client = boto3.resource(
        #     'dynamodb',
        #     region_name=region,
        #     aws_access_key_id=aws_access_key,
        #     aws_secret_access_key=aws_secret_key
        # )
        
        # # Access the DynamoDB table
        # table = dynamodb_client.Table('egg_product')
        # response = table.scan()
        # items = response['Items']

        # # Convert items to a pandas DataFrame
        # items_serializable = convert_dynamodb_items(items)
        # df1 = pd.DataFrame(items_serializable)
        df = pd.read_csv('egg-csv.csv')

        # fetching category name and its count
        category=df.groupby(['category']).size().reset_index(name='Count')

        # fetching sub category and its count
        subcategory=df.groupby(['subCategory']).size().reset_index(name='Count')

        # product name & count - broiler
        broiler=df.loc[df['subCategory'] == 'Broiler Chicken Meat', ['productName','price']]

        # product name & count - country chicken
        country=df.loc[df['subCategory'] == 'Country Chicken Meat',['productName','price']]

        #name & count egg
        egg=df.loc[df['subCategory'] == 'White Egg', ['productName','price']]

        #name & count country egg
        country_egg=df.loc[df['subCategory'] == 'Country Egg',['productName','price']]
       
       #name & count egg liquids
        liquids=df.loc[df['subCategory'] == 'Egg Liquids', ['productName','price']]

        response_data = {
            'category_analysis':{
                'category':category.to_dict(orient='records'),
                'subcategory':subcategory.to_dict(orient='records')
            },
            'product_analysis':{
                'broiler':broiler.to_dict(orient='records'),
                'country':country.to_dict(orient='records'),
                'egg':egg.to_dict(orient='records'),
                'country_egg':country_egg.to_dict(orient='records'),
                'liquids':liquids.to_dict(orient='records'),
            }
        }

        return jsonify(response_data), 200 
   
    except Exception as e:
        print(f"Error accessing DynamoDB: {e}")
        return jsonify({"error": f"Error accessing DynamoDB: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
