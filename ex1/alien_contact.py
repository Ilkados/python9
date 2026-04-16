from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ValidationError, model_validator, Field


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals should include received messages")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")

    try:
        valid_contact = AlienContact(
            contact_id="AC001",
            timestamp="2026-04-15T21:30:00",
            location="Sector 7",
            contact_type=ContactType.telepathic,
            signal_strength=8.5,
            duration_minutes=15,
            witness_count=4,
            message_received="We come in peace",
            is_verified=True,
        )

        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")

    except ValidationError as error:
        print("Unexpected validation error:")
        print(error.errors()[0]["msg"])

    print("======================================")

    try:
        AlienContact(
            contact_id="AC002",
            timestamp="2026-04-15T22:00:00",
            location=None,
            contact_type=ContactType.telepathic,
            signal_strength=.0,
            duration_minutes=10,
            witness_count=4,
            message_received=None,
            is_verified=False,
        )
        print("Valid contact report:")
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes} minutes")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")

    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
