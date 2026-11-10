# Career-wise Required Skills

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


# Personalized Skill Recommendations

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
        "Learn Java programming, OOP concepts and practice coding.",

    "git":
        "Learn Git commands and practice version control.",

    "html":
        "Learn HTML structure, forms and semantic elements.",

    "css":
        "Learn CSS styling, layouts and responsive design.",

    "javascript":
        "Learn JavaScript basics, functions and DOM manipulation.",

    "react":
        "Learn React components, props, state and basic projects.",

    "machine learning":
        "Learn Machine Learning fundamentals and practice projects.",

    "pandas":
        "Learn Pandas for data cleaning and data analysis."
}


# Function to find Skill Gap

def find_skill_gap(student_skills, required_skills):

    student_skills = set(student_skills)

    required_skills = set(required_skills)

    missing_skills = required_skills - student_skills

    return list(missing_skills)


# Display Available Careers

print("Available Careers:")

for career in career_skills:

    print("-", career)


# Get Career from User

career = input("\nEnter your career: ").strip().title()


# Check Career

if career in career_skills:

    # Get required skills
    required_skills = career_skills[career]

    print("\nRequired Skills:")
    print(required_skills)


    # Get Student Skills

    skills_input = input(
        "\nEnter your skills separated by comma: "
    )

    student_skills = [
        skill.strip().lower()
        for skill in skills_input.split(",")
    ]


    # Find Skill Gap

    missing_skills = find_skill_gap(
        student_skills,
        required_skills
    )


    # Display Student Skills

    print("\nStudent Skills:")
    print(student_skills)


    # Display Missing Skills

    print("\nMissing Skills:")

    if missing_skills:

        for skill in missing_skills:

            print("-", skill)

    else:

        print("No skill gap. You have all required skills!")


    # Personalized Recommendations

    print("\nPersonalized Skill Recommendations:")

    if missing_skills:

        for skill in missing_skills:

            if skill in skill_recommendations:

                print(
                    "-",
                    skill,
                    ":",
                    skill_recommendations[skill]
                )

            else:

                print(
                    "-",
                    skill,
                    ": Learn this skill and practice with projects."
                )

    else:

        print(
            "You have all the required skills. Keep improving them!"
        )


else:

    print("\nCareer not found.")
    print("Please enter a career from the available list.")