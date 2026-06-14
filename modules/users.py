import streamlit as st

from database.database import (
    add_user,
    get_users,
    delete_user,
    update_user,
    toggle_user_status
)


def show_users():

    with open(
        "assets/users.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


    st.markdown("""
    <div class="users-title">
        إدارة المستخدمين
    </div>

    <div class="users-subtitle">
        إدارة الحسابات والصلاحيات وأدوار المستخدمين
    </div>
    """, unsafe_allow_html=True)


    st.subheader("إضافة مستخدم")

    with st.form("user_form"):

        email = st.text_input(
            "البريد الإلكتروني"
        )

        password = st.text_input(
            "كلمة المرور",
            type="password"
        )

        role = st.selectbox(
            "الدور",
            [
                "مدير النظام",
                "مدير قسم",
                "موظف"
            ]
        )

        submitted = st.form_submit_button(
            "إضافة المستخدم"
        )

        if submitted:

            add_user(
                email,
                password,
                role
            )

            st.success(
                "تم إضافة المستخدم"
            )

            st.rerun()

    st.divider()

    st.subheader("المستخدمون")

    users = get_users()

    if users:

        for user in users:

            user_id = user[0]
            with st.expander(
                f"{user[1]}"
            ):

                st.write(
                    f"الدور الحالي: {user[3]}"
                )

                user_status = 1

                if len(user) > 4:

                    user_status = user[4]

                st.write(
                    "الحالة: نشط"
                    if user_status
                    else "الحالة: معطل"
                )

                st.divider()

                new_email = st.text_input(
                    "البريد الإلكتروني",
                    value=user[1],
                    key=f"email_{user_id}"
                )

                new_role = st.selectbox(
                    "الدور",
                    [
                        "مدير النظام",
                        "مدير قسم",
                        "موظف"
                    ],
                    index=[
                        "مدير النظام",
                        "مدير قسم",
                        "موظف"
                    ].index(user[3]),
                    key=f"role_{user_id}"
                )

                if st.button(
                    "حفظ التعديلات",
                    key=f"save_user_{user_id}"
                ):

                    update_user(
                        user_id,
                        new_email,
                        new_role
                    )

                    st.success(
                        "تم تحديث المستخدم"
                    )

                    st.rerun()

                if st.button(
                    "تفعيل / تعطيل",
                    key=f"toggle_user_{user_id}"
                ):

                    toggle_user_status(
                        user_id,
                        user_status
                    )

                    st.success(
                        "تم تحديث حالة المستخدم"
                    )

                    st.rerun()

                if st.button(
                    "حذف المستخدم",
                    key=f"delete_user_{user_id}"
                ):

                    delete_user(
                        user_id
                    )

                    st.success(
                        "تم حذف المستخدم"
                    )

                    st.rerun()
                    
    else:

        st.info(
            "لا يوجد مستخدمون"
        )