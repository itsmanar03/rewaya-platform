import streamlit as st

from database.database import (
    get_projects,
    save_logical_framework,
    get_logical_framework
)


def show_logical_framework():

    with open(
    "assets/logical_framework.css",
    encoding="utf-8"
) as f:

        st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

    st.markdown("""
<div class='framework-title'>
    الإطار المنطقي
</div>

<div class='framework-subtitle'>
    إدارة وربط المدخلات والأنشطة والمخرجات والتغيرات والأثر للمشروع
</div>
""", unsafe_allow_html=True)
    projects = get_projects()

    if not projects:
        st.warning("يجب إضافة مشروع أولاً")
        return

    project_names = {
        p[1]: p[0]
        for p in projects
    }

    selected_project = st.selectbox(
        "اختر المشروع",
        list(project_names.keys())
    )

    project_id = project_names[selected_project]

    existing = get_logical_framework(project_id)

    inputs = ""
    activities = ""
    outputs = ""

    short_term_change = ""
    medium_term_change = ""
    long_term_change = ""

    impact = ""

    assumptions = ""
    risks = ""

    if existing:

        inputs = existing[2] or ""

        activities = existing[3] or ""

        outputs = existing[4] or ""

        short_term_change = existing[5] or ""

        medium_term_change = existing[6] or ""

        long_term_change = existing[7] or ""

        impact = existing[8] or ""

        assumptions = existing[9] or ""

        risks = existing[10] or ""

    st.divider()
    with st.form("logical_framework_form"):

        with st.expander("📥 المدخلات والمخرجات", expanded=True):

            inputs = st.text_area(
            "المدخلات",
            value=inputs,
            height=120
        )

            activities = st.text_area(
            "الأنشطة",
            value=activities,
            height=120
        )

            outputs = st.text_area(
            "المخرجات",
            value=outputs,
            height=120
        )


        with st.expander("⚙️ التغيرات والنتائج"):

            short_term_change = st.text_area(
            "التغيرات قصيرة المدى",
            value=short_term_change,
            height=100
        )

            medium_term_change = st.text_area(
            "التغيرات متوسطة المدى",
            value=medium_term_change,
            height=100
        )

            long_term_change = st.text_area(
            "التغيرات طويلة المدى",
            value=long_term_change,
            height=100
        )

        with st.expander("🌍 الأثر النهائي"):


            impact = st.text_area(
            "الأثر النهائي",
            value=impact,
            height=120
        )

        with st.expander("⚠️ الافتراضات والمخاطر"):

            assumptions = st.text_area(
            "الافتراضات",
            value=assumptions,
            height=100
        )

            risks = st.text_area(
            "المخاطر",
            value=risks,
            height=100
        )

        submitted = st.form_submit_button(
            "حفظ الإطار المنطقي"
        )

        if submitted:

            save_logical_framework(
                project_id,
                inputs,
                activities,
                outputs,
                short_term_change,
                medium_term_change,
                long_term_change,
                impact,
                assumptions,
                risks
            )

            st.success(
                "تم حفظ الإطار المنطقي بنجاح"
            )

            st.rerun()

    st.divider()
    
    st.subheader("ملخص الإطار المنطقي")

    with st.expander("📥 المدخلات", expanded=True):
        st.write(inputs or "-")

    with st.expander("⚙️ الأنشطة"):
        st.write(activities or "-")

    with st.expander("📦 المخرجات"):
        st.write(outputs or "-")

    with st.expander("📈 التغيرات قصيرة المدى"):
        st.write(short_term_change or "-")

    with st.expander("📊 التغيرات متوسطة المدى"):
        st.write(medium_term_change or "-")

    with st.expander("🚀 التغيرات طويلة المدى"):
        st.write(long_term_change or "-")

    with st.expander("🌍 الأثر النهائي"):
        st.write(impact or "-")

    with st.expander("✅ الافتراضات"):
        st.write(assumptions or "-")

    with st.expander("⚠️ المخاطر"):
        st.write(risks or "-")