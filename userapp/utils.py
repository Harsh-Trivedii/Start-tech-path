def user_eligible(user_profile, job):
    # Check experience
    if job.experience and user_profile.experience != job.experience:
        print(f"Experience check failed: {user_profile.experience} != {job.experience}")
        return False

    # Check passing year
    if job.passing_year and user_profile.year != job.passing_year:
        print(f"Passing year check failed: {user_profile.year} != {job.passing_year}")
        return False

    # Check grade
    if job.grade:
        # Extract the numeric value from job.grade (e.g., '>70%' -> 70)
        job_grade_value = int(job.grade.strip('>%'))

        # Convert user_profile.grade to an integer for comparison
        user_profile_grade = int(user_profile.grade.strip('>%'))
        
        # Compare the values
        if user_profile_grade < job_grade_value:
            print(f"Grade check failed: {user_profile.grade} < {job_grade_value}")
            return False

    # Additional custom checks can be added

    # If all checks pass, the user is eligible
    return True
