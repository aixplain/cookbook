def get_nutriscore_beverage_score(
    energy_kcal: float, sugars_g: float, sat_fat_g: float, salt_mg: float, 
    fruit_veg_percent: int, fibre_g: float, protein_g: float  
) -> str:
    """Calculates the Nutri-Score for beverages based on nutritional values.

    Args:
        energy_kcal (float): Energy content in kilocalories.
        sugars_g (float): Sugar content in grams.
        sat_fat_g (float): Saturated fat content in grams.
        salt_mg (float): Salt content in milligrams.
        fruit_veg_percent (int): Percentage of fruit and vegetables.
        fibre_g (float): Fiber content in grams.
        protein_g (float): Protein content in grams.

    Returns:
        str: The calculated Nutri-Score for the beverage.
    """

    # Negative points (A, B, C, D)
    energy_thresholds = [7.2, 14.3, 21.5, 28.5, 35.9, 43.0, 50.2, 57.4, 64.5]
    A = next((i for i, t in enumerate(energy_thresholds) if energy_kcal <= t), 10)

    sugar_thresholds = [1.5, 3.0, 4.5, 6.0, 7.5, 9.0, 10.5, 12.0, 13.5]
    B = next((i for i, t in enumerate(sugar_thresholds) if sugars_g <= t), 10)

    sat_fat_thresholds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    C = next((i for i, t in enumerate(sat_fat_thresholds) if sat_fat_g <= t), 10)

    salt_thresholds = [90, 180, 270, 360, 450, 540, 630, 720, 810, 900]
    D = next((i for i, t in enumerate(salt_thresholds) if salt_mg <= t), 10)

    # Positive points (E, F, G)
    if fruit_veg_percent <= 40:
        E = 0
    elif fruit_veg_percent <= 60:
        E = 2
    elif fruit_veg_percent <= 80:
        E = 4
    else:
        E = 10

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
