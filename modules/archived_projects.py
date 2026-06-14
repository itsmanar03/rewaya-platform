import streamlit as st

from database.database import (
    get_archived_projects,
    restore_project,
    delete_project
)

with open(
    "assets/archived_projects.css",
    encoding="utf-8"
) as f:

    ARCHIVE_CSS = f.read()

def show_archived_projects():

    st.markdown(
        f"<style>{ARCHIVE_CSS}</style>",
        unsafe_allow_html=True
    )


    st.markdown(
    """
    <div class='archive-title'>
        أرشيف المشاريع
    </div>

    <div class='archive-subtitle'>
        المشاريع التي تم أرشفتها ويمكن استعادتها أو حذفها نهائياً
    </div>
    """,
        unsafe_allow_html=True
    )

    projects = get_archived_projects()

    total_archived = len(projects)



    c0, c1, c2, c3, c4 = st.columns([1,2,2,2,1])

    with c1:

        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">المشاريع المؤرشفة</div>
        <div class="kpi-value">{total_archived}</div>
    </div>
    """, unsafe_allow_html=True)

    with c2:

        completed_count = len(
        [
            p for p in projects
            if p[7] == "مكتمل"
        ]
    )

        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">المشاريع المكتملة</div>
        <div class="kpi-value">{completed_count}</div>
    </div>
    """, unsafe_allow_html=True)

    with c3:

        stopped_count = len(
        [
            p for p in projects
            if p[7] == "متوقف"
        ]
    )

        st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">المشاريع المتوقفة</div>
        <div class="kpi-value">{stopped_count}</div>
    </div>
    """, unsafe_allow_html=True)



    st.divider()


    if not projects:

        st.info(
            "لا توجد مشاريع مؤرشفة"
        )

        return

    # ==========================================
    # FILTERS
    # ==========================================

    search_text = st.text_input(
        "البحث باسم المشروع"
    )

    col1, col2 = st.columns(2)

    with col1:

        status_filter = st.selectbox(
            "فلترة حسب الحالة",
            [
                "الكل",
                "قيد التخطيط",
                "قيد التنفيذ",
                "مكتمل",
                "متوقف"
            ]
        )

    with col2:

        sector_filter = st.text_input(
            "فلترة حسب المجال"
        )

    # ==========================================
    # PROJECTS
    # ==========================================

    for project in projects:

        if not project[1]:
            continue

        # Search Filter

        if search_text:

            if search_text.lower() not in str(
                project[1]
            ).lower():

                continue

        # Status Filter

        if status_filter != "الكل":

            if project[7] != status_filter:

                continue

        # Sector Filter

        if sector_filter:

            if sector_filter.lower() not in str(
                project[3]
            ).lower():

                continue

        project_id = project[0]

        with st.expander(
            f"📁 {project[1]}",
            expanded=False
        ):

            m1, m2, m3 = st.columns(3)

            with m1:

                st.metric(
            "الحالة",
            project[7]
        )

            with m2:

                st.metric(
                "المجال",
                project[3]
                )

            with m3:

                st.metric(
                    "الميزانية",
                    f"{project[10]:,.0f}"
                )


            st.write(
                f"سبب الأرشفة: {project[69] or '-'}"
            )

            st.write(
                f"تمت الأرشفة بواسطة: {project[70] or '-'}"
            )

            st.write(
                f"تاريخ الأرشفة: {project[71] or '-'}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "استعادة المشروع",
                    key=f"restore_{project_id}"
                ):

                    restore_project(
                        project_id
                    )

                    st.success(
                        "تمت استعادة المشروع"
                    )

                    st.rerun()

            with col2:

                if st.button(
                    "حذف نهائي",
                    key=f"delete_archived_{project_id}"
                ):

                    delete_project(
                        project_id
                    )

                    st.success(
                        "تم حذف المشروع نهائياً"
                    )

                    st.rerun()