def calculate_target_cgpa(current_cgpa, completed_credits,
                          target_cgpa, future_credits):

    if future_credits <= 0:
        raise ValueError("Future credits must be greater than zero.")

    required_gp = (
        target_cgpa * (completed_credits + future_credits)
        - current_cgpa * completed_credits
    ) / future_credits

    # Target is not possible
    if required_gp > 4.00:
        return None

    return round(max(required_gp, 0.00), 2)