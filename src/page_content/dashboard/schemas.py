from typing import List, Literal, Dict
from datetime import datetime

from pydantic import BaseModel
import pandas as pd
import plotly.graph_objects as go


class CoverageArea(BaseModel):
    id: str
    type: str
    name: str
    description: str
    checked: bool = False
    sub_areas: List["CoverageArea"] = []

    @property
    def badge_color(self):
        type_ = self.type.lower()
        match type_:
            case "country":
                return "blue"
            case "province":
                return "indigo"
            case "district":
                return "teal"
            case "sub-district":
                return "cyan"
            case "village":
                return "gray"
            case _:
                return "gray"


class DashboardData(BaseModel):
    coverage_area_ids: List[str]
    datetime_start: datetime
    datetime_end: datetime
    num_transformers: int
    num_meters: int
    consumption_pattern_dict: dict
    trend_analysis_dict: dict
    freq_analysis_dict: dict
    anomaly_dict: dict

    @property
    def consumption_pattern_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.consumption_pattern_dict)

    @property
    def trend_analysis_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.trend_analysis_dict)

    @property
    def freq_analysis_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.freq_analysis_dict)

    @property
    def anomaly_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.anomaly_dict)


class Plots(BaseModel):
    num_transformers: int
    num_meters: int
    consump_ptrns_dict: dict
    trend_analysis_dict: dict
    freq_analysis_dict: dict
    anomaly_dict: dict

    @property
    def consump_ptrns_fig(self) -> go.Figure:
        return go.Figure(self.consump_ptrns_dict)

    @property
    def trend_analysis_fig(self) -> go.Figure:
        return go.Figure(self.trend_analysis_dict)

    @property
    def freq_analysis_fig(self) -> go.Figure:
        return go.Figure(self.freq_analysis_dict)

    @property
    def anomaly_fig(self) -> go.Figure:
        return go.Figure(self.anomaly_dict)


class SignalStream(BaseModel):
    title: str
    message: str
    status: Literal["success", "warning", "danger", "info", "primary", "secondary"]
    timestamp: datetime


class ChatMessage(BaseModel):
    id: str
    message: str
    sender: Literal["user", "lyti"]
    timestamp: datetime


class ChatThread(BaseModel):
    id: str
    title: str
    messages: List[ChatMessage] | None = None
    created_at: datetime
    updated_at: datetime


class ChatThreads(BaseModel):
    threads: Dict[str, List[ChatThread]]

    def get_sorted_threads(self, reverse: bool = True) -> Dict[str, List[ChatThread]]:
        """
        Sort the threads by date in order.

        Args:
            reverse (bool): If True, the threads will be sorted in descending order.
                If False, the threads will be sorted in ascending order.

        Returns:
            A dictionary of threads sorted by date.
        """
        return {
            date: sorted(threads, key=lambda x: x.updated_at, reverse=reverse)
            for date, threads in sorted(
                self.threads.items(), key=lambda x: x[0], reverse=reverse
            )
        }
