import pandas as pd
import pytest
from metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    assert attrition_rate(df) == 50.0


def test_attrition_rate_all_stay():
    df = pd.DataFrame({
        "employee_id": [1, 2],
        "attrition": ["No", "No"],
    })
    assert attrition_rate(df) == 0.0


def test_attrition_rate_all_leave():
    df = pd.DataFrame({
        "employee_id": [1, 2],
        "attrition": ["Yes", "Yes"],
    })
    assert attrition_rate(df) == 100.0


# --- attrition_by_department ---

def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_calculates_correct_rates():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5],
        "department": ["Sales", "Sales", "HR", "HR", "HR"],
        "attrition": ["Yes", "Yes", "Yes", "No", "No"],
    })
    result = attrition_by_department(df)
    sales = result[result["department"] == "Sales"].iloc[0]
    hr = result[result["department"] == "HR"].iloc[0]
    assert sales["attrition_rate"] == 100.0
    assert hr["attrition_rate"] == 33.33


def test_attrition_by_department_sorted_descending_by_rate():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5],
        "department": ["Sales", "Sales", "HR", "HR", "HR"],
        "attrition": ["Yes", "Yes", "Yes", "No", "No"],
    })
    result = attrition_by_department(df)
    assert result.iloc[0]["department"] == "Sales"
    assert result.iloc[1]["department"] == "HR"


# --- attrition_by_overtime ---

def test_attrition_by_overtime_calculates_correct_rates():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "overtime": ["Yes", "Yes", "No", "No"],
        "attrition": ["Yes", "Yes", "No", "No"],
    })
    result = attrition_by_overtime(df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["attrition_rate"] == 100.0
    assert no_row["attrition_rate"] == 0.0


def test_attrition_by_overtime_returns_expected_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2],
        "overtime": ["Yes", "No"],
        "attrition": ["Yes", "No"],
    })
    result = attrition_by_overtime(df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


# --- average_income_by_attrition ---

def test_average_income_by_attrition_returns_correct_means():
    df = pd.DataFrame({
        "attrition": ["Yes", "Yes", "No", "No"],
        "monthly_income": [4000, 5000, 7000, 8000],
    })
    result = average_income_by_attrition(df)
    yes_income = result[result["attrition"] == "Yes"]["avg_monthly_income"].iloc[0]
    no_income = result[result["attrition"] == "No"]["avg_monthly_income"].iloc[0]
    assert yes_income == 4500.0
    assert no_income == 7500.0


# --- satisfaction_summary ---

def test_satisfaction_summary_rate_is_per_group_not_share_of_leavers():
    # Validates the corrected formula: leavers / total_employees per group
    # Level 1: 2/2 = 100%, Level 2: 1/2 = 50%, Level 3: 0/2 = 0%
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5, 6],
        "job_satisfaction": [1, 1, 2, 2, 3, 3],
        "attrition": ["Yes", "Yes", "Yes", "No", "No", "No"],
    })
    result = satisfaction_summary(df)
    assert result[result["job_satisfaction"] == 1]["attrition_rate"].iloc[0] == 100.0
    assert result[result["job_satisfaction"] == 2]["attrition_rate"].iloc[0] == 50.0
    assert result[result["job_satisfaction"] == 3]["attrition_rate"].iloc[0] == 0.0


def test_satisfaction_summary_sorted_ascending_by_satisfaction():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "job_satisfaction": [3, 1, 4, 2],
        "attrition": ["No", "Yes", "No", "No"],
    })
    result = satisfaction_summary(df)
    assert list(result["job_satisfaction"]) == [1, 2, 3, 4]
