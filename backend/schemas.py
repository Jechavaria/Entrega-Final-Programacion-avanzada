from pydantic import BaseModel, Field
from typing import Any


class PredictRequest(BaseModel):
    LIMIT_BAL: int = Field(20000, title="Crédito límite")
    SEX: int = Field(2, title="Sexo")
    EDUCATION: int = Field(2, title="Educación")
    MARRIAGE: int = Field(1, title="Matrimonio")
    AGE: int = Field(30, title="Edad")
    PAY_0: int = Field(0, title="Pago en el mes 0")
    PAY_2: int = Field(0, title="Pago en el mes 2")
    PAY_3: int = Field(0, title="Pago en el mes 3")
    PAY_4: int = Field(0, title="Pago en el mes 4")
    PAY_5: int = Field(0, title="Pago en el mes 5")
    PAY_6: int = Field(0, title="Pago en el mes 6")
    BILL_AMT1: int = Field(0, title="Factura mes 1")
    BILL_AMT2: int = Field(0, title="Factura mes 2")
    BILL_AMT3: int = Field(0, title="Factura mes 3")
    BILL_AMT4: int = Field(0, title="Factura mes 4")
    BILL_AMT5: int = Field(0, title="Factura mes 5")
    BILL_AMT6: int = Field(0, title="Factura mes 6")
    PAY_AMT1: int = Field(0, title="Pago mes 1")
    PAY_AMT2: int = Field(0, title="Pago mes 2")
    PAY_AMT3: int = Field(0, title="Pago mes 3")
    PAY_AMT4: int = Field(0, title="Pago mes 4")
    PAY_AMT5: int = Field(0, title="Pago mes 5")
    PAY_AMT6: int = Field(0, title="Pago mes 6")


class PredictResponse(BaseModel):
    prediction: int
    probability: float


class MetricsResponse(BaseModel):
    accuracy: float
    roc_auc: float
    n_samples: int
    created_at: str


class PredictionRecord(BaseModel):
    id: int
    input_data: Any
    prediction: int
    probability: float
    created_at: str
