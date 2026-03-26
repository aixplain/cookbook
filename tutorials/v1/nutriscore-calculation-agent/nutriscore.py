def get_nutriscore(
    energy_kcal: float, sugars_g: float, sat_fat_g: float, salt_mg: float, 
    fruit_veg_percent: float, fibre_g: float, protein_g: float
) -> str:
    """Calculates the Nutri-Score for food items (excluding beverages and cooking fats).

    The Nutri-Score is a health-based food rating that considers negative (unhealthy) 
    and positive (healthy) nutritional factors. A lower score indicates a healthier food.

    Negative points are assigned based on high energy, sugar, saturated fat, and salt content.
    Positive points are assigned based on fruit/vegetable percentage, fiber, and protein content.

    Args:
        energy_kcal (float): Energy content in kilocalories.
        sugars_g (float): Sugar content in grams.
        sat_fat_g (float): Saturated fat content in grams.
        salt_mg (float): Salt content in milligrams.
        fruit_veg_percent (float): Percentage of fruit and vegetables in the food.
        fibre_g (float): Fiber content in grams.
        protein_g (float): Protein content in grams.

    Returns:
        str: The calculated Nutri-Score. Lower values indicate healthier food.
    """

    # Negative Points (A, B, C, D)
    energy_thresholds = [80, 160, 240, 320, 400, 480, 560, 640, 720, 800]
    A = next((i for i, t in enumerate(energy_thresholds) if energy_kcal <= t), 10)

    sugar_thresholds = [4.5, 9, 13.5, 18, 22.5, 27, 31, 36, 40, 45]
    B = next((i for i, t in enumerate(sugar_thresholds) if sugars_g <= t), 10)

    sat_fat_thresholds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    C = next((i for i, t in enumerate(sat_fat_thresholds) if sat_fat_g <= t), 10)

    salt_thresholds = [90, 180, 270, 360, 450, 540, 630, 720, 810, 900]
    D = next((i for i, t in enumerate(salt_thresholds) if salt_mg <= t), 10)

    # Positive Points (E, F, G)
    if fruit_veg_percent <= 40:
        E = 0
    elif fruit_veg_percent <= 60:
        E = 1
    elif fruit_veg_percent <= 80:
        E = 2
    else:
        E = 5

    fibre_thresholds = [0.7, 1.4, 2.1, 2.8, 3.5]
    F = next((i for i, t in enumerate(fibre_thresholds) if fibre_g <= t), 5)

    protein_thresholds = [1.6, 3.2, 4.8, 6.4, 8.0]
    G = next((i for i, t in enumerate(protein_thresholds) if protein_g <= t), 5)

    # Calculate final Nutri-Score
    negative = A + B + C + D
    positive = E + F + G

    score = negative - positive
    thresholds = [-1, 2, 10, 18]
    labels = ['A', 'B', 'C', 'D', 'E']
    nutriscore = next((label for t, label in zip(thresholds, labels) if score <= t), 'E')
    return nutriscore

