from datetime import datetime
from enum import Enum
from typing import List

from pydantic import BaseModel, Field, ValidationError, model_validator  # type: ignore[import-not-found]

class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')

        has_leader = any(
            member.rank in {Rank.commander, Rank.captain}
            for member in self.crew
        )
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )

        if self.duration_days > 365:
            experienced_count = sum(
                member.years_experience >= 5 for member in self.crew
            )
            if experienced_count < len(self.crew) / 2:
                raise ValueError(
                    "Long missions require at least 50% experienced crew"
                )

        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        valid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date="2026-06-15T08:00:00",
            duration_days=900,
            budget_millions=2500.0,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=45,
                    specialization="Mission Command",
                    years_experience=15,
                    is_active=True,
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=34,
                    specialization="Navigation",
                    years_experience=7,
                    is_active=True,
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=29,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True,
                ),
            ],
        )

        print("Valid mission created:")
        print(f"Mission: {valid_mission.mission_name}")
        print(f"ID: {valid_mission.mission_id}")
        print(f"Destination: {valid_mission.destination}")
        print(f"Duration: {valid_mission.duration_days} days")
        print(f"Budget: ${valid_mission.budget_millions}M")
        print(f"Crew size: {len(valid_mission.crew)}")
        print("Crew members:")
        for member in valid_mission.crew:
            print(
                f"- {member.name} ({member.rank.value}) "
                f"- {member.specialization}"
            )

    except ValidationError as error:
        print("Unexpected validation error:")
        print(error)

    print("=========================================")

    try:
        SpaceMission(
            mission_id="M2024_FAIL",
            mission_name="Deep Space Survey",
            destination="Europa",
            launch_date="2026-09-01T10:00:00",
            duration_days=200,
            budget_millions=800.0,
            crew=[
                CrewMember(
                    member_id="C101",
                    name="Mark Lee",
                    rank=Rank.officer,
                    age=30,
                    specialization="Science",
                    years_experience=4,
                    is_active=True,
                ),
                CrewMember(
                    member_id="C102",
                    name="Nina Ray",
                    rank=Rank.lieutenant,
                    age=32,
                    specialization="Systems",
                    years_experience=6,
                    is_active=True,
                ),
            ],
        )

    except ValidationError as error:
        print("Expected validation error:")
        message = error.errors()[0]["msg"]
        print(message.replace("Value error, ", ""))


if __name__ == "__main__":
    main()