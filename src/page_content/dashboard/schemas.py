from typing import List, Literal, Dict, Any
from datetime import datetime
from enum import Enum

from pydantic import BaseModel
import pandas as pd
import plotly.graph_objects as go


class CoverageAreaType(Enum):
    COUNTRY = "country"
    PROVINCE = "province"
    DISTRICT = "district"
    SUB_DISTRICT = "sub-district"
    VILLAGE = "village"


class CoverageArea(BaseModel):
    id: str
    type: CoverageAreaType
    name: str
    description: str
    checked: bool = False
    sub_areas: List["CoverageArea"] = []

    @property
    def badge_color(self):
        match self.type:
            case CoverageAreaType.COUNTRY:
                return "blue"
            case CoverageAreaType.PROVINCE:
                return "indigo"
            case CoverageAreaType.DISTRICT:
                return "teal"
            case CoverageAreaType.SUB_DISTRICT:
                return "cyan"
            case CoverageAreaType.VILLAGE:
                return "gray"


class DashboardData(BaseModel):
    coverage_area_ids: List[str]
    datetime_start: datetime
    datetime_end: datetime
    num_transformers: int
    num_meters: int
    consumption_pattern_dict: Dict[str, Any]
    trend_analysis_dict: Dict[str, Any]
    freq_analysis_dict: Dict[str, Any]
    anomaly_dict: Dict[str, Any]

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
    consump_ptrns_dict: Dict[str, Any]
    trend_analysis_dict: Dict[str, Any]
    freq_analysis_dict: Dict[str, Any]
    anomaly_dict: Dict[str, Any]

    @property
    def consump_ptrns_fig(self) -> go.Figure:  # type: ignore
        return go.Figure(self.consump_ptrns_dict)  # type: ignore

    @property
    def trend_analysis_fig(self) -> go.Figure:  # type: ignore
        return go.Figure(self.trend_analysis_dict)  # type: ignore

    @property
    def freq_analysis_fig(self) -> go.Figure:  # type: ignore
        return go.Figure(self.freq_analysis_dict)  # type: ignore

    @property
    def anomaly_fig(self) -> go.Figure:  # type: ignore
        return go.Figure(self.anomaly_dict)  # type: ignore


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
