import streamlit as st

from database.database import (
    get_projects,
    add_kpi,
    get_kpis,
    delete_kpi,
    update_kpi
)

def show_kpis():

    with open(
    "assets/kpis.css",
    encoding="utf-8"
    ) as f:

        st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
        )

    st.markdown(
"""
<div class='kpis-title'>
    المؤشرات
</div>

<div class='kpis-subtitle'>
    إدارة ومتابعة مؤشرات الأداء والنتائج والأثر للمشاريع
</div>
""",
    unsafe_allow_html=True
)

    projects = get_projects()

    if not projects:

        st.warning(
            "يجب إضافة مشروع أولاً"
        )
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


    kpis = get_kpis(project_id)

    total_kpis = len(kpis)

    excellent_kpis = 0
    medium_kpis = 0
    poor_kpis = 0

    for kpi in kpis:

        target_value = kpi[3]
        actual_value = kpi[4]

        percentage = 0

        if target_value > 0:

            percentage = (
                actual_value
                / target_value
            ) * 100

        if percentage >= 80:

            excellent_kpis += 1

        elif percentage >= 50:

            medium_kpis += 1

        else:

            poor_kpis += 1


    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                إجمالي المؤشرات
            </div>
            <div class="kpi-value">
                {total_kpis}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                مؤشرات ممتازة
            </div>
            <div class="kpi-value">
                {excellent_kpis}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                مؤشرات متوسطة
            </div>
            <div class="kpi-value">
                {medium_kpis}
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">
                تحتاج متابعة
            </div>
            <div class="kpi-value">
                {poor_kpis}
            </div>
        </div>
        """, unsafe_allow_html=True)


    st.divider()


    framework_levels = [
        "المخرجات",
        "التغيرات قصيرة المدى",
        "التغيرات متوسطة المدى",
        "التغيرات طويلة المدى",
        "الأثر"
    ]

    stakeholders = [
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


    st.markdown(
"""
<div class='section-title'>
    إضافة مؤشر جديد
</div>
""",
unsafe_allow_html=True
)

    with st.container(border=True):

        with st.form("kpi_form"):

            indicator_name = st.text_input(
            "اسم المؤشر"
        )

            framework_level = st.selectbox(
            "مرتبط بأي مستوى؟",
            framework_levels
        )

            linked_element = st.text_input(
            "العنصر المرتبط من الإطار المنطقي"
        )

            stakeholder_priority = st.selectbox(
            "صاحب المصلحة المستهدف",
            stakeholders
        )

            target_value = st.number_input(
            "القيمة المستهدفة",
            min_value=0.0
        )

            actual_value = st.number_input(
            "القيمة المتحققة",
            min_value=0.0
        )

            unit = st.text_input(
            "وحدة القياس"
        )

            indicator_type = st.selectbox(
            "نوع المؤشر",
            [
                "مخرجات",
                "نتائج",
                "أثر",
                "تشغيلي",
                "مالي"
            ]
        )

            deviation_reason = st.text_area(
            "سبب الانحراف (إن وجد)"
        )

            submitted = st.form_submit_button(
            "حفظ المؤشر"
        )

            if submitted:

                add_kpi(
                project_id,
                indicator_name,
                target_value,
                actual_value,
                unit,
                indicator_type,
                framework_level,
                linked_element,
                stakeholder_priority,
                deviation_reason
            )

                st.success(
                "تم حفظ المؤشر"
            )

                st.rerun()


    st.divider()

    st.subheader("المؤشرات المسجلة")

    kpis = get_kpis(project_id)

    if kpis:

        for kpi in kpis:

            kpi_id = kpi[0]

            indicator_name = kpi[2]

            target_value = kpi[3]

            actual_value = kpi[4]

            unit = kpi[5]

            percentage = 0

            if target_value > 0:

                percentage = round(
                    (actual_value / target_value) * 100,
                1
            )

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">
                        📊 {indicator_name}
                    </div>
                    <div class="kpi-value">
                        {percentage}%
                    </div>
                    <div class="kpi-meta">
                        المستهدف: {target_value:,.0f} {unit}
                        <br>
                        المتحقق: {actual_value:,.0f} {unit}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )


            st.progress(
            min(
                percentage / 100,
                1.0
            )
        )

            if percentage >= 80:

                st.success(
                "🟢 الأداء ممتاز"
            )

            elif percentage >= 50:

                st.warning(
                "🟡 الأداء متوسط"
            )

            else:

                st.error(
                "🔴 الأداء يحتاج متابعة"
            )

            with st.expander("عرض التفاصيل"):

                st.write(
                f"نوع المؤشر: {kpi[6]}"
            )

                st.write(
                f"مستوى الإطار: {kpi[7] or '-'}"
            )

                st.write(
                f"العنصر المرتبط: {kpi[8] or '-'}"
            )

                st.write(
                f"صاحب المصلحة: {kpi[9] or '-'}"
            )

                st.write(
                f"سبب الانحراف: {kpi[10] or '-'}"
            )

            with st.expander("تعديل المؤشر"):

                new_name = st.text_input(
                "اسم المؤشر",
                value=indicator_name,
                key=f"name_{kpi_id}"
            )

                current_framework = kpi[7] or framework_levels[0]

                new_framework = st.selectbox(
                "مستوى الإطار",
                framework_levels,
                index=framework_levels.index(
                    current_framework
                )
                    if current_framework in framework_levels
                    else 0,
                    key=f"framework_{kpi_id}"
            )

                new_linked_element = st.text_input(
                    "العنصر المرتبط",
                    value=kpi[8] or "",
                    key=f"linked_{kpi_id}"
            )

                current_stakeholder = (
                    kpi[9]
                    if kpi[9] in stakeholders
                    else stakeholders[0]
            )

                new_stakeholder = st.selectbox(
                "صاحب المصلحة",
                stakeholders,
                index=stakeholders.index(
                    current_stakeholder
            ),
                key=f"stakeholder_{kpi_id}"
            )

                new_target = st.number_input(
                "القيمة المستهدفة",
                value=float(target_value),
                key=f"target_{kpi_id}"
            )

                new_actual = st.number_input(
                "القيمة المتحققة",
                value=float(actual_value),
                key=f"actual_{kpi_id}"
            )

                new_unit = st.text_input(
                "وحدة القياس",
                value=unit,
                key=f"unit_{kpi_id}"
            )

                current_type = kpi[6] if len(kpi) > 6 else "نتائج"

                types = [
                "مخرجات",
                "نتائج",
                "أثر",
                "تشغيلي",
                "مالي"
            ]

                new_type = st.selectbox(
                "نوع المؤشر",
                types,
                index=types.index(current_type),
                key=f"type_{kpi_id}"
            )

                new_reason = st.text_area(
                "سبب الانحراف",
                value=kpi[10] or "",
                key=f"reason_{kpi_id}"
            )

                if st.button(
                "حفظ التعديلات",
                key=f"save_kpi_{kpi_id}"
            ):

                    update_kpi(
                    kpi_id,
                    new_name,
                    new_target,
                    new_actual,
                    new_unit,
                    new_type,
                    new_framework,
                    new_linked_element,
                    new_stakeholder,
                    new_reason
                )

                    st.success(
                    "تم تحديث المؤشر"
                )

                    st.rerun()


            if st.button(
            "حذف المؤشر",
            key=f"delete_{kpi_id}"
        ):

                delete_kpi(
                kpi_id
            )

                st.success(
                "تم حذف المؤشر"
            )

                st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

    else:

        st.info(
        "لا توجد مؤشرات لهذا المشروع"
    )