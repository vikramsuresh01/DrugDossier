from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb+srv://vs7552:drugdossier@drugdossier.09fff1b.mongodb.net/user_info?retryWrites=true&w=majority")

# Access the database
db2 = client.substances

# Access the collection
collection2 = db2.narcotics

# Define the document to insert
drug_data = {
     "drug_name": "Lysergic acid diethylamide (LSD)",
        "description": "A powerful hallucinogenic drug known for its profound effects on perception and consciousness.",
        "category": "Hallucinogen",
        "chemical_structure": "Lysergic acid diethylamide",
        "route_of_administration": ["Oral", "Sublingual (under the tongue)"],
        "effects": {
            "physiological": ["Dilated pupils", "Increased heart rate", "Increased body temperature"],
            "psychological": ["Altered perception of reality", "Hallucinations", "Intense emotional experiences"]
        },
        "risks_and_side_effects": {
            "short_term": ["Panic", "Paranoia", "Flashbacks", "Anxiety"],
            "long_term": ["Hallucinogen persisting perception disorder (HPPD)", "Psychological dependence"]
        },
        "legal_status": "Illegal in most countries; classified as a Schedule I controlled substance",
        "dosage_and_usage_guidelines": {
            "dosage_forms": ["Blotter paper", "Microdots", "Liquid"],
            "dosage_ranges": {
                "Oral": "20-200 micrograms per dose"
            },
            "usage_guidelines": "Use with extreme caution; can produce profound and unpredictable effects."
        },
        "history_and_origin": "Synthesized in the 1930s and later popularized as a recreational drug during the counterculture movement of the 1960s.",
        "availability_and_distribution": "Manufactured and distributed illicitly; often found in underground markets and among certain subcultures.",
        "medical_uses": "Research suggests potential therapeutic uses in treating certain mental health conditions, but more research is needed due to legal restrictions."
}


# Insert the document into the collection
collection2.insert_one(drug_data)

print("Data inserted successfully.")