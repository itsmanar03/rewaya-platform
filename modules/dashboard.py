import streamlit as st
import pandas as pd
import plotly.express as px

from database.database import (
    get_projects_count,
    get_total_budget,
    get_total_beneficiaries,
    get_total_volunteers,
    get_projects,
    get_all_kpis,
    get_average_kpi_achievement,
    get_projects_by_status
)

def show_dashboard():

    with open(
        "assets/dashboard.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="dashboard-title" style="text-align:center;">
    لوحة التحكم
    </div>

    <div class="dashboard-subtitle" style="text-align:center;">
    نظرة شاملة على المشاريع والمؤشرات والتقارير التنموية
    </div>
    """, unsafe_allow_html=True)


    stakeholder_view = st.selectbox(
        "عرض اللوحة حسب صاحب المصلحة",
        [
            "الكل",
            "مجلس الإدارة",
            "الجهة الإشرافية",
            "الداعم",
            "الشريك الاستراتيجي",
            "المجتمع المحلي",
            "المستفيدون",
            "الإدارة التنفيذية",
            "فريق المشروع",
            "المتطوعون",
            "فريق قياس الأثر"
        ]
    )

    # ==========================================
    # KPIs
    # ==========================================

    total_projects = get_projects_count()

    total_budget = get_total_budget()

    total_beneficiaries = get_total_beneficiaries()

    total_volunteers = get_total_volunteers()

    kpis = get_all_kpis()

    if stakeholder_view != "الكل":

        filtered_kpis = []

        for kpi in kpis:

            if len(kpi) > 9 and kpi[9] == stakeholder_view:

                filtered_kpis.append(kpi)

        kpis = filtered_kpis

    total_kpis = len(kpis)

    average_achievement = (
        get_average_kpi_achievement()
    )


    green_kpis = 0
    yellow_kpis = 0
    red_kpis = 0

    for kpi in kpis:

        target = kpi[3] or 0
        actual = kpi[4] or 0

        percentage = 0

        if target > 0:
            percentage = (
                actual / target
            ) * 100

        if percentage >= 80:
            green_kpis += 1

        elif percentage >= 50:
            yellow_kpis += 1

        else:
            red_kpis += 1


    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي المشاريع</div>
            <div class="kpi-value">{total_projects}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي المستفيدين</div>
            <div class="kpi-value">{total_beneficiaries}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي المتطوعين</div>
            <div class="kpi-value">{total_volunteers}</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي الميزانية</div>
            <div class="kpi-value">{total_budget:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">إجمالي المؤشرات</div>
            <div class="kpi-value">{total_kpis}</div>
        </div>
        """, unsafe_allow_html=True)

    with col6:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">متوسط الإنجاز</div>
            <div class="kpi-value">{average_achievement}%</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.subheader("لوحة متابعة المؤشرات")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🟢 مؤشرات ممتازة</div>
            <div class="kpi-value">{green_kpis}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🟡 مؤشرات متوسطة</div>
            <div class="kpi-value">{yellow_kpis}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🔴 مؤشرات تحتاج متابعة</div>
            <div class="kpi-value">{red_kpis}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">متوسط الإنجاز</div>
            <div class="kpi-value">{average_achievement}%</div>
        </div>
        """, unsafe_allow_html=True)
        

    st.markdown("<div style='height:20px'></div>",
                unsafe_allow_html=True)

    if average_achievement >= 80:

        st.success(
            "الحالة العامة للمشاريع ممتازة"
        )

    elif average_achievement >= 50:

        st.warning(
            "الحالة العامة جيدة وتحتاج بعض التحسين"
        )

    else:

        st.error(
            "الحالة العامة تحتاج متابعة عاجلة"
        )


    # ==========================================
    # PROJECT STATUS CHART
    # ==========================================

    st.subheader("المشاريع حسب الحالة")

    status_data = get_projects_by_status()

    if status_data:


        status_df = pd.DataFrame(
            status_data,
            columns=[
                "الحالة",
                "العدد"
            ]
        )

        fig = px.bar(
            status_df,
            x="الحالة",
            y="العدد",
            title=" ",
            color_discrete_sequence=["#A855F7"]
        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#F8FAFC"
            ),

            title_font=dict(
                color="#F8FAFC"
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    # ==========================================
    # PROJECTS TABLE
    # ==========================================

    st.subheader("المشاريع المسجلة")

    projects = get_projects()

    if projects:

        projects_table = []

        for project in projects:

            projects_table.append({

                "اسم المشروع": project[1],
                "الحالة": project[7],
                "مدير المشروع": project[5],
                "الميزانية": project[10],
                "عدد المستفيدين": project[12]

            })

        st.data_editor(
            pd.DataFrame(projects_table),
            width="stretch",
            disabled=True,
            hide_index=True
        )

    else:

        st.info(
            "لا توجد مشاريع مسجلة حتى الآن"
        )

    st.divider()

    # ==========================================
    # SUMMARY
    # ==========================================

    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader("ملخص الأداء")

    if projects:

        target_beneficiaries = 0
        actual_beneficiaries = 0

        target_volunteers = 0
        actual_volunteers = 0

        for project in projects:

            target_beneficiaries += project[11] or 0
            actual_beneficiaries += project[12] or 0

            target_volunteers += project[13] or 0
            actual_volunteers += project[14] or 0

        summary_df = pd.DataFrame({

            "المؤشر": [
                "المستفيدون",
                "المتطوعون"
            ],

            "المستهدف": [
                target_beneficiaries,
                target_volunteers
            ],

            "المتحقق": [
                actual_beneficiaries,
                actual_volunteers
            ]

        })

        st.data_editor(
            summary_df,
            width='stretch',
            disabled=True,
            hide_index=True
        )

    else:

        st.info(
            "لا توجد بيانات كافية لعرض ملخص الأداء"
        )


    st.divider()

    st.subheader("تحليل المستفيدين والمتطوعين")

    if projects:

        comparison_people = pd.DataFrame({

            "الفئة": [
                "المستفيدون",
                "المتطوعون"
            ],

            "القيمة": [
                total_beneficiaries,
                total_volunteers
            ]

        })

        fig = px.bar(

            comparison_people,

            x="الفئة",

            y="القيمة",

            color="الفئة",

            color_discrete_sequence=[
                "#A855F7",
                "#C084FC"
            ]

        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#F8FAFC"
            ),

            height=450,

            showlegend=False

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("تحليل المؤشرات حسب مستوى الإطار")

    if kpis:

        framework_data = {}

        for kpi in kpis:

            level = kpi[7] or "غير محدد"

            framework_data[level] = (
                framework_data.get(level, 0) + 1
            )

        framework_df = pd.DataFrame({

            "المستوى": list(
                framework_data.keys()
            ),

            "عدد المؤشرات": list(
                framework_data.values()
            )

        })

        fig = px.pie(
            framework_df,
            names="المستوى",
            values="عدد المؤشرات",
            title=" ",
            color_discrete_sequence=[
            "#7C3AED",
            "#A855F7",
            "#C084FC",
            "#D4B483"
            ]
        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#F8FAFC"
            ),

            title_font=dict(
                color="#F8FAFC"
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("تحليل أصحاب المصلحة")

    if kpis:

        stakeholder_data = {}

        for kpi in kpis:

            stakeholder = kpi[9] or "غير محدد"

            stakeholder_data[stakeholder] = (
                stakeholder_data.get(
                    stakeholder,
                    0
                ) + 1
            )

        stakeholder_df = pd.DataFrame({

            "صاحب المصلحة": list(
                stakeholder_data.keys()
            ),

            "عدد المؤشرات": list(
                stakeholder_data.values()
            )

        })

        fig = px.bar(
            stakeholder_df,
            x="صاحب المصلحة",
            y="عدد المؤشرات",
            title=" ",
            color_discrete_sequence=["#A855F7"]
        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#F8FAFC"
            ),

            title_font=dict(
                color="#F8FAFC"
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.divider()

    st.subheader("المؤشرات المتعثرة")

    delayed = []

    for kpi in kpis:

        target = kpi[3] or 0
        actual = kpi[4] or 0

        if target > 0:

            achievement = (
                actual / target
            ) * 100

            if achievement < 50:

                delayed.append({

                    "المؤشر": kpi[2],

                    "الإنجاز": round(
                        achievement,
                        1
                    ),

                    "صاحب المصلحة": kpi[9],

                    "المستوى": kpi[7]

                })

    if delayed:

        st.data_editor(
            pd.DataFrame(delayed),
            width='stretch',
            disabled=True,
            hide_index=True
        )

    else:

        st.success(
            "لا توجد مؤشرات متعثرة"
        )

    st.divider()

    st.subheader("الاستنتاجات والتوصيات الذكية")

    if red_kpis > green_kpis:

        st.error(
            "يوجد عدد كبير من المؤشرات المتعثرة ويُنصح بمراجعة خطط التنفيذ."
        )

    elif yellow_kpis > green_kpis:

        st.warning(
            "بعض المؤشرات تحتاج إلى متابعة وتحسين لتحقيق المستهدفات."
        )

    else:

        st.success(
            "معظم المؤشرات تسير وفق المستهدفات المخططة."
        )

    if average_achievement < 50:

        st.warning(
            "يوصى بإعداد خطة تصحيحية عاجلة للمؤشرات منخفضة الإنجاز."
        )

    elif average_achievement < 80:

        st.info(
            "يوصى بمراجعة أسباب الانحراف وتحسين الأداء التشغيلي."
        )

    else:

        st.success(
            "مستوى الإنجاز مرتفع ويُنصح بالتركيز على الاستدامة والتوسع."
        )

    if projects:

        comparison_df = pd.DataFrame({

            "الفئة": [
                "المستفيدون المستهدفون",
                "المستفيدون المتحققون",
                "المتطوعون المستهدفون",
                "المتطوعون المتحققون"
            ],

            "القيمة": [
                target_beneficiaries,
                actual_beneficiaries,
                target_volunteers,
                actual_volunteers
            ]

        })

        fig = px.bar(
            comparison_df,
            x="الفئة",
            y="القيمة",
            title=" ",
            color_discrete_sequence=["#A855F7"]
        )

        fig.update_layout(

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)",

            font=dict(
                color="#F8FAFC"
            ),

            title_font=dict(
                color="#F8FAFC"
            )

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
