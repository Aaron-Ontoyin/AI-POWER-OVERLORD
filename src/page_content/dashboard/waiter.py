"""
This module contains the functions to fetch data from the api
"""

import dash.exceptions
from typing import List
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import random
import time

from .schemas import (
    CoverageArea,
    DashboardData,
    SignalStream,
    ChatMessage,
    ChatThread,
    ChatThreads,
)


def get_coverage_areas() -> List[CoverageArea]:
    """
    Get the coverage areas from the api
    """
    time.sleep(2)
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


def get_dashboard_data(
    datetime_start: datetime,
    datetime_end: datetime,
    coverage_areas_ids: List[str],
) -> DashboardData:
    """
    Get the data for all graphs and infos given some filters.

    Args:
        datetime_start: The start date and time of the data to fetch.
        datetime_end: The end date and time of the data to fetch.
        coverage_areas_ids: The ids of the coverage areas to fetch data for.

    Returns:
        The dashboard data.
    """
    y_dist = random.choice([(0, 10, 0.1), (10, 30, 0.1), (30, 90, 3), (25, 50, 0.5)])
    periods = len(np.arange(y_dist[0], y_dist[1], y_dist[2]))
    df = pd.DataFrame(
        {
            "T1": np.sin(np.arange(y_dist[0], y_dist[1], y_dist[2])),
            "T2": np.cos(np.arange(y_dist[0], y_dist[1], y_dist[2])),
            "T3": np.tan(np.arange(y_dist[0], y_dist[1], y_dist[2])),
        },
        index=pd.date_range(start="2024-01-01", periods=periods, freq="D"),
    )
    time.sleep(2)

    return DashboardData(
        coverage_area_ids=coverage_areas_ids,
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        num_transformers=random.choice([10, 15, 20, 40]),
        num_meters=random.choice([50, 100, 200, 1000]),
        consumption_pattern_dict=df.to_dict(),
        trend_analysis_dict=df.to_dict(),
        freq_analysis_dict=df.to_dict(),
        anomaly_dict=df.to_dict(),
    )


def get_signal_streams() -> List[SignalStream]:
    time.sleep(1)
    return [
        SignalStream(
            title="Transformer 1 stopped working",
            message="Transformer 1 stopped working at 10:00 AM. Please check the transformer.",
            status="danger",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
        SignalStream(
            title="Transformer 2 is working again",
            message="Transformer 2 is working again at 10:00 AM. Please check the transformer.",
            status="success",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
        SignalStream(
            title="Illegal connections at Tongo Village",
            message="Illegal connections at Tongo Village at 10:00 AM. Please check the transformer.",
            status="warning",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
        SignalStream(
            title="Transformer 1 is working again",
            message="Transformer 1 is working again at 10:00 AM. Please check the transformer.",
            status="info",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
        SignalStream(
            title="Transformer 1 is working again",
            message="Transformer 1 is working again at 10:00 AM. Please check the transformer.",
            status="primary",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
        SignalStream(
            title="Transformer 1 is working again",
            message="Transformer 1 is working again at 10:00 AM. Please check the transformer.",
            status="secondary",
            timestamp=datetime.now() - timedelta(hours=1),
        ),
    ]


def get_chat_thread(
    thread_id: str,
    new_message: str | None = None,
    datetime_start: datetime | str | None = None,
    datetime_end: datetime | str | None = None,
    coverage_areas_ids: List[str] | None = None,
) -> ChatThread:
    """
    Get a chat thread with messages.

    Args:
        thread_id: The id of the chat thread.
        new_message: The new message to add to the chat thread.
        datetime_start: The start date and time of the data to fetch for context.
        datetime_end: The end date and time of the data to fetch for context.
        coverage_areas_ids: The ids of the coverage areas to fetch data for context.

    Returns:
        A chat thread with messages.
    """
    time.sleep(3)
    lyti_res = random.choice(
        [
            ChatMessage(
                id="1",
                message="Hello, how are you?",
                sender="lyti",
                timestamp=datetime.now(),
            ),
            ChatMessage(
                id="2",
                message="I'm Lyti, your AI assistant. How can I help you today?",
                sender="lyti",
                timestamp=datetime.now(),
            ),
            ChatMessage(
                id="3",
                message="Please tell me about the data",
                sender="lyti",
                timestamp=datetime.now(),
            ),
            ChatMessage(
                id="4",
                message="The data is about the electricity consumption of the transformers in the Tongo District.",
                sender="lyti",
                timestamp=datetime.now(),
            ),
            ChatMessage(
                id="5",
                message="what is the total consumption of the transformers in the Tongo District?",
                sender="lyti",
                timestamp=datetime.now(),
            ),
            ChatMessage(
                id="6",
                message="The total consumption of the transformers in the Tongo District is 1000 kWh. Do you want to know more about the data? I can help you with that. I can also help you with the data analysis.",
                sender="lyti",
                timestamp=datetime.now(),
            ),
        ]
    )
    return ChatThread(
        id=thread_id,
        title=f"Chat Thread {thread_id}",
        messages=[
            ChatMessage(
                id="user-message",
                message=new_message or "Hello, how are you?",
                sender="user",
                timestamp=datetime.now(),
            ),
            lyti_res,
        ],
        created_at=datetime.now() - timedelta(days=1),
        updated_at=datetime.now() - timedelta(days=1),
    )


def get_chat_threads() -> ChatThreads:
    """
    Return chat threads for a user. Does not include the messages in the threads.

    Returns:
        ChatThreads: A list of chat threads.
    """
    chat_threads = [
        ChatThread(
            id="1",
            title="Transformer 1 stopped working",
            created_at=datetime.now() - timedelta(days=2),
            updated_at=datetime.now() - timedelta(days=2),
        ),
        ChatThread(
            id="2",
            title="Meaning of the data",
            created_at=datetime.now() - timedelta(days=1),
            updated_at=datetime.now() - timedelta(days=1),
        ),
        ChatThread(
            id="3",
            title="Meaning of the data",
            created_at=datetime.now() - timedelta(days=1),
            updated_at=datetime.now() - timedelta(days=1),
        ),
        ChatThread(
            id="4",
            title="Meaning of the data",
            created_at=datetime.now() - timedelta(days=1),
            updated_at=datetime.now() - timedelta(days=1),
        ),
        ChatThread(
            id="5",
            title="Total consumption in Tongo District?",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ChatThread(
            id="6",
            title="Total consumption in Tongo District?",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ChatThread(
            id="7",
            title="Total consumption in Tongo District?",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
        ChatThread(
            id="8",
            title="Total consumption in Tongo District?",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        ),
    ]
    threads = {}
    for chat_thread in chat_threads:
        date = chat_thread.updated_at.strftime("%Y-%m-%d")
        if date not in threads:
            threads[date] = [chat_thread]
        else:
            threads[date].append(chat_thread)
    return ChatThreads(threads=threads)
