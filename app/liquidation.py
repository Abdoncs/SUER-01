def calcular_liquidacao(saldo_kwh):
    preco_kwh = 0.85
    valor_bruto = saldo_kwh * preco_kwh
    taxa_distribuidora = valor_bruto * 0.12
    taxa_suer = valor_bruto * 0.03
    valor_liquido = valor_bruto - (taxa_distribuidora + taxa_suer)
    return {
        "valor_bruto": round(valor_bruto, 2),
        "taxa_distribuidora": round(taxa_distribuidora, 2),
        "taxa_suer": round(taxa_suer, 2),
        "valor_liquido": round(valor_liquido, 2)
    }
