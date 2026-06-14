import streamlit as st

from database.database import (
    get_notifications,
    mark_notification_as_read,
    mark_all_notifications_as_read
)

def show_notifications():

    with open(
        "assets/notifications.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="notifications-title">
        الإشعارات
    </div>

    <div class="notifications-subtitle">
        متابعة جميع تنبيهات النظام والأنشطة الأخيرة
    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "تحديد الكل كمقروء"
    ):

        mark_all_notifications_as_read()

        st.success(
            "تم تحديث جميع الإشعارات"
        )

        st.rerun()

    notifications = get_notifications()

    if not notifications:

        st.info(
            "لا توجد إشعارات"
        )

        return

    for notification in notifications:

        status = "🔴 غير مقروء"

        if notification[4] == 1:

            status = "🟢 مقروء"

        with st.expander(
            f"{status} - {notification[1]}"
        ):

            st.write(
                f"التاريخ: {notification[3]}"
            )

            st.write(
                notification[2]
            )

            if notification[4] == 0:

                if st.button(
                    "تحديد كمقروء",
                    key=f"read_{notification[0]}"
                ):

                    mark_notification_as_read(
                        notification[0]
                    )

                    st.rerun()