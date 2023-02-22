from typing import Union


class DragonValidator:
    @staticmethod
    def validate_name(data: dict) -> Union[dict, bool]:
        """
        Validate dragon name based on the length. Must be between 100 and 3
        """
        return (
            {"message": "Name attribute must have length between 3 and 100"}
            if 100 < len(data.get("name", "")) or len(data.get("name", "")) < 3
            else True
        )

    @staticmethod
    def validate_breed(data: dict) -> Union[dict, bool]:
        """
        Validate dragon breed based on the length. Must be between 150 and 5
        """
        return (
            {"message": "Breed attribute must have length between 5 and 150"}
            if 150 < len(data.get("breed", "")) or len(data.get("breed", "")) < 5
            else True
        )

    @staticmethod
    def validate_danger_rating(data: dict) -> Union[dict, bool]:
        """
        Validate dragon rating based on the value. Must be between 10 and 0 and
        value must be integer
        """
        return (
            {"message": "Danger rating must be integer or between 0 and 10"}
            if not isinstance(data.get("danger_rating", 0), int)
            or 0 > data.get("danger_rating")
            or data.get("danger_rating") > 10
            else True
        )

    def validate_dragon(self, data: dict) -> Union[dict, bool]:
        """
        Validate dragon using validators and send list of messages to user
        """
        validators = {
            "name": self.validate_name,
            "breed": self.validate_breed,
            "danger_rating": self.validate_danger_rating,
        }
        keys = ["name", "breed", "danger_rating", "description"]
        messages = []
        for key in data.keys():
            if key not in keys:
                return {"message": f"Extra {key} is present in request"}

            if key != "description":
                res = validators.get(key)(data)
                if res is not True:
                    messages.append(res)

        return messages if messages else True
