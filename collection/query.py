# Contains the logic for reading the scraping configuration
__author__ = "Matteo Golin"

# Imports
from dataclasses import dataclass, field
from typing import Any, Self
import json

# Constants
JSON = dict[str, Any]


# Query
@dataclass
class Query:
    """Represents a query for scraping RateMyProf."""

    school: str
    professors: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, json_data: JSON) -> Self:
        """Returns a Query object populated from JSON data."""
        return cls(
            school=json_data.get("school"),
            professors=json_data.get("professors")
        )

    def __str__(self):
        return f"{self.school}: {', '.join(self.professors)}"


# Loading queries
def load_queries(query_filepath: str) -> list[Query]:
    """Returns a list of Query objects created from queries in a JSON file."""

    # Read JSON file
    with open(query_filepath, 'r') as file:
        data = json.load(file)

    # Create Query objects using raw JSON
    queries: list[Query] = []
    for query in data.get("queries", []):
        queries.append(
            Query.from_json(query)
        )

    return queries
