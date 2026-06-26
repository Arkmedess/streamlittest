from pydantic import BaseModel, EmailStr, Field
from decimal import Decimal
from datetime import date

class Venda(BaseModel):

    cliente_nome_fantasia: str = Field(min_length=1, max_length=150)
    cidade: str = Field(min_length=1, max_length=60)
    uf: str = Field(min_length=2, max_length=2)

    email_cliente: EmailStr | None = None

    data_faturamento: date

    tipo_operacao: str = Field(min_length=1, max_length=40)
    status: str = Field(min_length=1, max_length=20)

    pedido_venda: str = Field(min_length=1, max_length=30)
    nota_fiscal: str = Field(min_length=1, max_length=30)

    prd: str = Field(min_length=1, max_length=30)
    descricao_produto: str = Field(min_length=1, max_length=200)

    qtd: Decimal = Field(gt=0)

    vlr_total_mercadoria: Decimal = Field(gt=0)
    vlr_total_nf: Decimal = Field(gt=0)