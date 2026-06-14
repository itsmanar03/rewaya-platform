import streamlit as st
import pandas as pd
import os
from datetime import datetime

from database.database import (
    add_project,
    get_projects,
    delete_project,
    update_project,
    get_project_by_id,
    add_attachment,
    get_project_attachments,
    delete_attachment,
    archive_project
)

def show_projects():

    with open(
        "assets/projects.css",
        encoding="utf-8"
    ) as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

    st.markdown("""
    <div class="projects-title">
    إدارة المشاريع
    </div>

    <div class="projects-subtitle">
    إدارة المشاريع التنموية ومتابعة الأداء والأثر والمخرجات
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.get(
        "project_updated"
    ):

        st.success(
            "تم حفظ التعديلات بنجاح"
        )   

        del st.session_state[
            "project_updated"
        ]

    st.subheader("إضافة مشروع جديد")

    with st.form("project_form"):

        with st.expander(
            "📁 البيانات الأساسية",
            expanded=True
        ):

                project_name = st.text_input(
                    "اسم المشروع"
                )

                project_type = st.selectbox(
                    "نوع المشروع",
                    [
                        "برنامج",
                        "مشروع",
                        "مبادرة",
                        "حملة",
                        "فعالية"
                    ]
                )

                sector = st.selectbox(
                    "المجال",
                    [
                        "التمكين الاقتصادي",
                        "التعليم",
                        "التطوع",
                        "الصحة",
                        "الثقافة",
                        "التنمية الأسرية"
                    ]
                )

                region = st.text_input(
                    "المنطقة"
                )

                project_manager = st.text_input(
                    "مدير المشروع"
                )

                funding_source = st.text_input(
                    "جهة التمويل"
                )

                status = st.selectbox(
                    "حالة المشروع",
                    [
                        "قيد التخطيط",
                        "قيد التنفيذ",
                        "مكتمل",
                        "متوقف"
                    ]
                )

                start_date = st.date_input(
                    "تاريخ البداية"
                )

                end_date = st.date_input(
                    "تاريخ النهاية"
                )

                budget = st.number_input(
                    "الميزانية",
                    min_value=0.0
                )

        with st.expander(
            "👥 المستفيدون والمتطوعون"
        ):

                target_beneficiaries = st.number_input(
                    "المستفيدون المستهدفون",
                    min_value=0
                )

                actual_beneficiaries = st.number_input(
                    "المستفيدون المتحققون",
                    min_value=0
                )

                target_volunteers = st.number_input(
                    "المتطوعون المستهدفون",
                    min_value=0
                )

                actual_volunteers = st.number_input(
                    "المتطوعون المتحققون",
                    min_value=0
                )

                target_group = st.text_input(
                    "الفئة المستهدفة"
                )

                indirect_beneficiaries = st.number_input(
                    "المستفيدون غير المباشرين",
                    min_value=0
                )

                volunteer_hours = st.number_input(
                    "ساعات العمل التطوعي",
                    min_value=0
                )

                job_opportunities = st.number_input(
                    "عدد فرص العمل",
                min_value=0
                )

                partners = st.text_area(
                    "الشركاء"
                )

                partners_count = st.number_input(
                    "عدد الشركاء",
                    min_value=0
                )

                operational_costs = st.number_input(
                    "التكاليف التشغيلية",
                    min_value=0.0
                )

        with st.expander(
            "🎯 الإطار المنطقي"
        ):

                inputs = st.text_area(
                    "المدخلات"
                )

                activities = st.text_area(
                "الأنشطة المنفذة"
                )

                outputs = st.text_area(
                "المخرجات"
                )

                short_term_results = st.text_area(
                    "النتائج قصيرة المدى"
                )

                medium_term_results = st.text_area(
                    "النتائج متوسطة المدى"
                )

        with st.expander(
            "📈 نتائج وأثر المشروع"
        ):

                impact = st.text_area(
                    "الأثر"
                )

                success_stories = st.text_area(
                    "قصص النجاح"
                )   

                challenges = st.text_area(
                    "التحديات"
                )

                corrective_actions = st.text_area(
                    "الحلول والإجراءات التصحيحية"
                )

                lessons_learned = st.text_area(
                    "الدروس المستفادة"
                )

                recommendations = st.text_area(
                    "التوصيات"
                )

                donation_link = st.text_input(
                    "رابط التبرع"
                )

                volunteer_link = st.text_input(
                    "رابط التطوع"
                )

                description = st.text_area(
                "وصف المشروع"
                )


                development_need = st.text_area(
                    "الاحتياج التنموي"
                )

                need_evidence = st.text_area(
                    "الأدلة والشواهد"
                )   

                beneficiary_criteria = st.text_area(
                    "معايير اختيار المستفيدين"
                )

                strategic_goal = st.text_area(
                    "الهدف الاستراتيجي"
                )

                operational_goals = st.text_area(
                    "الأهداف التشغيلية"
                )

                long_term_change = st.text_area(
                    "التغيرات طويلة المدى"
                )


        with st.expander(
            "📊 قياس الأثر"
        ):

                impact_level = st.selectbox(
                    "مستوى الأثر",
                    [
                        "فردي",
                        "أسري",
                        "مؤسسي",
                        "مجتمعي"
                    ]
                )

                impact_scope = st.text_input(
                    "نطاق الأثر"
                )

                measurement_methodology = st.text_area(
                    "منهجية القياس"
                )

                sample_size = st.number_input(
                    "حجم العينة",
                    min_value=0
                )

                data_collection_tools = st.text_area(
                    "أدوات جمع البيانات"
                )

                financial_support_value = st.number_input(
                    "قيمة الدعم المالي",
                    min_value=0.0
                )

                in_kind_contributions = st.number_input(
                    "قيمة المساهمات العينية",
                    min_value=0.0
                )

                cost_per_beneficiary = st.number_input(
                        "تكلفة المستفيد الواحد",
                    min_value=0.0
                )   

                beneficiary_satisfaction = st.number_input(
                    "رضا المستفيدين %",
                    min_value=0.0,
                    max_value=100.0
                )

                partner_satisfaction = st.number_input(
                    "رضا الشركاء %",
                    min_value=0.0,
                    max_value=100.0
                )


        with st.expander(
            "🤝 أصحاب المصلحة"
        ):

                stakeholders = st.text_area(
                    "أصحاب المصلحة"
                )   

                stakeholder_influence = st.text_area(
                    "درجة التأثير"
                )

                stakeholder_affected = st.text_area(
                    "درجة التأثر"
                )

                engagement_method = st.text_area(
                    "آلية الإشراك"
                )

                engagement_results = st.text_area(
                    "نتائج المشاركة"
                )


        with st.expander(
            "⚡ قياس الأثر المتقدم"
        ):

                attribution = st.number_input(
                    "العزو Attribution %",
                    min_value=0.0,
                    max_value=100.0
                )

                displacement = st.number_input(
                    "الإزاحة Displacement %",
                    min_value=0.0,
                    max_value=100.0
                )

                dropoff = st.number_input(
                    "الحمل الزائد Drop-off %",
                    min_value=0.0,
                    max_value=100.0
                )

                deadweight = st.number_input(
                    "ما كان سيحدث بدون المشروع Deadweight %",
                    min_value=0.0,
                    max_value=100.0
                )

                net_impact = (
                    attribution
                    - displacement
                    - dropoff
                    - deadweight
                )

                st.info(
                    f"صافي الأثر المحسوب: {net_impact:.2f}%"
                )

        with st.expander(
            "💰 العائد الاجتماعي على الاستثمار (SROI)"
        ):

                social_value = st.number_input(
                    "القيمة الاجتماعية المحققة",
                    min_value=0.0
                )   

                economic_value = st.number_input(
                    "القيمة الاقتصادية المحققة",
                    min_value=0.0
                )

                government_saving = st.number_input(
                    "قيمة التوفير الحكومي",
                    min_value=0.0
                )

                environmental_value = st.number_input(
                    "القيمة البيئية",
                    min_value=0.0
                )

                total_social_return = (
                    social_value
                    + economic_value
                    + government_saving
                    + environmental_value
                )

                sroi_ratio = 0

                if budget > 0:

                    sroi_ratio = round(
                        total_social_return / budget,
                            2
                    )

                st.info(
                    f"SROI = {sroi_ratio}"
                )

        submitted = st.form_submit_button(
            "حفظ المشروع"
        )

        if submitted:

            add_project(
                project_name,
                project_type,
                sector,
                region,
                project_manager,
                funding_source,
                status,
                start_date,
                end_date,   
                budget,
                target_beneficiaries,
                actual_beneficiaries,
                target_volunteers,
                actual_volunteers,
                description,
                target_group,
                indirect_beneficiaries,
                volunteer_hours,
                job_opportunities,
                partners,
                partners_count,
                operational_costs,
                inputs,
                activities,
                outputs,
                short_term_results,
                medium_term_results,
                impact,
                success_stories,
                challenges,
                corrective_actions,
                lessons_learned,
                recommendations,
                donation_link,
                volunteer_link,

                development_need,
                need_evidence,

                beneficiary_criteria,

                strategic_goal,
                operational_goals,

                long_term_change,

                impact_level,
                impact_scope,

                measurement_methodology,
                sample_size,
                data_collection_tools,

                financial_support_value,
                in_kind_contributions,

                cost_per_beneficiary,

                beneficiary_satisfaction,
                partner_satisfaction,

                stakeholders,
                stakeholder_influence,
                stakeholder_affected,
                engagement_method,
                engagement_results,
                attribution,
                displacement,
                dropoff,
                deadweight,
                net_impact,
                social_value,
                economic_value,
                government_saving,
                environmental_value,
                sroi_ratio
            )

            st.success(
                "تم حفظ المشروع بنجاح"
            )

            st.rerun()

    st.divider()

    search_text = st.text_input(
        "البحث عن مشروع"
    )

    projects = get_projects()

    if search_text:

        projects = [
            p for p in projects
            if search_text.lower()
            in p[1].lower()
        ]

    st.subheader("المشاريع المسجلة")

    if projects:

        for project in projects:

            project_id = project[0]
            project_name = project[1]

            with st.expander(f"📁 {project_name}", expanded=False):
                c1, c2, c3, c4 = st.columns(4)

                with c1:
                    st.metric(
                        "الميزانية",
                        f"{project[10]:,.0f}"
                    )

                with c2:
                    st.metric(
                    "المستفيدون",
                    project[12]
                    )

                with c3:
                    st.metric(
                    "الحالة",
                    project[7]
                    )

                with c4:
                    st.metric(
                    "نوع المشروع",
                    project[2]
                )

                st.write("### وصف المشروع")

                if project[15]:
                    st.write(project[15])
                else:
                    st.info("لا يوجد وصف للمشروع")

                st.divider()

                st.subheader("قياس الأثر المتقدم")


                m1, m2, m3, m4, m5 = st.columns(5)

                with m1:
                    st.metric(
                        "العزو",
                        f"{project[58]}%"
                        if len(project) > 58 and project[58] is not None
                        else "-"
                        )

                with m2:
                    st.metric(
                    "الإزاحة",
                    f"{project[59]}%"
                    if len(project) > 59 and project[59] is not None
                    else "-"
                    )

                with m3:
                    st.metric(
                    "Drop-off",
                    f"{project[60]}%"
                    if len(project) > 60 and project[60] is not None
                    else "-"
                    )

                with m4:
                    st.metric(
                    "Deadweight",
                    f"{project[61]}%"
                    if len(project) > 61 and project[61] is not None
                    else "-"
                )

                with m5:
                    st.metric(
                    "Net Impact",
                    f"{project[62]}%"
                    if len(project) > 62 and project[62] is not None
                    else "-"
                )


                c1, c2 = st.columns([1,1])
                
                with c1:

                    if st.button(
                        "عرض التفاصيل",
                        key=f"view_{project_id}"
                    ):
                        st.session_state.selected_project = project_id
                        st.rerun()

                with c2:

                    with st.expander(
                        "تعديل المشروع"
                    ):

                        new_name = st.text_input(
                            "اسم المشروع",
                            value=project[1],
                            key=f"name_{project_id}"
                        )

                        new_manager = st.text_input(
                            "مدير المشروع",
                            value=project[5] or "",
                            key=f"manager_{project_id}"
                        )

                        new_funding = st.text_input(
                            "جهة التمويل",
                            value=project[6] or "",
                            key=f"funding_{project_id}"
                        )

                        status_options = [
                            "قيد التخطيط",
                            "قيد التنفيذ",
                            "مكتمل",
                            "متوقف"
                        ]

                        new_status = st.selectbox(
                        "الحالة",
                        status_options,
                        index=status_options.index(project[7])
                        if project[7] in status_options
                        else 0,
                        key=f"status_{project_id}"
                        )

                        new_budget = st.number_input(
                            "الميزانية",
                            value=float(project[10] or 0),
                            key=f"budget_{project_id}"
                        )

                        new_beneficiaries = st.number_input(
                            "المستفيدون المتحققون",
                            value=int(project[12] or 0),
                            key=f"ben_{project_id}"
                        )

                        new_volunteers = st.number_input(
                            "المتطوعون المتحققون",
                            value=int(project[14] or 0),
                            key=f"vol_{project_id}"
                        )

                        new_volunteer_hours = st.number_input(
                            "ساعات التطوع",
                            value=int(project[18] or 0),
                            key=f"hours_{project_id}"
                        )

                        new_jobs = st.number_input(
                            "فرص العمل",
                            value=int(project[19] or 0),
                            key=f"jobs_{project_id}"
                        )

                        new_activities = st.text_area(
                            "الأنشطة",
                            value=project[24] or "",
                            key=f"activities_{project_id}"
                        )

                        new_outputs = st.text_area(
                            "المخرجات",
                            value=project[25] or "",
                            key=f"outputs_{project_id}"
                        )

                        new_impact = st.text_area(
                            "الأثر",
                            value=project[28] or "",
                            key=f"impact_{project_id}"
                        )

                        new_challenges = st.text_area(
                            "التحديات",
                            value=project[30] or "",
                            key=f"challenges_{project_id}"
                        )

                        new_recommendations = st.text_area(
                            "التوصيات",
                            value=project[33] or "",
                            key=f"recommendations_{project_id}"
                        )

                        new_beneficiary_satisfaction = st.number_input(
                            "رضا المستفيدين",
                            value=float(project[51] or 0),
                            key=f"beneficiary_sat_{project_id}"
                        )

                        new_partner_satisfaction = st.number_input(
                            "رضا الشركاء",
                            value=0.0,
                            key=f"partner_sat_{project_id}"
                        )

                        new_net_impact = st.number_input(
                            "صافي الأثر",
                            value=float(project[62] or 0),
                            key=f"netimpact_{project_id}"
                        )

                        new_sroi = st.number_input(
                            "SROI",
                            value=float(project[67] or 0),
                            key=f"sroi_{project_id}"
                        )

                        new_description = st.text_area(
                            "الوصف",
                            value=project[15] or "",
                            key=f"desc_{project_id}"
                        )


                        if st.button(
                            "حفظ التعديلات",
                            key=f"save_{project_id}"
                        ):

                            update_project(
                                project_id,
                                new_name,
                                new_manager,
                                new_funding,
                                new_status,
                                new_budget,
                                new_beneficiaries,
                                new_volunteers,
                                new_volunteer_hours,
                                new_jobs,
                                new_activities,
                                new_outputs,
                                new_impact,
                                new_challenges,
                                new_recommendations,
                                new_beneficiary_satisfaction,
                                new_partner_satisfaction,
                                new_net_impact,
                                new_sroi,
                                new_description
                            )

                            st.session_state.project_updated = True

                            st.rerun()


    else:

        st.info(
            "لا توجد مشاريع حالياً"
        )

    # ==========================================
    # PROJECT DETAILS
    # ==========================================

    if (
        "selected_project" in st.session_state
        and st.session_state.selected_project is not None
    ):
        project = get_project_by_id(
            st.session_state.selected_project
        )

        if project:

            st.divider()

            st.subheader(
                f"تفاصيل المشروع: {project[1]}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.write("**نوع المشروع:**", project[2])
                st.write("**المجال:**", project[3])
                st.write("**المنطقة:**", project[4])
                st.write("**مدير المشروع:**", project[5])
                st.write("**جهة التمويل:**", project[6])
                st.write("**الحالة:**", project[7])

            with col2:

                st.write("**الميزانية:**", project[10])
                st.write("**المستفيدون المستهدفون:**", project[11])
                st.write("**المستفيدون المتحققون:**", project[12])
                st.write("**المتطوعون المستهدفون:**", project[13])
                st.write("**المتطوعون المتحققون:**", project[14])

            st.divider()

            st.subheader("بيانات إضافية")

            st.write("**الفئة المستهدفة:**", project[16])
            st.write("**المستفيدون غير المباشرين:**", project[17])
            st.write("**ساعات العمل التطوعي:**", project[18])
            st.write("**فرص العمل:**", project[19])

            st.write("**الشركاء:**", project[20])
            st.write("**عدد الشركاء:**", project[21])
            st.write("**التكاليف التشغيلية:**", project[22])

            st.divider()

            st.subheader("محتوى المشروع")

            st.write("### وصف المشروع")
            st.write(project[15] or "-")

            st.write("### المدخلات")
            st.write(project[23] or "-")

            st.write("### الأنشطة")
            st.write(project[24] or "-")

            st.write("### المخرجات")
            st.write(project[25] or "-")

            st.write("### النتائج قصيرة المدى")
            st.write(project[26] or "-")

            st.write("### النتائج متوسطة المدى")
            st.write(project[27] or "-")

            st.write("### الأثر")
            st.write(project[28] or "-")

            st.write("### قصص النجاح")
            st.write(project[29] or "-")

            st.write("### التحديات")
            st.write(project[30] or "-")

            st.write("### الإجراءات التصحيحية")
            st.write(project[31] or "-")

            st.write("### الدروس المستفادة")
            st.write(project[32] or "-")

            st.write("### التوصيات")
            st.write(project[33] or "-")

            st.divider()

            st.subheader("قياس الأثر")

            st.write(
                "**الاحتياج التنموي:**",
                project[37] if len(project) > 37 else "-"
            )

            st.write(
                "**الأدلة والشواهد:**",
                project[38] if len(project) > 38 else "-"
            )

            st.write(
                "**معايير اختيار المستفيدين:**",
                project[39] if len(project) > 39 else "-"
            )

            st.write(
                "**الهدف الاستراتيجي:**",
                project[40] if len(project) > 40 else "-"
            )

            st.write(
                "**الأهداف التشغيلية:**",
                project[41] if len(project) > 41 else "-"
            )

            st.write(
                "**التغير طويل المدى:**",
                project[42] if len(project) > 42 else "-"
            )

            st.write(
                "**مستوى الأثر:**",
                project[43] if len(project) > 43 else "-"
            )

            st.write(
                "**نطاق الأثر:**",
                project[44] if len(project) > 44 else "-"
            )

            st.write(
                "**منهجية القياس:**",
                project[45] if len(project) > 45 else "-"
            )

            st.write(
                "**حجم العينة:**",
                project[46] if len(project) > 46 else "-"
            )

            st.write(
                "**أدوات جمع البيانات:**",
                project[47] if len(project) > 47 else "-"
            )

            st.write(
                "**قيمة الدعم المالي:**",
                project[48] if len(project) > 48 else "-"
            )

            st.write(
                "**المساهمات العينية:**",
                project[49] if len(project) > 49 else "-"
            )

            st.write(
                "**تكلفة المستفيد الواحد:**",
                project[50] if len(project) > 50 else "-"
            )

            st.write(
                "**رضا المستفيدين:**",
                project[51] if len(project) > 51 else "-"
            )

            st.write(
                "**رضا الشركاء:**",
                project[52] if len(project) > 52 else "-"
            )


            st.subheader("أصحاب المصلحة")

            st.write(
                "**أصحاب المصلحة:**",
                project[53] if len(project) > 53 else "-"
            )

            st.write(
                "**درجة التأثير:**",
                project[54] if len(project) > 54 else "-"
            )

            st.write(
                "**درجة التأثر:**",
                project[55] if len(project) > 55 else "-"
            )

            st.write(
                "**آلية الإشراك:**",
                project[56] if len(project) > 56 else "-"
            )

            st.write(
                "**نتائج المشاركة:**",
                project[57] if len(project) > 57 else "-"
            )

            st.divider()

            st.subheader(
                "العائد الاجتماعي على الاستثمار (SROI)"
            )

            st.write(
                "**القيمة الاجتماعية:**",
                project[63] if len(project) > 63 else "-"
            )

            st.write(
                "**القيمة الاقتصادية:**",
                project[64] if len(project) > 64 else "-"
            )

            st.write(
                "**التوفير الحكومي:**",
                project[65] if len(project) > 65 else "-"
            )

            st.write(
                "**القيمة البيئية:**",
                project[66] if len(project) > 66 else "-"
            )

            st.write(
                "**SROI:**",
                project[67] if len(project) > 67 else "-"
            )

            st.subheader("الروابط")

            st.write("**رابط التبرع:**", project[34] or "-")
            st.write("**رابط التطوع:**", project[35] or "-")

            st.divider()

            st.subheader("المرفقات")

            uploaded_files = st.file_uploader(
                "رفع صور أو ملفات المشروع",
                accept_multiple_files=True
            )

            if uploaded_files:

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                for uploaded_file in uploaded_files:

                    existing_files = get_project_attachments(
                        project[0]
                    )

                    file_exists = any(
                        attachment[2] == uploaded_file.name
                        for attachment in existing_files
                    )

                    if file_exists:
                        continue


                    file_path = os.path.join(
                        "uploads",
                        uploaded_file.name
                    )

                    with open(
                        file_path,
                        "wb"
                    ) as f:

                        f.write(
                            uploaded_file.getbuffer()
                        )

                    add_attachment(
                        project[0],
                        uploaded_file.name,
                        file_path,
                        uploaded_file.type,
                        str(datetime.now())
                    )

                st.success(
                    "تم رفع الملفات بنجاح"
                )

                st.rerun()

            attachments = get_project_attachments(
                project[0]
            )

            if attachments:

                st.subheader(
                    "الملفات المرفوعة"
                )

                for attachment in attachments:

                    st.write(
                        f"📎 {attachment[2]}"
                    )

                    file_type = attachment[4] or ""

                    try:

                        # صور
                        if "image" in file_type:

                            st.image(
                                attachment[3],
                                use_container_width=True
                            )

                        # فيديو
                        elif "video" in file_type:

                            with open(
                                attachment[3],
                                "rb"
                            ) as video_file:

                                st.video(
                                    video_file.read()
                                )

                    except:
                        pass

                    col1, col2 = st.columns([3,1])

                    with col1:

                        try:

                            with open(
                                attachment[3],
                                "rb"
                            ) as file:

                                st.download_button(
                                    label=f"تحميل {attachment[2]}",
                                    data=file,
                                    file_name=attachment[2],
                                    key=f"download_{attachment[0]}"
                                )

                        except:

                            st.warning(
                                "الملف غير موجود على الجهاز"
                            )

                    with col2:

                        if st.button(
                            "حذف",
                            key=f"delete_attachment_{attachment[0]}"
                        ):

                            try:

                                if os.path.exists(
                                    attachment[3]
                                ):

                                    os.remove(
                                        attachment[3]
                                    )

                            except:
                                pass

                            delete_attachment(
                                attachment[0]
                            )

                            st.success(
                                "تم حذف المرفق"
                            )

                            st.rerun()


            st.divider()

            st.subheader("أرشفة المشروع")

            archive_reason = st.text_area(
            "سبب الأرشفة"
            )

            if st.button(
            "أرشفة المشروع",
            use_container_width=True
            ):

                archive_project(
                    project[0],
                    archive_reason,
                    st.session_state.get(
                    "user_email",
                    "غير معروف"
                    )
                )

                st.success(
                    "تمت أرشفة المشروع"
                )

                st.rerun()


            if st.button("إغلاق التفاصيل"):

                del st.session_state.selected_project

                st.rerun()