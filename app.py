import streamlit as st

from modules.dashboard import show_dashboard
from modules.projects import show_projects
from modules.logical_framework import show_logical_framework
from database.database import login_user
from modules.reports import show_reports
from modules.kpis import show_kpis
from modules.users import show_users
from modules.archived_projects import show_archived_projects
from modules.activity_logs import show_activity_logs
from modules.notifications import show_notifications

from database.database import (
    create_tables,
    create_default_admin,
    create_projects_table,
    create_logical_framework_table,
    create_kpis_table,
    initialize_database
)

# ==========================================
# DATABASE INIT
# ==========================================

create_tables()
create_default_admin()
create_projects_table()
create_logical_framework_table()
create_kpis_table()

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="روايـة",
    page_icon="assets/favicon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

initialize_database()

# ==========================================
# SESSION
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# LOGIN PAGE
# ==========================================

if not st.session_state.logged_in:

    with open(
        "assets/login.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )



    logo_left, logo_center, logo_right = st.columns([1,1,1])

    with logo_center:

        st.image(
            "assets/logo_used.png"
        )

    left, center, right = st.columns([1, 2.5, 1])

    with center:

        st.markdown("""
        <div class="hero-title">
        منصـة روايـة
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-subtitle">
        منصة إدارة المشاريع والتقارير التنموية الذكية
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="hero-desc">
        منصة موحدة لإدارة المشاريع والبرامج والمبادرات التنموية
        وإنتاج التقارير التنفيذية وتقارير الأثر بشكل ذكي وآلي
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            """
        <div style="
            text-align:right;
            color:#C4B5FD;
            font-weight:600;
            margin-bottom:5px;
        ">
        البريد الإلكتروني
        </div>
        """,
            unsafe_allow_html=True
        )

        email = st.text_input(
            "",
            placeholder="",
            label_visibility="collapsed"
        )

        st.markdown(
            """
            <div style="
                text-align:right;
                color:#C4B5FD;
                font-weight:600;
                margin-bottom:5px;
                margin-top:10px;
            ">
            كلمة المرور
            </div>
            """,
            unsafe_allow_html=True
        )

        password = st.text_input(
            "",
            type="password",
            placeholder="",
            label_visibility="collapsed"
        )

        st.markdown(
            """
            <div style="
                text-align:right;
                color:#C4B5FD;
                font-weight:600;
                margin-bottom:5px;
                margin-top:10px;
            ">
            الدور الوظيفي
            </div>
            """,
            unsafe_allow_html=True
        )

        role = st.selectbox(
            "",
            [
                "مدير النظام",
                "مدير قسم",
                "موظف"
            ],
            label_visibility="collapsed"
        )

        if st.button(
            "تسجيل الدخول",
            use_container_width=True
        ):

            user = login_user(
                email,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.user_role = user[3]
                st.session_state.user_email = user[1]

                st.success(
                    "تم تسجيل الدخول بنجاح"
                )

                st.rerun()

            else:

                st.error(
                    "البريد الإلكتروني أو كلمة المرور غير صحيحة"
                )


# ==========================================
# MAIN APP
# ==========================================

else:

    with open(
        "assets/sidebar.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.sidebar.image(
        "assets/logo_used.png",
        use_container_width=220
    )

    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)

    unread_notifications = 0

    role = st.session_state.user_role

    if role == "مدير النظام":

        pages = [
            "لوحة التحكم",
            "المشاريع",
            "أرشيف المشاريع",
            "الإطار المنطقي",
            "المؤشرات",
            "التقارير",
            "الإشعارات",
            "إدارة المستخدمين",
            "سجل العمليات"
        ]

    elif role == "مدير قسم":

        pages = [
            "لوحة التحكم",
            "المشاريع",
            "الإطار المنطقي",
            "المؤشرات",
            "التقارير"
        ]

    else:

        pages = [
            "المشاريع",
            "المؤشرات"
        ]

    page = st.sidebar.radio(
        "",
        pages,
        label_visibility="collapsed"
    )

    st.sidebar.divider()

    if st.sidebar.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()

    if page == "لوحة التحكم":
        show_dashboard()

    elif page == "المشاريع":
        show_projects()

    elif page == "الإطار المنطقي":
        show_logical_framework()

    elif page == "المؤشرات":
        show_kpis()

    elif page == "التقارير":
        show_reports()

    elif page == "إدارة المستخدمين":
        show_users()

    elif page == "الإشعارات":
        show_notifications()

    elif page == "سجل العمليات":
        show_activity_logs()

    elif page == "أرشيف المشاريع":
        show_archived_projects()