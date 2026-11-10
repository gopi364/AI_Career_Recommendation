from flask import Flask, render_template, request
import json
import math

app = Flask(__name__)


# Load trained career model

with open("model/career_model.json", "r") as file:
    model = json.load(file)


skills = model["skills"]
centroids = model["centroids"]


# Career-wise required skills

career_skills = {

    "Data Analyst": [
        "python",
        "sql",
        "excel",
        "power bi",
        "statistics"
    ],

    "Software Developer": [
        "java",
        "python",
        "sql",
        "git",
        "html",
        "css"
    ],

    "Data Scientist": [
        "python",
        "sql",
        "statistics",
        "machine learning",
        "pandas"
    ],

    "Web Developer": [
        "html",
        "css",
        "javascript",
        "react",
        "git"
    ]
}


# Personalized recommendations

skill_recommendations = {

    "python":
        "Learn Python fundamentals and practice coding problems.",

    "sql":
        "Learn SQL queries, joins, grouping and database operations.",

    "excel":
        "Learn Excel formulas, Pivot Tables and data analysis.",

    "power bi":
        "Learn Power BI and practice creating interactive dashboards.",

    "statistics":
        "Learn basic statistics, probability and data analysis.",

    "java":
        "Learn Java programming and OOP concepts.",

    "git":
        "Learn Git commands and version control.",

    "html":
        "Learn HTML structure and forms.",

    "css":
        "Learn CSS styling and responsive design.",

    "javascript":
        "Learn JavaScript basics and DOM manipulation.",

    "react":
        "Learn React components, props and state.",

    "machine learning":
        "Learn Machine Learning fundamentals and practice projects.",

    "pandas":
        "Learn Pandas for data cleaning and analysis."
}


# Predict career using Nearest Centroid Classifier

def predict_career(student_skills):

    student_vector = []

    for skill in skills:

        if skill in student_skills:
            student_vector.append(1)
        else:
            student_vector.append(0)


    best_career = None
    best_distance = float("inf")


    for career, centroid in centroids.items():

        distance = 0

        for i in range(len(student_vector)):

            difference = student_vector[i] - centroid[i]

            distance += difference ** 2

        distance = math.sqrt(distance)


        if distance < best_distance:

            best_distance = distance
            best_career = career


    return best_career


# Home page

@app.route("/", methods=["GET", "POST"])
def home():

    result = None


    if request.method == "POST":

        skills_input = request.form["skills"]


        # Convert entered skills into a list

        student_skills = [

            skill.strip().lower()

            for skill in skills_input.split(",")

            if skill.strip()
        ]


        # ML Career Prediction

        predicted_career = predict_career(student_skills)


        # Required skills for predicted career

        required_skills = career_skills[predicted_career]


        # Find missing skills

        missing_skills = [

            skill

            for skill in required_skills

            if skill not in student_skills
        ]


        # Calculate career match percentage

        matched_skills = len(required_skills) - len(missing_skills)

        if len(required_skills) > 0:

            match_percentage = round(
                (matched_skills / len(required_skills)) * 100
            )

        else:

            match_percentage = 0


        # Personalized recommendations

        recommendations = []


        for skill in missing_skills:

            if skill in skill_recommendations:

                recommendations.append(
                    skill_recommendations[skill]
                )


        # Final result

        result = {

            "career": predicted_career,

            "match_percentage": match_percentage,

            "student_skills": student_skills,

            "required_skills": required_skills,

            "missing_skills": missing_skills,

            "recommendations": recommendations
        }


    return render_template(

        "index.html",

        careers=career_skills.keys(),

        result=result
    )


if __name__ == "__main__":

    app.run(debug=True)