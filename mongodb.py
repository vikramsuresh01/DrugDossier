from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://vs7552:drugdossier@drugdossier.09fff1b.mongodb.net/user_info?retryWrites=true&w=majority")

# Access the database
db3 = client.substances

# Access the collection
collection2 = db3.supplements

# Define the document to insert
drug_data = {
    "supplement_name": "Vitamin B12",
    "description": "Vitamin B12, also known as cobalamin, is a water-soluble vitamin essential for red blood cell formation, neurological function, and DNA synthesis.",
    "category": "Dietary Supplement",
    "chemical_components": ["Cyanocobalamin", "Methylcobalamin", "Hydroxocobalamin"],
    "source": "Found naturally in animal products such as meat, fish, eggs, and dairy. Also available in fortified foods and dietary supplements.",
    "benefits": {
        "physiological": ["Supports red blood cell production and prevents anemia", "Maintains neurological function"],
        "energy": ["May help alleviate fatigue and promote energy production"]
    },
    "risks_and_side_effects": {
        "short_term": ["Nausea", "Vomiting", "Diarrhea"],
        "long_term": ["Risk of hypervitaminosis (excessive intake) with very high doses"]
    },
    "dosage_and_usage_guidelines": {
        "dosage_forms": ["Tablets", "Sublingual tablets", "Sprays"],
        "dosage_ranges": {
            "General Health": "2.4 mcg per day for most adults",
            "Deficiency Treatment": "Higher doses (up to 1000 mcg or more) for individuals with deficiency under medical supervision"
        },
        "usage_guidelines": "Take as directed by a healthcare professional. Sublingual forms may be absorbed more effectively for individuals with absorption issues."
    },
    "availability_and_distribution": "Available over-the-counter in pharmacies, health food stores, and online.",
    "medical_uses": "Used as a dietary supplement to prevent and treat vitamin B12 deficiency and support red blood cell production and neurological function."
}




# Insert the document into the collection
collection2.insert_one(drug_data)

print("Data inserted successfully.")