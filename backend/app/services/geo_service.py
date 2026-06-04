import math


class GeoService:

    @staticmethod
    def calculate_distance(
        lat1,
        lon1,
        lat2,
        lon2
    ):

        """
        Returns distance in meters
        """

        R = 6371000

        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))

        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(lat1)
            *
            math.cos(lat2)
            *
            math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        distance = R * c

        return round(distance, 2)

    @staticmethod
    def is_inside_radius(
        office_lat,
        office_lon,
        user_lat,
        user_lon,
        allowed_radius=5
    ):

        distance = GeoService.calculate_distance(
            office_lat,
            office_lon,
            user_lat,
            user_lon
        )

        return {

            "allowed":
            distance <= allowed_radius,

            "distance":
            distance

        }