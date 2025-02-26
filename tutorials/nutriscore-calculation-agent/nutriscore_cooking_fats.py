
def get_nutriscore_cooking_fat_score(sat_fat_g: int, total_fat_g: int) -> str:
    """Calculates the Nutri-Score for cooking fats.

    Args:
        sat_fat_g (int): Saturated fat content in grams.
        total_fat_g (int): Total fat content in grams.

    Returns:
        str: The calculated Nutri-Score for cooking fats.
    """
    if total_fat_g == 0:
        score = 0  
    else:
        ratio = (sat_fat_g / total_fat_g) * 100  
        thresholds = [10,16,22,28,34,40,46,52,58,64]
        score = None
        for i, t in enumerate(thresholds):
            if ratio <= t:
                score = i
                break
        if score is None:
            score = 10
    thresholds = [-1, 2, 10, 18]
    labels = ['A', 'B', 'C', 'D', 'E']
    nutriscore = next((label for t, label in zip(thresholds, labels) if score <= t), 'E')
    return nutriscore