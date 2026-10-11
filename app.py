import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Banking Loans Analysis", layout="wide")
df = pd.read_csv("Banking_Loans_CLEANED_Mid_Project.csv")
df["origination_date"] = pd.to_datetime(df["origination_date"])
st.sidebar.title("Dashboard Analysis Navigation")
page = st.sidebar.radio("Select a page:", ["🏠 Portfolio Overview", "📊📈 Portfolio Insights", "🔍📈 Portfolio Deep Dive", "📋 Executive Summary"])
if page == "🏠 Portfolio Overview":

    # Center the title and control its width
    col1, col2, col3 = st.columns([1.25, 2, 1])
    with col2:
        st.title("Banking Loans Dataset Analysis")

    # Center the image and control its width
    col1, col2, col3 = st.columns([0.75, 1.75, 0.75])
    with col2:
        st.image("Banking_Loans_App.jpg", use_container_width=True)

    st.info(
    "This dataset explores Loan Details & Performance, Customer Characteristics,  "
    "Credit Patterns, and Financial Indicators across the banking loan portfolio.")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("**Loan Records**")
        st.metric("Loan Records", f"{len(df):,}", label_visibility="collapsed")

    with col2:
        st.markdown("**Loan Attributes**")
        st.metric("Loan Attributes", f"{df.shape[1]:,}", label_visibility="collapsed")

    with col3:
        st.markdown("**Loan Period Covered**")
        st.metric("Loan Period Covered", f"{df['origination_date'].dt.year.min()}-{df['origination_date'].dt.year.max()}", label_visibility="collapsed")

    with col4:
        st.markdown("**Loan Types**")
        st.metric("Loan Types", f"{df['loan_type'].nunique():,}", label_visibility="collapsed")

    with col5:
        st.markdown("**Loan Status Categories**")
        st.metric("Loan Status Categories", f"{df['loan_status'].nunique():,}", label_visibility="collapsed")

    # ============================================================
    # Portfolio at a Glance
    # ============================================================

    st.subheader("Loans Dataset & Portfolio at a Glance")

    attribute_categories = {"Customer Profile": 4, "Loan Characteristics": 5, "Credit & Risk": 3,
                            "Application & Status": 4, "Repayment & Exposure": 4}

    fig = px.pie(names=attribute_categories.keys(), values=attribute_categories.values(), hole=0.5)

    fig.update_layout(title="Analytical Attributes by Data Category", showlegend=True)

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "The dataset contains 20 analytical attributes grouped into five "
        "main data categories. The loan_id field is retained as an identifier "
        "and is excluded from the analytical attribute breakdown. ")

elif page == "📊📈 Portfolio Insights":

    st.title("Portfolio Analysis Overview")

    st.markdown("""
        This section provides a comprehensive insights of the bank's loan portfolio,
        covering customer characteristics, financial profiles, lending activity,
        credit quality, risk exposure, portfolio trends, and loan maturity.

        **Key areas covered:**

        - **Customer Profile**
        - **Financial Profile**
        - **Lending Activity**
        - **Credit Profile**
        - **Risk Profile**
        - **Bivariate Relationships**
        - **Portfolio Trends**
        - **Loan Maturity** """)

    st.header("1. Univariate Analysis")

    # ============================================================
    # QUESTION 1: Customer Age Distribution
    # ============================================================

    st.subheader("Q1. Customer Age Distribution")
    age_counts = df["customer_age"].value_counts().sort_index()
    fig = px.bar(
        x=age_counts.values,
        y=age_counts.index,
        text=age_counts.values,
        orientation="h",
        labels={"x": "Number of Customers", "y": "Customer Age"}, title="Customer Age Distribution")
    fig.update_traces(textposition="outside")
    fig.update_layout(height=900)
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The customer age distribution shows that "
        "the bank serves customers across a broad range of age groups, "
        "reflecting a diversified customer base.")
    st.divider()

    # ============================================================
    # QUESTION 2: Annual Income Distribution
    # ============================================================

    st.subheader("Q2. Annual Income Distribution")
    fig = px.histogram(
        df,
        x="annual_income_egp",
        nbins=30,
        title="Annual Income Distribution",
        labels={"annual_income_egp": "Annual Income (EGP)"})
    fig.update_yaxes(title_text="Number of Customers")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of annual income shows that "
        "the bank serves customers across different income levels, "
        "indicating a diversified customer base with lending activity "
        "across a broad range of financial profiles.")
    st.divider()

    # ============================================================
    # QUESTION 3: Loan Amount Distribution
    # ============================================================
    
    st.subheader("Q3. Loan Amount Distribution")
    fig = px.histogram(
        df,
        x="loan_amount_egp",
        nbins=30,
        title="Loan Amount Distribution",
        labels={"loan_amount_egp": "Loan Amount (EGP)"})
    fig.update_yaxes(title_text="Number of Loans")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of loan amounts shows that "
        "the bank's lending portfolio covers a range of financing needs, "
        "from smaller to larger loan amounts.")
    st.divider()

    # ============================================================
    # QUESTION 4: Credit Score Distribution
    # ============================================================
    
    st.subheader("Q4. Credit Score Distribution")
    fig = px.histogram(
        df,
        x="credit_score",
        nbins=30,
        title="Credit Score Distribution",
        labels={"credit_score": "Credit Score"})
    fig.update_yaxes(title_text="Number of Loans")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of credit scores provides "
        "an overview of the credit profiles represented in the loan portfolio, "
        "supporting a better understanding of the bank's overall credit risk exposure.")
    st.divider()

    st.header("2. Bivariate & Multivariate Analysis")

    # ============================================================
    # QUESTION 5: Loans by Risk Grade
    # ============================================================
    
    st.subheader("Q5. Loans by Risk Grade")
    loan_type_options = ["All Loan Types"] + sorted(df["loan_type"].dropna().unique())
    selected_loan_type_q5 = st.radio("Loan Type:", loan_type_options, horizontal=True, key="q5_loan_type")
    if selected_loan_type_q5 == "All Loan Types":
            q5_df = df
    else:
        q5_df = df[df["loan_type"] == selected_loan_type_q5]
    risk_order = ["A", "B", "C", "D", "E"]
    risk_grade_counts = (q5_df["risk_grade"].value_counts().reindex(risk_order, fill_value=0))
    fig = px.bar(
        x=risk_grade_counts.index,
        y=risk_grade_counts.values,
        text=risk_grade_counts.values,
        labels={"x": "Risk Grade", "y": "Number of Loans"}, title=f"Loans by Risk Grade - {selected_loan_type_q5}")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of loans across risk grades "
        "provides an overview of the portfolio's credit risk composition, "
        "helping the bank monitor how lending exposure is distributed across "
        "different levels of credit risk.")
    st.divider()

    # ============================================================
    # QUESTION 6: Loan Amount vs Annual Income
    # ============================================================
    
    st.subheader("Q6. Loan Amount vs Annual Income")
    fig = px.scatter(
        df,
        x="annual_income_egp",
        y="loan_amount_egp",
        title="Loan Amount vs Annual Income",
        labels={"annual_income_egp": "Annual Income (EGP)", "loan_amount_egp": "Loan Amount (EGP)"}, opacity=0.6)
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The relationship between annual income and "
        "loan amount helps the bank understand how financing amounts vary "
        "across different customer income levels and provides insight into "
        "the structure of lending exposure.")
    st.divider()

    # ============================================================
    # QUESTION 7: Credit Score Across Risk Grades
    # ============================================================
    
    st.subheader("Q7. Credit Score Across Risk Grades")
    risk_order = ["A", "B", "C", "D", "E"]
    fig = px.box(
        df,
        x="risk_grade",
        y="credit_score",
        category_orders={"risk_grade": risk_order},
        title="Credit Score Across Risk Grades",
        labels={"risk_grade": "Risk Grade", "credit_score": "Credit Score"})
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of credit scores across "
        "risk grades helps the bank understand how customer credit quality "
        "varies across different levels of portfolio risk.")
    st.divider()

    # ============================================================
    # QUESTION 8: Interest Rate Across Risk Grades
    # ============================================================

    st.subheader("Q8. Interest Rate Across Risk Grades")
    risk_order = ["A", "B", "C", "D", "E"]
    fig = px.box(
        df,
        x="risk_grade",
        y="interest_rate_pct",
        category_orders={"risk_grade": risk_order},
        title="Interest Rate Across Risk Grades",
        labels={"risk_grade": "Risk Grade", "interest_rate_pct": "Interest Rate (%)"})
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of interest rates across "
        "risk grades helps the bank understand how pricing varies across "
        "different levels of credit risk within the loan portfolio.")
    st.divider()

    # ============================================================
    # QUESTION 9: Average Loan Amount by Employment Status
    # ============================================================

    st.subheader("Q9. Average Loan Amount by Employment Status")
    avg_loan_by_employment = (df.groupby("employment_status")["loan_amount_egp"].mean().sort_values(ascending=False))
    fig = px.bar(
        x=avg_loan_by_employment.index,
        y=avg_loan_by_employment.values,
        text=avg_loan_by_employment.values.round(0),
        labels={"x": "Employment Status", "y": "Average Loan Amount (EGP)"}, title="Average Loan Amount by Employment Status")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The average loan amount across employment "
        "statuses helps the bank understand how financing levels vary "
        "across different customer employment profiles.")
    st.divider()

    st.header("3. Portfolio Trend Analysis")

    # ============================================================
    # QUESTION 10: Loan Origination Volume Over Time
    # ============================================================

    st.subheader("Q10. Loan Origination Volume Over Time")
    origination_counts = (df.groupby(df["origination_date"].dt.to_period("M")).size().reset_index(name="loan_count"))
    origination_counts["origination_date"] = (origination_counts["origination_date"].astype(str))
    fig = px.line(
        origination_counts,
        x="origination_date",
        y="loan_count",
        markers=True,
        title="Loan Origination Volume Over Time",
        labels={"origination_date": "Origination Month", "loan_count": "Number of Loans"})
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The trend in loan originations over time "
        "helps the bank monitor changes in lending activity and identify "
        "periods of higher or lower loan origination volumes.")
    st.divider()

    # ============================================================
    # QUESTION 11: Total Loan Amount Over Time
    # ============================================================

    st.subheader("Q11. Total Loan Amount Over Time")
    loan_amount_over_time = (df.groupby(df["origination_date"].dt.to_period("M"))["loan_amount_egp"].sum().reset_index())
    loan_amount_over_time["origination_date"] = (loan_amount_over_time["origination_date"].astype(str))
    fig = px.line(
        loan_amount_over_time,
        x="origination_date",
        y="loan_amount_egp",
        markers=True,
        title="Total Loan Amount Over Time",
        labels={"origination_date": "Origination Month", "loan_amount_egp": "Total Loan Amount (EGP)"})
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The trend in total loan amounts over time "
        "helps the bank monitor changes in the value of lending activity "
        "and identify periods with higher or lower financing volumes.")
    st.divider()

    st.header("4. Loan Maturity Analysis")

    # ============================================================
    # QUESTION 12: Expected Loan End Year
    # ============================================================

    st.subheader("Q12. Expected Loan End Year")
    end_year_counts = (df["expected_end_year"].value_counts().sort_index())
    fig = px.bar(
        x=end_year_counts.index,
        y=end_year_counts.values,
        text=end_year_counts.values,
        labels={"x": "Expected End Year", "y": "Number of Loans"}, title="Loans by Expected End Year")
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "**Business Insight:** The distribution of expected loan end years "
        "shows that the portfolio includes loans with extended maturity "
        "horizons, demonstrating the bank's exposure to and management of "
        "longer-term lending commitments.")
    st.divider()

    # ============================================================
    # QUESTION 13. LONG-TERM PORTFOLIO STRUCTURE
    # ============================================================

    st.header("Q13. Long-Term Portfolio Structure")

    maturity_by_type = (df.groupby("loan_type")["expected_end_year"].mean().sort_values().reset_index())

    fig = px.bar(maturity_by_type,
        x="loan_type",
        y="expected_end_year",
        text=maturity_by_type["expected_end_year"].round(1),
        labels={"loan_type": "Loan Type", "expected_end_year": "Average Expected End Year"},
        title="Average Expected Maturity Year by Loan Type")

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        Loan terms and expected maturity dates provide a forward-looking view
        of the portfolio. Comparing the average expected maturity year across
        loan types highlights differences in the time horizon of lending
        commitments. """)
    
    st.write(
        "**Business Insight:** Different loan products carry different expected "
        "maturity horizons, highlighting variation in the duration of the bank's "
        "future lending commitments. ")

    st.divider()

elif page == "🔍📈 Portfolio Deep Dive":

    st.title("Portfolio Deep Dive")

    st.markdown(
        """
        This section provides a deeper insights of the bank's loan portfolio by
        connecting customer, credit, risk, pricing, product, and maturity
        characteristics.

        The analysis goes beyond individual portfolio measures to highlight
        relationships and patterns across different dimensions of the lending
        portfolio. """)


    # ============================================================
    # 1. CUSTOMER & FINANCING DIVERSITY
    # ============================================================

    st.header("1. Customer & Financing Diversity")

    risk_by_loan_type = (
        pd.crosstab(
            df["loan_type"],
            df["risk_grade"],
            normalize="index").reset_index())

    risk_columns = ["A", "B", "C", "D", "E"]

    for col in risk_columns:
        if col not in risk_by_loan_type.columns:
            risk_by_loan_type[col] = 0

    risk_by_loan_type = risk_by_loan_type[["loan_type", "A", "B", "C", "D", "E"]]

    fig = px.bar(risk_by_loan_type,
        x="loan_type",
        y=risk_columns,
        text_auto=".0%",
        barmode="stack",
        labels={"loan_type": "Loan Type", "value": "Share of Loans", "variable": "Risk Grade"}, title="Risk Grade Composition by Loan Type")

    fig.update_yaxes(tickformat=".0%")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        The portfolio serves customers with different financial characteristics
        across a range of lending products. Looking at the risk composition within
        each loan type provides a broader view of how credit exposure is distributed
        across the bank's products. """)
    
    st.write(
        "**Business Insight:** The risk composition varies across loan products, "
        "showing that different lending segments carry different mixes of credit "
        "profiles within the overall portfolio. ")

    # ============================================================
    # 2. CREDIT, RISK & PRICING
    # ============================================================

    st.header("2. Credit, Risk & Pricing")

    fig = px.scatter(df,
        x="credit_score",
        y="interest_rate_pct",
        color="risk_grade",
        category_orders={"risk_grade": ["A", "B", "C", "D", "E"]},
        opacity=0.55,
        labels={"credit_score": "Credit Score", "interest_rate_pct": "Interest Rate (%)","risk_grade": "Risk Grade"},
        title="Credit Score and Interest Rate Across Risk Profiles")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        Credit score and interest rate provide two complementary views of the
        portfolio: customer credit characteristics and loan pricing. Examining
        them together, while retaining the risk-grade structure, provides a
        broader perspective on the relationship between credit quality and pricing. """)
    
    st.write(
        "**Business Insight:** The combined view of credit scores, risk grades, "
        "and interest rates provides insight into how customer credit "
        "characteristics are reflected within the portfolio's pricing structure. ")


    # ============================================================
    # 3. PORTFOLIO COMPOSITION & LOAN STATUS
    # ============================================================

    st.header("3. Portfolio Composition & Loan Status")

    status_by_loan_type = (
        pd.crosstab(
            df["loan_type"],
            df["loan_status"],
            normalize="index").reset_index())

    status_columns = ["Active", "Closed", "Defaulted", "Restructured", "Written Off"]

    for col in status_columns:
        if col not in status_by_loan_type.columns:
            status_by_loan_type[col] = 0

    status_by_loan_type = status_by_loan_type[
        ["loan_type"] + status_columns]

    fig = px.bar(status_by_loan_type,
        x="loan_type",
        y=status_columns,
        text_auto=".0%",
        barmode="stack",
        labels={"loan_type": "Loan Type", "value": "Share of Loans", "variable": "Loan Status"},
        title="Loan Status Composition by Loan Type")

    fig.update_yaxes(tickformat=".0%")

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        Loan status provides an additional perspective on portfolio composition.
        Comparing status distributions across loan types helps show how different
        lending products are represented across the current portfolio lifecycle. """)

    st.write(
        "**Business Insight:** Loan products show different portfolio-status "
        "compositions, providing a broader view of how lending activity is "
        "distributed across different stages of the loan lifecycle. ")

    # ============================================================
    # 4: Monthly Installment Across Loan Amount and Loan Types
    # ============================================================

    st.subheader("4. Monthly Installment Across Loan Amounts and Loan Types")

    df["loan_amount_group"] = pd.qcut(
    df["loan_amount_egp"],
    q=4,
    labels=["Low", "Medium", "High", "Very High"])

    installment_summary = (
    df.groupby(
        ["loan_type", "loan_amount_group"],
        observed=True
    )["monthly_installment_egp"]
    .mean()
    .reset_index())

    heatmap_data = installment_summary.pivot(
    index="loan_type",
    columns="loan_amount_group",
    values="monthly_installment_egp")
    
    fig = px.imshow(
    heatmap_data,
    text_auto=".0f",
    aspect="auto",
    color_continuous_scale="YlOrRd",
    title="Average Monthly Installment by Grouped Loan Amounts and Loan Type",
    labels={
        "x": "Loan Amount Group",
        "y": "Loan Type",
        "color": "Average Monthly Installment (EGP)"})

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Loan Amount Groups are based on quartiles: "
        "Low = lowest 25%, Medium = 25%-50%, "
        "High = 50%-75%, and Very High = highest 25%. ")

    st.write(
    "**Business Insight:** The heatmap shows how average monthly "
    "installments vary across different loan amount groups and loan types. "
    "Higher loan amount groups generally represent greater monthly "
    "repayment obligations, while differences across loan types may "
    "highlight variations in loan structure and repayment terms. ")

# ============================================================
# 5. REPAYMENT EXPOSURE
# ============================================================

    st.header("5. Repayment Exposure")

    remaining_balance = (df.groupby(["loan_type", "loan_status"])["remaining_balance_egp"].mean().reset_index())

    fig = px.bar(
        remaining_balance,
        x="loan_type",
        y="remaining_balance_egp",
        color="loan_status",
        barmode="group",
        labels={"loan_type": "Loan Type", "remaining_balance_egp": "Average Remaining Balance (EGP)", "loan_status": "Loan Status"},
        title="Average Remaining Balance by Loan Type and Loan Status")

    st.plotly_chart(fig, use_container_width=True)

    st.write(
        "**Business Insight:** Comparing average remaining balances across "
        "loan types and loan statuses helps the bank identify where higher "
        "outstanding exposure remains within the portfolio. ")

    st.divider()

elif page == "📋 Executive Summary":

    st.title("Executive Summary")

    st.markdown(
        """
        This section consolidates findings from the portfolio analysis
        into a set of interconnected business insights.

        The following business stories combines relevant findings and supporting statistics
        to highlight broader perspective and patterns across customer characteristics,
        lending exposure, credit quality, portfolio composition, and long-term commitments. """)

    # ============================================================
    # PREPARE PORTFOLIO STATISTICS
    # ============================================================

    total_records = len(df)
    total_loan_value = df["loan_amount_egp"].sum()
    median_age = df["customer_age"].median()
    median_income = df["annual_income_egp"].median()
    median_loan_amount = df["loan_amount_egp"].median()

    loan_type_counts = df["loan_type"].dropna().value_counts()

    if not loan_type_counts.empty:
        top_loan_type = loan_type_counts.index[0]
        top_loan_type_share = loan_type_counts.iloc[0] / total_records * 100
    else:
        top_loan_type = "Not available"
        top_loan_type_share = 0

    risk_data = df["risk_grade"].dropna()
    risk_e_share = (
        risk_data.eq("E").mean() * 100
        if not risk_data.empty else 0)

    status_normalized = (df["loan_status"].fillna("").astype(str).str.strip().str.lower())

    default_written_off = status_normalized.isin(["defaulted", "written off"])

    default_written_off_share = (
        default_written_off.mean() * 100
        if total_records > 0 else 0)

    # Affordability-related descriptive measures
    median_dti = df["debt_to_income_pct"].median()
    dti_75th_percentile = df["debt_to_income_pct"].quantile(0.75)

    valid_income = df.loc[df["annual_income_egp"].notna() & (df["annual_income_egp"] > 0), ["loan_amount_egp", "annual_income_egp"]].copy()

    valid_income["loan_to_income_ratio"] = (valid_income["loan_amount_egp"] / valid_income["annual_income_egp"])

    median_loan_to_income = valid_income["loan_to_income_ratio"].median()

    # Credit score and pricing by risk grade
    median_score_a = df.loc[df["risk_grade"] == "A", "credit_score"].median()

    median_score_e = df.loc[df["risk_grade"] == "E", "credit_score"].median()

    median_rate_a = df.loc[df["risk_grade"] == "A", "interest_rate_pct"].median()

    median_rate_e = df.loc[df["risk_grade"] == "E", "interest_rate_pct"].median()

    # Portfolio status by loan type
    status_by_type = (df.assign(_status=status_normalized).groupby("loan_type")["_status"]
                      .apply(lambda values: values.isin(["defaulted", "written off"])
                             .mean() * 100).dropna().sort_values(ascending=False))

    # Origination activity over time
    yearly_activity = (df.assign(_year=df["origination_date"].dt.year).dropna(subset=["_year"]).groupby("_year")
                       .agg(record_count=("loan_amount_egp", "size"), total_amount=("loan_amount_egp", "sum")).sort_index())

    # Expected maturity profile
    maturity_years = df["expected_end_year"].dropna()

    # ============================================================
    # BUSINESS insight 1: CUSTOMER PROFILE & FINANCING DEMAND
    # ============================================================

    st.header("1. Customer Profile & Financing Demand")

    col1, col2, col3 = st.columns(3)

    col1.metric("Portfolio Records", f"{total_records:,}")
    col2.metric(
        "Median Customer Age",
        f"{median_age:.0f}" if pd.notna(median_age) else "N/A")
    col3.metric("Median Loan Amount", f"EGP {median_loan_amount:,.0f}"
                if pd.notna(median_loan_amount) else "N/A")

    st.markdown(
        f"""The portfolio contains **{total_records:,} records**, with a median
        customer age of **{median_age:.0f} years**
        and a median loan amount of **EGP {median_loan_amount:,.0f}**."""

        if pd.notna(median_age) and pd.notna(median_loan_amount)
        else f"The portfolio contains **{total_records:,} records**. "
             f"Some customer or financing statistics are unavailable.")

    if pd.notna(median_income):
        st.write(f"The median annual customer income is "
                 f"**EGP {median_income:,.0f}**.")

    st.write(f"**{top_loan_type}** is the most frequently represented loan type, "
             f"accounting for approximately **{top_loan_type_share:.1f}%** "
             f"of all portfolio records.")

    st.markdown(
        "**Business perspective:** These measures describe the customer "
        "profile and the financing products most represented in the dataset. "
        "They provide context for interpreting the portfolio's credit and "
        "affordability characteristics. ")

    st.divider()

    # ============================================================
    # BUSINESS insight 2: CREDIT QUALITY & PRICING
    # ============================================================

    st.header("2. Credit Quality & Pricing")

    col1, col2 = st.columns(2)

    col1.metric("Risk Grade E Share", f"{risk_e_share:.1f}%")
    col2.metric("Total Portfolio Loan Value", f"EGP {total_loan_value:,.0f}")

    if pd.notna(median_score_a) and pd.notna(median_score_e):
        st.write(f"The median credit score is **{median_score_a:.0f}** "
                 f"for Grade A records and **{median_score_e:.0f}** "
                 f"for Grade E records.")

    if pd.notna(median_rate_a) and pd.notna(median_rate_e):
        st.write(f"The median interest rate is **{median_rate_a:.2f}%** "
                 f"for Grade A and **{median_rate_e:.2f}%** for Grade E.")

    st.markdown(
        "**Business perspective:** Considering credit scores, risk grades, "
        "and interest rates together provides a broader view of the portfolio's "
        "credit profile and pricing structure. Differences between groups are "
        "descriptive relationships and do not, by themselves, establish "
        "causation. ")

    st.divider()

    # ============================================================
    # BUSINESS insight 3: PORTFOLIO STATUS & CREDIT OUTCOMES
    # ============================================================

    st.header("3. Portfolio Status & Credit Outcomes")

    st.metric("Defaulted or Written-Off Records", f"{default_written_off_share:.1f}%")

    if not status_by_type.empty:
        highest_status_type = status_by_type.index[0]
        highest_status_share = status_by_type.iloc[0]

        st.write(f"Across loan types, **{highest_status_type}** has the highest "
                 f"share of records classified as defaulted or written off, "
                 f"at **{highest_status_share:.1f}%**.")

    st.markdown(
        "**Business perspective:** Overall loan status and differences "
        "between loan types help describe how the portfolio is distributed "
        "across its recorded lifecycle outcomes. These figures should be "
        "interpreted alongside the size and composition of each loan segment. ")

    st.divider()

    # ============================================================
    # BUSINESS insight 4: AFFORDABILITY & LENDING EXPOSURE
    # ============================================================

    st.header("4. Affordability & Lending Exposure")

    col1, col2 = st.columns(2)

    col1.metric("Median Debt-to-Income Ratio",
                f"{median_dti:.1f}%"
                if pd.notna(median_dti) else "N/A")

    col2.metric("75th Percentile Debt-to-Income", f"{dti_75th_percentile:.1f}%"
                if pd.notna(dti_75th_percentile) else "N/A")

    if pd.notna(median_loan_to_income):
        st.write(f"The median loan amount divided by annual income is "
                 f"**{median_loan_to_income:.2f} times** among records with "
                 f"a positive, available annual income.")

    st.markdown(
        "**Business perspective:** Loan size, annual income, and the reported "
        "debt-to-income ratio provide complementary views of customer "
        "financing exposure. The distribution is important: a median alone "
        "does not capture customers with substantially higher reported ratios. "
        "These indicators should be interpreted as descriptive measures, "
        "not as a standalone credit decision. ")

    st.divider()

    # ============================================================
    # BUSINESS insight 5: PORTFOLIO EVOLUTION & MATURITY
    # ============================================================

    st.header("5. Portfolio Evolution & Long-Term Commitments")

    if not yearly_activity.empty:
        first_year = int(yearly_activity.index.min())
        last_year = int(yearly_activity.index.max())

        first_year_records = int(yearly_activity.loc[first_year, "record_count"])
        last_year_records = int(yearly_activity.loc[last_year, "record_count"])

        col1, col2 = st.columns(2)

        col1.metric(f"Records Originated in {first_year}", f"{first_year_records:,}")

        col2.metric(f"Records Originated in {last_year}", f"{last_year_records:,}")

        st.write(f"The available origination data spans **{first_year}-{last_year}**. "
                 f"Recorded loan amounts totalled **EGP "
                 f"{yearly_activity['total_amount'].sum():,.0f}** across this period.")

    if not maturity_years.empty:
        most_common_maturity = int(maturity_years.mode().iloc[0])

        st.write(
            f"Expected loan end years range from **{int(maturity_years.min())}** "
            f"to **{int(maturity_years.max())}**, with **{most_common_maturity}** "
            "being the most frequently recorded expected end year. ")

    st.markdown(
        "**Business perspective:** Origination activity describes how lending "
        "has been recorded over time, while expected end years provide a "
        "forward-looking view of scheduled loan maturities. Together, these "
        "measures describe both historical lending activity and the timing "
        "of expected portfolio commitments. ")

    st.divider()

    st.caption(
        "All statistics above are calculated from the dataset loaded by the app. "
        "The findings describe the available records and should be interpreted "
        "within the dataset's scope and limitations. ")