import streamlit as st
import pandas as pd

# Constants
exchange_rate = 0.0914
shopify_percent = 0.0299
shopify_fixed_fee = 0.35
conversion_fee_percent = 0.02

# Function to calculate metrics
def calculate_metrics(cogs, sek_price):
    eur_gross = sek_price * exchange_rate
    fees = (shopify_percent + conversion_fee_percent) * eur_gross + shopify_fixed_fee
    net = eur_gross - fees
    markup = net / cogs
    beroas = net / (net - cogs) if net > cogs else float('inf')
    return {
        "Price (SEK)": sek_price,
        "Gross (€)": round(eur_gross, 2),
        "Net (€)": round(net, 2),
        "Markup": round(markup, 2),
        "BEROAS": round(beroas, 2)
    }

# Streamlit app
st.title("Markup and BEROAS Calculator")

cogs_input = st.number_input("Enter your COGS (€):", min_value=0.0, step=0.01)

if cogs_input > 0:
    results = []
    sek_price = 100  # Start at a reasonable low price
    while True:
        metrics = calculate_metrics(cogs_input, sek_price)
        if metrics["Markup"] >= 2.5:
            results.append(metrics)
        if metrics["Markup"] >= 5.0:
            break
        sek_price += 5  # Increment in steps of 5 SEK

    df = pd.DataFrame(results)
    st.dataframe(df)

    st.success("Table generated successfully!")
else:
    st.info("Please enter a COGS value to start.")
