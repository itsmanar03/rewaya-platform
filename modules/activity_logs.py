import streamlit as st

from database.database import (
    get_activity_logs
)

def show_activity_logs():

    with open(
        "assets/activity_logs.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="logs-title">
        سجل العمليات
    </div>

    <div class="logs-subtitle">
        متابعة جميع الأنشطة والإجراءات المنفذة داخل النظام
    </div>
    """, unsafe_allow_html=True)


    logs = get_activity_logs()

    if not logs:

        st.info(
            "لا توجد عمليات مسجلة"
        )

        return
    
    
    for log in logs:


        st.markdown(
            f"""
        <div class="log-card">

        <div class="log-date">
        {log[4]}
        </div>

        <div class="log-item">
        <b>العملية:</b> {log[1]}
        </div>

        <div class="log-item">
        <b>النوع:</b> {log[2]}
        </div>

        <div class="log-item">
        <b>العنصر:</b> {log[3]}
        </div>

        </div>
        """,
            unsafe_allow_html=True
        )