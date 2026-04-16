from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError  # type: ignore[import-not-found]


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")

    try:
        valid_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=21,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2026-04-14T10:30:00",
            notes="Main orbital research station."
        )

        print("Valid station created:")
        print(f"ID: {valid_station.station_id}")
        print(f"Name: {valid_station.name}")
        print(f"Crew: {valid_station.crew_size} people")
        print(f"Power: {valid_station.power_level}%")
        print(f"Oxygen: {valid_station.oxygen_level}%")
        status = (
            "Operational"
            if valid_station.is_operational
            else "Not operational"
        )
        print(f"Status: {status}")

    except ValidationError as error:
        print("Validation error while creating valid station:")
        print(error)

    print("========================================")

    try:
        invalid_station = SpaceStation(
            station_id="BAD01",
            name="Broken Station",
            crew_size=25,
            power_level=85.0,
            oxygen_level=90.0,
            last_maintenance="2026-04-14T10:30:00"
        )
        print(invalid_station)

    except ValidationError as error:
        print("Expected validation error:")
        print(error)


if __name__ == "__main__":
    main()
