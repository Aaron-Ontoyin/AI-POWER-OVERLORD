"""
This module contains the functions to fetch data from the api
"""

from typing import List

from .schemas import CoverageArea


def get_coverage_areas() -> List[CoverageArea]:
    """
    Get the coverage areas from the api
    """
    return [
        CoverageArea(
            id="1",
            type="Country",
            name="Ghana",
            description="Ghana is a country in West Africa.",
            sub_areas=[
                CoverageArea(
                    id="2",
                    type="Province",
                    name="Western Province",
                    description="Western Province",
                    sub_areas=[
                        CoverageArea(
                            id="3",
                            type="District",
                            name="Tongo District",
                            description="Tongo District",
                            sub_areas=[
                                CoverageArea(
                                    id="4",
                                    type="Sub-District",
                                    name="Tongo Sub-District",
                                    description="Tongo Sub-District is a sub-district in the Tongo District of the Western Province of Ghana.",
                                    sub_areas=[
                                        CoverageArea(
                                            id="6",
                                            type="Village",
                                            name="Tongo Village",
                                            description="Tongo Village is a village in the Tongo Sub-District of the Tongo District of the Western Province of Ghana.",
                                            sub_areas=[],
                                        ),
                                        CoverageArea(
                                            id="7",
                                            type="Village",
                                            name="Tongo Village 2",
                                            description="Tongo Village 2 is a village in the Tongo Sub-District of the Tongo District of the Western Province of Ghana.",
                                            sub_areas=[],
                                        ),
                                    ],
                                ),
                                CoverageArea(
                                    id="5",
                                    type="Sub-District",
                                    name="Tongo Sub-District 2",
                                    description="Tongo Sub-District 2 is a sub-district in the Tongo District of the Western Province of Ghana.",
                                    sub_areas=[],
                                ),
                            ],
                        ),
                        CoverageArea(
                            id="4",
                            type="District",
                            name="Tongo District",
                            description="Tongo District",
                            sub_areas=[],
                        ),
                        CoverageArea(
                            id="5",
                            type="District",
                            name="Tongo District",
                            description="Tongo District",
                            sub_areas=[],
                        ),
                    ],
                ),
                CoverageArea(
                    id="3",
                    type="Province",
                    name="Eastern Province",
                    description="Eastern Province",
                    sub_areas=[
                        CoverageArea(
                            id="5",
                            type="District",
                            name="Tongo District",
                            description="Tongo District",
                            sub_areas=[],
                        ),
                        CoverageArea(
                            id="6",
                            type="District",
                            name="Tongo District",
                            description="Tongo District",
                            sub_areas=[],
                        ),
                    ],
                ),
                CoverageArea(
                    id="4",
                    type="Province",
                    name="Northern Province",
                    description="Northern Province",
                    sub_areas=[],
                ),
                CoverageArea(
                    id="5",
                    type="Province",
                    name="Southern Province",
                    description="Southern Province",
                    sub_areas=[],
                ),
            ],
        ),
    ]
