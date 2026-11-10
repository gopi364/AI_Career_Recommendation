import os
import json
import math


# Skills used by the model

skills = [
    "python",
    "sql",
    "excel",
    "power bi",
    "statistics",
    "java",
    "git",
    "html",
    "css",
    "javascript",
    "react",
    "machine learning",
    "pandas"
]


# Training data

training_data = [

    # Data Analyst
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],

    # Software Developer
    [1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0],

    # Data Scientist
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1],

    # Web Developer
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0]
]


# Career labels

career_labels = [
    "Data Analyst",
    "Data Analyst",
    "Data Analyst",
    "Data Analyst",

    "Software Developer",
    "Software Developer",
    "Software Developer",
    "Software Developer",

    "Data Scientist",
    "Data Scientist",
    "Data Scientist",
    "Data Scientist",

    "Web Developer",
    "Web Developer",
    "Web Developer",
    "Web Developer"
]


# Calculate centroid for every career

centroids = {}

for career in set(career_labels):

    career_records = []

    for i in range(len(training_data)):

        if career_labels[i] == career:
            career_records.append(training_data[i])

    centroid = []

    for column in range(len(skills)):

        total = 0

        for record in career_records:
            total += record[column]

        average = total / len(career_records)

        centroid.append(average)

    centroids[career] = centroid


# Save trained model

os.makedirs("model", exist_ok=True)

model = {
    "skills": skills,
    "centroids": centroids
}

model_path = "model/career_model.json"

with open(model_path, "w") as file:
    json.dump(model, file, indent=4)


print("Model training completed successfully!")
print("Model type: Nearest Centroid Classifier")
print("Model saved at:", model_path)
print("Number of training records:", len(training_data))
print("Number of careers:", len(set(career_labels)))