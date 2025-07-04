class PricingRules:
    def __init__(self):
        pass  # You can later add configurable pricing parameters here

    def motorcycle_fare(self, distance_km):
        if distance_km <= 2:
            return 50
        elif distance_km <= 7:
            return 50 + (distance_km - 2) * 10
        else:
            return 50 + (5 * 10) + (distance_km - 7) * 15

    def car4_fare(self, distance_km, duration_min):
        base_fare = 45
        distance_fee = 15 * distance_km
        duration_fee = 2 * duration_min
        return base_fare + distance_fee + duration_fee

    def car6_fare(self, distance_km, duration_min):
        base_fare = 55
        distance_fee = 20 * distance_km
        duration_fee = 2 * duration_min
        return base_fare + distance_fee + duration_fee

    def tank_fare(self, distance_km):
        return 100_000 * distance_km

