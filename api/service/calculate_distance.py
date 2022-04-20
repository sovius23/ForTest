import math


def calculate_distance(longme, latme, longano, latano):
    def to_rads(decimal):
        return decimal * math.pi / 180

    def cos(decimal):
        return math.cos(decimal)

    def sin(decimal):
        return math.sin(decimal)
    latme_rad = to_rads(latme)
    latano_rad = to_rads(latano)
    delta = abs(to_rads(longme) - to_rads(longano))

    def top_fraction():
        return math.sqrt(
            math.pow(cos(latme_rad) * sin(delta), 2) +
            math.pow(cos(latano_rad) * sin(latme_rad) - sin(latano_rad) * cos(latme_rad) * cos(delta), 2)
        )

    def bottom_fraction():
        return sin(latano_rad) * sin(latme_rad) + cos(latano_rad) * cos(latme_rad) * cos(delta)

    return math.ceil(math.atan2(top_fraction(), bottom_fraction()) * 6372795)/1000
