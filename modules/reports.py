import streamlit as st

from modules.pdf_generator import (
    generate_text_report
)

from database.database import (
    get_projects_count,
    get_total_budget,
    get_total_beneficiaries,
    get_total_volunteers,
    get_projects,
    get_total_kpis,
    get_average_kpi_achievement,
    get_all_kpis,
    get_project_by_id,
    get_logical_framework,
    get_kpis
)

from modules.word_generator import (
    generate_word_report
)

from modules.excel_generator import (
    generate_excel_report
)

def show_reports():

    with open(
        "assets/reports.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class='reports-title'>
        التقارير
    </div>

    <div class='reports-subtitle'>
        إنشاء وتصدير التقارير الذكية والتقارير المخصصة لأصحاب المصلحة
    </div>
    """, unsafe_allow_html=True)

    projects = get_projects()

    project_names = {
        p[1]: p[0]
        for p in projects
    }

    selected_project = st.selectbox(
        "المشروع",
        list(project_names.keys())
    )

    project_id = project_names[selected_project]

    project = get_project_by_id(
        project_id
    )

    logical_framework = get_logical_framework(
        project_id
    )

    project_kpis = get_kpis(
        project_id
    )

    stakeholder = st.selectbox(
        "صاحب المصلحة",
        [
            "عام",
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

    report_type = st.selectbox(
        "نوع التقرير",
        [   
            "التقرير التنفيذي",
            "تقرير الداعمين",
            "تقرير الأثر",
            "تقرير الإدارة التنفيذية",
            "تقرير مجلس الإدارة",
            "تقرير الشركاء"
        ]
    )

    st.divider()

    total_projects = get_projects_count()

    total_budget = get_total_budget()

    total_beneficiaries = get_total_beneficiaries()

    total_volunteers = get_total_volunteers()

    projects = get_projects()

    kpis = get_all_kpis()

    # ==========================================
    # EXECUTIVE REPORT
    # ==========================================

    if report_type == "التقرير التنفيذي":

        st.markdown(f"""
        <div class="report-card">

        <h3>ملخص تنفيذي</h3>

        <p><b>اسم المشروع:</b> {project[1]}</p>

        <p><b>الحالة:</b> {project[7]}</p>

        <p><b>مدير المشروع:</b> {project[5]}</p>

        <p><b>الميزانية:</b> {project[10]:,.0f}</p>

        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="dashboard-kpi-title">
                    عدد المشاريع
                </div>
                <div class="dashboard-kpi-value">
                    {total_projects}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="dashboard-kpi-title">
                    إجمالي المستفيدين
                </div>
                <div class="dashboard-kpi-value">
                    {total_beneficiaries:,}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="dashboard-kpi-title">
                    إجمالي الميزانية
                </div>
                <div class="dashboard-kpi-value">
                    {total_budget:,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="dashboard-kpi-card">
                <div class="dashboard-kpi-title">
                    إجمالي المتطوعين
                </div>
                <div class="dashboard-kpi-value">
                    {total_volunteers}
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        if logical_framework:

            st.subheader("الهدف العام")

            st.write(
                logical_framework[2]
            )

        st.subheader("مؤشرات المشروع")

        if project_kpis:

            for kpi in project_kpis:

                st.write(
                    f"• {kpi[2]}"
                )

    # ==========================================
    # DONOR REPORT
    # ==========================================

    elif report_type == "تقرير الداعمين":

        st.subheader("تقرير الداعمين")

        st.write(
            f"عدد المشاريع المنفذة: {total_projects}"
        )

        st.write(
            f"إجمالي المستفيدين: {total_beneficiaries}"
        )

        st.write(
            f"إجمالي الميزانية: {total_budget:,.0f}"
        )

    # ==========================================
    # IMPACT REPORT
    # ==========================================

    elif report_type == "تقرير الأثر":

        total_kpis = get_total_kpis()

        average_achievement = (
            get_average_kpi_achievement()
        )

        st.subheader("ملخص الأثر التنموي")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "إجمالي المستفيدين",
                total_beneficiaries
            )

        with col2:
            st.metric(
                "إجمالي المتطوعين",
                total_volunteers
            )

        with col3:
            st.metric(
                "عدد المؤشرات",
                total_kpis
            )

        st.divider()

        st.metric(
            "متوسط الإنجاز",
            f"{average_achievement}%"
        )

        st.divider()

        st.subheader("قياس الأثر المتقدم")

        st.write(
            f"العزو (Attribution): {project[58] or 0}%"
        )

        st.write(
            f"الإزاحة (Displacement): {project[59] or 0}%"
        )

        st.write(
            f"الحمل الزائد (Drop-off): {project[60] or 0}%"
        )

        st.write(
            f"ما كان سيحدث بدون المشروع (Deadweight): {project[61] or 0}%"
        )

        st.write(
            f"صافي الأثر (Net Impact): {project[62] or 0}%"
        )

        st.divider()

        st.subheader(
            "العائد الاجتماعي على الاستثمار (SROI)"
        )

        st.write(
            f"القيمة الاجتماعية: {project[63] or 0}"
        )

        st.write(
            f"القيمة الاقتصادية: {project[64] or 0}"
        )

        st.write(
            f"التوفير الحكومي: {project[65] or 0}"
        )

        st.write(
            f"القيمة البيئية: {project[66] or 0}"
        )

        st.write(
            f"SROI: {project[67] or 0}"
        )

        if average_achievement >= 80:

            st.success(
                "الأثر المحقق مرتفع وتم تحقيق معظم المؤشرات المستهدفة."
            )

        elif average_achievement >= 50:

            st.warning(
                "الأثر جيد لكن ما زالت هناك فرص لتحسين النتائج."
            )

        else:

            st.error(
                "مستوى الإنجاز منخفض ويحتاج إلى متابعة وتحسين."
            )

    elif report_type == "تقرير الإدارة التنفيذية":

        st.subheader("تقرير الإدارة التنفيذية")

        st.metric(
            "عدد المشاريع",
            total_projects
        )

        st.metric(
            "إجمالي الميزانية",
            f"{total_budget:,.0f}"
        )

        st.metric(
            "إجمالي المستفيدين",
            total_beneficiaries
        )

        st.metric(
            "إجمالي المتطوعين",
            total_volunteers
        )

        st.success(
            "ملخص موجه للإدارة العليا لدعم اتخاذ القرار."
        )

    elif report_type == "تقرير مجلس الإدارة":
        
        st.subheader("تقرير مجلس الإدارة")

        st.write(
            f"عدد المشاريع الحالية: {total_projects}"
        )

        st.write(
            f"إجمالي الميزانية: {total_budget:,.0f}"
        )   

        st.write(
            f"متوسط الإنجاز: {get_average_kpi_achievement()}%"
        )

        st.success(
            "تقرير استراتيجي لمجلس الإدارة."
        )


    elif report_type == "تقرير الشركاء":
        
        st.subheader("تقرير الشركاء")

        st.write(
            f"إجمالي المستفيدين: {total_beneficiaries}"
        )

        st.write(
            f"إجمالي المتطوعين: {total_volunteers}"
        )   

        st.write(
            f"عدد المشاريع: {total_projects}"
        )

        st.success(
            "تقرير مخصص للشركاء والجهات المتعاونة."
        )

    st.divider()


    # ==========================================
    # AI REPORT PREVIEW
    # ==========================================

    if st.button(
        "إنشاء تقرير ذكي"
    ):

        st.subheader(
            "التقرير الذكي"
        )

        total_target = 0
        total_actual = 0

        for kpi in project_kpis:

            total_target += kpi[3] or 0
            total_actual += kpi[4] or 0

        achievement = 0

        if total_target > 0:

            achievement = round(
                (total_actual / total_target) * 100,
                1
            )

        st.write(
            f"""
            مشروع {project[1]} في قطاع {project[3]}.

            استفاد من المشروع {project[12]} مستفيداً
            بمشاركة {project[14]} متطوعاً.

            بلغت نسبة الإنجاز العامة
            {achievement}%.

            وبلغ صافي الأثر
            {project[62] or 0}%،

            بينما سجل العائد الاجتماعي على الاستثمار
            SROI = {project[67] or 0}.
            """
        )

        st.subheader(
            "تحليل المؤشرات"
        )

        if achievement >= 80:

            st.success(
                "حقق المشروع أداءً مرتفعاً وتم تحقيق معظم المؤشرات المستهدفة."
            )

        elif achievement >= 50:

            st.warning(
                "حقق المشروع نتائج جيدة مع وجود فرص إضافية للتحسين."
            )

        else:

            st.error(
                "مستوى الإنجاز منخفض ويحتاج إلى تدخلات تطويرية."
            )

        st.subheader(
            "تحليل الأثر"
        )

        if (project[62] or 0) >= 70:

            st.success(
                "الأثر المتحقق مرتفع ويعكس تغيراً ملموساً لدى الفئة المستهدفة."
            )

        elif (project[62] or 0) >= 40:

            st.warning(
                "الأثر جيد ويمكن تعزيزه عبر توسيع الأنشطة وتحسين الاستهداف."
            )

        else:

            st.error(
                "مستوى الأثر منخفض مقارنة بالمستهدف."
            )

        st.subheader(
            "تحليل SROI"
        )

        if (project[67] or 0) >= 2:

            st.success(
                "العائد الاجتماعي على الاستثمار مرتفع ويعكس قيمة تنموية قوية."
            )

        elif (project[67] or 0) >= 1:

            st.info(
                "العائد الاجتماعي إيجابي ويحقق قيمة مناسبة مقابل الاستثمار."
            )

        else:

            st.warning(
                "العائد الاجتماعي منخفض ويحتاج إلى مراجعة فعالية التدخلات."
            )

        st.subheader(
            "التوصيات"
        )

        st.write(
            """
            • التركيز على الأنشطة الأعلى أثراً.

            • متابعة المؤشرات منخفضة الأداء.

            • زيادة مشاركة أصحاب المصلحة.

            • تحسين عمليات القياس والتقييم.

            • تعظيم القيمة الاجتماعية للمشروع.
            """
        )


        st.subheader(
            "مسودة قصة نجاح"
        )

        if project[29]:

            st.success(
                f"""
                ساهم مشروع {project[1]}
                في تحقيق نتائج إيجابية للفئة المستهدفة.

                ومن أبرز قصص النجاح:

                {project[29]}
                """
            )

        else:

            st.info(
                f"""
                ساهم مشروع {project[1]}
                في خدمة {project[12]} مستفيداً
                بمشاركة {project[14]} متطوعاً.

                يمكن إضافة قصة نجاح تفصيلية
                لإبراز أثر المشروع بصورة أكبر.
                """
            )

    if "edited_report" not in st.session_state:

        st.session_state.edited_report = ""

    if st.button(
        "إنشاء تقرير تلقائي"
    ):







        report_text = f"""


        
        يستعرض هذا التقرير أبرز نتائج وإنجازات مشروع {project[1]}
        ويقدم ملخصاً عن التنفيذ والمخرجات والأثر المتحقق.        

        ------------------------------------------------

        اسم المشروع:
        {project[1]}

        حالة المشروع:
        {project[7]}

        مدير المشروع:
        {project[5]}

        بلغت ميزانية المشروع        
        {project[10]:,.0f} ريال.

        استفاد من المشروع
        {project[12]} مستفيداً.

        وشارك في التنفيذ
        {project[14]} متطوعاً.       

        وصف المشروع:

        {project[15] or "لا يوجد وصف متاح"}

        """


        if logical_framework:

            report_text += f"""

        الهدف العام:
        {logical_framework[2]}      

        النتائج المتوقعة:
        {logical_framework[3]}
        """
            
        if project_kpis:

            report_text += """

        ------------------------

        مؤشرات الأداء

        """

            for kpi in project_kpis:

                target = kpi[3] or 0
                actual = kpi[4] or 0

                achievement = 0

                if target > 0:

                    achievement = round(
                        (actual / target) * 100,
                        1
                    )

                report_text += f"""

        المؤشر:
        {kpi[2]}

        المستهدف:
        {target}

        المتحقق:
        {actual}

        نسبة الإنجاز:
        {achievement}%

        """

        # ==========================================
        # Stakeholder Specific Sections
        # ==========================================

        if stakeholder == "عام":

            report_text += """

            ------------------------

            التقرير العام

            يعرض هذا التقرير جميع بيانات المشروع
            دون تخصيص لفئة محددة من أصحاب المصلحة.

            """

        if stakeholder == "الداعم":

            report_text += f"""

            ------------------------

            بيانات تهم الداعم

            عدد المستفيدين:
            {project[12]}

            عدد المستفيدين غير المباشرين:
            {project[17]}

            الأثر:
            {project[28] or "-"}

            قصص النجاح:
            {project[29] or "-"}
            """

        elif stakeholder == "الإدارة التنفيذية":

            report_text += f"""

            ------------------------

            بيانات الإدارة التنفيذية

            الميزانية:
            {project[10]:,.0f}

            التحديات:
            {project[30] or "-"}

            الحلول التصحيحية:
            {project[31] or "-"}

            التوصيات:
            {project[33] or "-"}
            """

        elif stakeholder == "مجلس الإدارة":

            report_text += f"""

            ------------------------

            بيانات مجلس الإدارة

            حالة المشروع:
            {project[7]}

            عدد المستفيدين:
            {project[12]}

            عدد المتطوعين:
            {project[14]}

            الميزانية:
            {project[10]:,.0f}
            """

        elif stakeholder == "الشريك الاستراتيجي":

            report_text += f"""

            ------------------------

            بيانات الشركاء

            الشركاء:
            {project[20] or "-"}

            عدد الشركاء:
            {project[21]}

            الأنشطة المنفذة:
            {project[24] or "-"}

            المخرجات:
            {project[25] or "-"}
            """

        elif stakeholder == "الجهة الإشرافية":

            report_text += f"""

            ------------------------

            بيانات الجهة الإشرافية

            المجال التنموي:
            {project[3] or "-"}

            الفئة المستهدفة:
            {project[16] or "-"}

            عدد المستفيدين:
            {project[12]}

            عدد المتطوعين:
            {project[14]}

            ساعات التطوع:
            {project[18]}

            """

        elif stakeholder == "المجتمع المحلي":

            report_text += f"""

            ------------------------

            بيانات المجتمع المحلي

            وصف المشروع:
            {project[15] or "-"}

            قصص النجاح:
            {project[29] or "-"}

            الأثر:
            {project[28] or "-"}

            """

        elif stakeholder == "المستفيدون":

            report_text += f"""

            ------------------------

            بيانات المستفيدين

            المخرجات:
            {project[25] or "-"}

            التغيرات:
            {project[26] or "-"}

            رضا المستفيدين:
            {project[51] or "-"}
            %
            """

        elif stakeholder == "فريق المشروع":

            report_text += f"""

            ------------------------

            بيانات فريق المشروع

            الأنشطة:
            {project[24] or "-"}

            المخرجات:
            {project[25] or "-"}

            التحديات:
            {project[30] or "-"}

            الدروس المستفادة:
            {project[32] or "-"}
            """

        elif stakeholder == "المتطوعون":

            report_text += f"""

            ------------------------

            بيانات المتطوعين

            عدد المتطوعين:
            {project[14]}

            ساعات التطوع:
            {project[18]}

            الأثر:
            {project[28] or "-"}
            """

        elif stakeholder == "فريق قياس الأثر":

            report_text += f"""

            ------------------------

            بيانات قياس الأثر

            منهجية القياس:
            {project[45] or "-"}

            حجم العينة:
            {project[46] or "-"}

            أدوات جمع البيانات:
            {project[47] or "-"}

            مستوى الأثر:
            {project[43] or "-"}

            نطاق الأثر:
            {project[44] or "-"}

            العزو:
            {project[58] or 0}%

            الإزاحة:
            {project[59] or 0}%

            الحمل الزائد:
            {project[60] or 0}%

            ما كان سيحدث بدون المشروع:
            {project[61] or 0}%

            صافي الأثر:
            {project[62] or 0}%

            القيمة الاجتماعية:
            {project[63] or 0}

            القيمة الاقتصادية:
            {project[64] or 0}

            التوفير الحكومي:
            {project[65] or 0}

            القيمة البيئية:
            {project[66] or 0}

            SROI:
            {project[67] or 0}

            """

        total_target = 0
        total_actual = 0

        for kpi in project_kpis:

            total_target += kpi[3] or 0
            total_actual += kpi[4] or 0

        overall_achievement = 0

        if total_target > 0:

            overall_achievement = round(
                (total_actual / total_target) * 100,
                1
            )

        report_text += f"""

        ------------------------------------------------

        قياس الأثر المتقدم

        العزو:
        {project[58] or 0}%

        الإزاحة:
        {project[59] or 0}%

        الحمل الزائد:
        {project[60] or 0}%

        ما كان سيحدث بدون المشروع:
        {project[61] or 0}%

        صافي الأثر:
        {project[62] or 0}%

        """

        report_text += f"""

        ------------------------------------------------

        العائد الاجتماعي على الاستثمار (SROI)

        القيمة الاجتماعية:
        {project[63] or 0}

        القيمة الاقتصادية:
        {project[64] or 0}

        التوفير الحكومي:
        {project[65] or 0}

        القيمة البيئية:
        {project[66] or 0}

        نسبة SROI:
        {project[67] or 0}

        """

        report_text += f"""

        ------------------------------------------------

        ملخص الإنجاز

        نسبة الإنجاز الكلية:

        {overall_achievement}%

        """


        report_text += """

            ------------------------------------------------

            يعكس هذا المشروع الجهود المبذولة لتحقيق
            الأهداف التنموية المخططة.       

            كما يوضح مستوى الإنجاز الحالي
            والمخرجات والأثر المتحقق للمستفيدين.

            ويوصي التقرير بالاستمرار في متابعة                
            المؤشرات وتحسين الأداء وتعظيم الأثر
            التنموي خلال المراحل القادمة.

        """

        st.session_state.edited_report = report_text

        pdf_file = "project_report.pdf"

        word_file = "project_report.docx"

        excel_file = "project_report.xlsx"

        generate_text_report(
            pdf_file,
            report_text
        )

        generate_word_report(
            word_file,
            report_text
        )

        generate_excel_report(
            excel_file,
            project,
            report_text
        )

        st.success(
            "تم إنشاء التقرير بنجاح"
        )

        st.subheader("التقرير الناتج")

        edited_report = st.text_area(
            "تحرير التقرير قبل التصدير",
            value=st.session_state.edited_report,
            height=500,
            key="report_editor"
        )

        st.session_state.edited_report = edited_report

        generate_text_report(
            pdf_file,
            edited_report
        )

        with open(
            pdf_file,
            "rb"
        ) as file:

            st.download_button(
                label="تحميل التقرير PDF",
                data=file,
                file_name=pdf_file,
                mime="application/pdf"
            )

        with open(
            word_file,
            "rb"
        ) as file:

            st.download_button(
                label="تحميل التقرير Word",
                data=file,
                file_name=word_file,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        with open(
            excel_file,
            "rb"
        ) as file:

            st.download_button(
                label="تحميل التقرير Excel",
                data=file,
                file_name=excel_file,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.subheader(
            "معاينة التقرير"
        )

        st.text_area(
            "",
            value=edited_report,
            height=300,
            disabled=True,
            key="report_preview"
        )

