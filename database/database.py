import sqlite3
from datetime import datetime

def get_connection():

    conn = sqlite3.connect(
        "rewaya.db",
        check_same_thread=False
    )

    return conn


# ==========================================
# USERS
# ==========================================

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_default_admin():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email = ?
    """, ("admin@rewaya.com",))

    admin = cursor.fetchone()

    if not admin:

        cursor.execute("""
        INSERT INTO users(
            email,
            password,
            role
        )
        VALUES (?, ?, ?)
        """, (
            "admin@rewaya.com",
            "123456",
            "مدير النظام"
        ))

        conn.commit()

    conn.close()


def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    WHERE email = ?
    AND password = ?
    """, (
        email,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user

def add_user(
    email,
    password,
    role
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users(
        email,
        password,
        role
    )
    VALUES (?, ?, ?)
    """, (
        email,
        password,
        role
    ))

    conn.commit()
    conn.close()


def get_users():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM users
    ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users

def update_user(
    user_id,
    email,
    role
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET
        email = ?,
        role = ?
    WHERE id = ?
    """, (
        email,
        role,
        user_id
    ))

    conn.commit()
    conn.close()


def toggle_user_status(
    user_id,
    current_status
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET is_active = ?
    WHERE id = ?
    """, (
        0 if current_status else 1,
        user_id
    ))

    conn.commit()
    conn.close()

def delete_user(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM users
    WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
    

# ==========================================
# ACTIVITY LOGS
# ==========================================

def create_activity_logs_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activity_logs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        action TEXT,

        entity_type TEXT,

        entity_name TEXT,

        action_date TEXT

    )
    """)

    conn.commit()
    conn.close()

def create_notifications_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        message TEXT,

        created_at TEXT,

        is_read INTEGER DEFAULT 0

    )
    """)

    conn.commit()
    conn.close()

def add_activity_log(
    action,
    entity_type,
    entity_name
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO activity_logs(
        action,
        entity_type,
        entity_name,
        action_date
    )
    VALUES (?, ?, ?, ?)
    """, (
        action,
        entity_type,
        entity_name,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()

def add_notification(
    title,
    message
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO notifications(
        title,
        message,
        created_at
    )
    VALUES (?, ?, ?)
    """, (
        title,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))

    conn.commit()
    conn.close()

def get_notifications():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM notifications
    ORDER BY id DESC
    """)

    notifications = cursor.fetchall()

    conn.close()

    return notifications

def get_unread_notifications_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM notifications
    WHERE is_read = 0
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def mark_notification_as_read(
    notification_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE notifications
    SET is_read = 1
    WHERE id = ?
    """, (notification_id,))

    conn.commit()
    conn.close()


def mark_all_notifications_as_read():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE notifications
    SET is_read = 1
    """)

    conn.commit()
    conn.close()

def get_activity_logs():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM activity_logs
    ORDER BY id DESC
    """)

    logs = cursor.fetchall()

    conn.close()

    return logs


# ==========================================
# PROJECTS
# ==========================================

def create_projects_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_name TEXT,
        project_type TEXT,
        sector TEXT,
        region TEXT,

        project_manager TEXT,
        funding_source TEXT,

        status TEXT,

        start_date TEXT,
        end_date TEXT,

        budget REAL,

        target_beneficiaries INTEGER,
        actual_beneficiaries INTEGER,

        target_volunteers INTEGER,
        actual_volunteers INTEGER,

        description TEXT,

        target_group TEXT,

        indirect_beneficiaries INTEGER,

        volunteer_hours INTEGER,

        job_opportunities INTEGER,

        partners TEXT,

        partners_count INTEGER,

        operational_costs REAL,

        inputs TEXT,

        activities TEXT,

        outputs TEXT,

        short_term_results TEXT,

        medium_term_results TEXT,

        impact TEXT,

        success_stories TEXT,

        challenges TEXT,

        corrective_actions TEXT,

        lessons_learned TEXT,

        recommendations TEXT,

        donation_link TEXT,

        volunteer_link TEXT,

        development_need TEXT,
        need_evidence TEXT,

        beneficiary_criteria TEXT,

        strategic_goal TEXT,
        operational_goals TEXT, 

        long_term_change TEXT,

        impact_level TEXT,
        impact_scope TEXT,

        measurement_methodology TEXT,
        sample_size INTEGER,
        data_collection_tools TEXT,

        financial_support_value REAL,
        in_kind_contributions REAL,

        cost_per_beneficiary REAL,

        beneficiary_satisfaction REAL,
        partner_satisfaction REAL,

        stakeholders TEXT,

        stakeholder_influence TEXT,

        stakeholder_affected TEXT,

        engagement_method TEXT,

        engagement_results TEXT,

        attribution REAL,

        displacement REAL,

        dropoff REAL,

        deadweight REAL,

        net_impact REAL,

        social_value REAL,

        economic_value REAL,

        government_saving REAL,

        environmental_value REAL,

        sroi_ratio REAL,

        archived INTEGER DEFAULT 0

    )
    """)

    conn.commit()
    conn.close()


def add_project(
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
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO projects(
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

    VALUES (
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?,?,?,?,?,
    ?,?,?,?,?,?
    )
    """, (

        project_name,
        project_type,
        sector,
        region,
        project_manager,
        funding_source,
        status,
        str(start_date),
        str(end_date),
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

    ))

    conn.commit()

    add_activity_log(
        "إضافة",
        "مشروع",
        project_name
    )

    add_notification(
        "مشروع جديد",
        f"تمت إضافة المشروع: {project_name}"
    )

    conn.close()


def create_attachments_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attachments(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        file_name TEXT,

        file_path TEXT,

        file_type TEXT,

        upload_date TEXT,

        FOREIGN KEY(project_id)
        REFERENCES projects(id)

    )
    """)

    conn.commit()
    conn.close()

def add_attachment(
    project_id,
    file_name,
    file_path,
    file_type,
    upload_date
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO attachments(

        project_id,
        file_name,
        file_path,
        file_type,
        upload_date

    )
    VALUES (?, ?, ?, ?, ?)
    """, (

        project_id,
        file_name,
        file_path,
        file_type,
        upload_date

    ))

    conn.commit()
    conn.close()

def get_project_attachments(
    project_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM attachments
    WHERE project_id = ?
    """, (project_id,))

    data = cursor.fetchall()

    conn.close()

    return data

def get_projects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM projects
    WHERE archived = 0
    ORDER BY id DESC
    """)

    projects = cursor.fetchall()

    conn.close()

    return projects


# ==========================================
# DASHBOARD STATS
# ==========================================

def get_projects_count():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE archived = 0
    """)

    count = cursor.fetchone()[0]

    conn.close()

    return count


def get_total_budget():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(budget)
    FROM projects
    WHERE archived = 0
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0


def get_total_beneficiaries():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(actual_beneficiaries)
    FROM projects
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0


def get_total_volunteers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT SUM(actual_volunteers)
    FROM projects
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return result if result else 0

# ==========================================
# PROJECT DETAILS
# ==========================================

def get_project_by_id(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM projects
    WHERE id = ?
    """, (project_id,))

    project = cursor.fetchone()

    conn.close()

    return project

def delete_project(project_id):

    project = get_project_by_id(
        project_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM projects
    WHERE id = ?
    """, (project_id,))

    conn.commit()

    if project:

        add_activity_log(
            "حذف",
            "مشروع",
            project[1]
        )

    add_notification(
        "حذف مشروع",
        f"تم حذف المشروع نهائياً: {project[1]}"
    )

    conn.close()

# ==========================================
# LOGICAL FRAMEWORK
# ==========================================

def create_logical_framework_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS logical_framework(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER UNIQUE,

        inputs TEXT,

        activities TEXT,

        outputs TEXT,

        short_term_change TEXT,

        medium_term_change TEXT,

        long_term_change TEXT,

        impact TEXT,

        assumptions TEXT,

        risks TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_logical_framework(
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
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM logical_framework
    WHERE project_id = ?
    """, (project_id,))

    exists = cursor.fetchone()

    if exists:

        cursor.execute("""
        UPDATE logical_framework
        SET
            inputs = ?,
            activities = ?,
            outputs = ?,
            short_term_change = ?,
            medium_term_change = ?,
            long_term_change = ?,
            impact = ?,
            assumptions = ?,
            risks = ?
        WHERE project_id = ?
        """, (
            inputs,
            activities,
            outputs,
            short_term_change,
            medium_term_change,
            long_term_change,
            impact,
            assumptions,
            risks,
            project_id
        ))

    else:

        cursor.execute("""
        INSERT INTO logical_framework(

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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
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
))

    conn.commit()
    conn.close()

def get_logical_framework(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM logical_framework
    WHERE project_id = ?
    """, (project_id,))

    data = cursor.fetchone()

    conn.close()

    return data

def create_kpis_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS kpis(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        indicator_name TEXT,

        target_value REAL,

        actual_value REAL,

        unit TEXT,

        indicator_type TEXT,
        
        framework_level TEXT,

        linked_element TEXT,

        stakeholder_priority TEXT,

        deviation_reason TEXT

    )
    """)

    conn.commit()
    conn.close()


def add_kpi(
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
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO kpis(

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
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

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

    ))

    conn.commit()

    add_notification(
        "مؤشر جديد",
        f"تمت إضافة مؤشر: {indicator_name}"
    )

    conn.close()


def get_kpis(project_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM kpis
    WHERE project_id = ?
    ORDER BY id DESC
    """, (project_id,))

    data = cursor.fetchall()

    conn.close()

    return data


def delete_kpi(kpi_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM kpis
    WHERE id = ?
    """, (kpi_id,))

    conn.commit()
    conn.close()

def get_all_kpis():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM kpis
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_projects_by_status():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        status,
        COUNT(*)
    FROM projects
    WHERE archived = 0
    GROUP BY status
    """)

    data = cursor.fetchall()

    conn.close()

    return data

def get_total_kpis():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM kpis
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_kpi_achievement():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        AVG(
            CASE
                WHEN target_value > 0
                THEN (actual_value * 100.0 / target_value)
                ELSE 0
            END
        )
    FROM kpis
    """)

    result = cursor.fetchone()[0]

    conn.close()

    return round(result or 0, 1)

def update_project(
    project_id,
    project_name,
    project_manager,
    funding_source,
    status,
    budget,
    actual_beneficiaries,
    actual_volunteers,
    volunteer_hours,
    job_opportunities,
    activities,
    outputs,
    impact,
    challenges,
    recommendations,
    beneficiary_satisfaction,
    partner_satisfaction,
    net_impact,
    sroi_ratio,
    description
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE projects
    SET
        project_name = ?,
        project_manager = ?,
        funding_source = ?,
        status = ?,
        budget = ?,
        actual_beneficiaries = ?,
        actual_volunteers = ?,
        volunteer_hours = ?,
        job_opportunities = ?,
        activities = ?,
        outputs = ?,
        impact = ?,
        challenges = ?,
        recommendations = ?,
        beneficiary_satisfaction = ?,
        partner_satisfaction = ?,
        net_impact = ?,
        sroi_ratio = ?,
        description = ?
    WHERE id = ?
    """,
    (
        project_name,
        project_manager,
        funding_source,
        status,
        budget,
        actual_beneficiaries,
        actual_volunteers,
        volunteer_hours,
        job_opportunities,
        activities,
        outputs,
        impact,
        challenges,
        recommendations,
        beneficiary_satisfaction,
        partner_satisfaction,
        net_impact,
        sroi_ratio,
        description,
        project_id
    ))

    conn.commit()

    add_activity_log(
        "تعديل",
        "مشروع",
        project_name
    )

    add_notification(
        "تحديث مشروع",
        f"تم تحديث المشروع: {project_name}"
    )

    conn.close()

def archive_project(
    project_id,
    archive_reason,
    archived_by
):

    project = get_project_by_id(
        project_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE projects
    SET
        archived = 1,
        archive_reason = ?,
        archived_by = ?,
        archived_date = ?
    WHERE id = ?
    """, (
        archive_reason,
        archived_by,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        ),
        project_id
    ))

    conn.commit()

    add_activity_log(
        "أرشفة",
        "مشروع",
        project[1]
    )

    add_notification(
        "أرشفة مشروع",
        f"تمت أرشفة المشروع: {project[1]}"
    )

    conn.close()
def restore_project(project_id):

    project = get_project_by_id(
        project_id
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE projects
    SET archived = 0
    WHERE id = ?
    """, (project_id,))

    conn.commit()

    add_activity_log(
        "استعادة",
        "مشروع",
        project[1]
    )

    add_notification(
        "استعادة مشروع",
        f"تمت استعادة المشروع: {project[1]}"
    )

    conn.close()



def get_archived_projects():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM projects
    WHERE archived = 1
    ORDER BY id DESC
    """)

    projects = cursor.fetchall()

    conn.close()

    return projects


def initialize_database():

    create_tables()

    create_projects_table()

    create_logical_framework_table()

    create_kpis_table()

    create_attachments_table()

    create_activity_logs_table()

    create_notifications_table()

    create_default_admin()

    create_performance_tracking_table()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
        ALTER TABLE projects
        ADD COLUMN archived INTEGER DEFAULT 0
        """)

        conn.commit()

    except:

        pass


    try:

        cursor.execute("""
        ALTER TABLE kpis
        ADD COLUMN deviation_reason TEXT
        """)

        conn.commit()

    except:

        pass

    new_columns = [

        ("development_need", "TEXT"),
        ("need_evidence", "TEXT"),

        ("beneficiary_criteria", "TEXT"),

        ("strategic_goal", "TEXT"),
        ("operational_goals", "TEXT"),

        ("long_term_change", "TEXT"),

        ("impact_level", "TEXT"),
        ("impact_scope", "TEXT"),

        ("measurement_methodology", "TEXT"),
        ("sample_size", "INTEGER"),
        ("data_collection_tools", "TEXT"),

        ("financial_support_value", "REAL"),
        ("in_kind_contributions", "REAL"),

        ("cost_per_beneficiary", "REAL"),

        ("beneficiary_satisfaction", "REAL"),
        ("partner_satisfaction", "REAL"),

        ("stakeholders", "TEXT"),

        ("stakeholder_influence", "TEXT"),

        ("stakeholder_affected", "TEXT"),

        ("engagement_method", "TEXT"),

        ("engagement_results", "TEXT"),

        ("attribution", "REAL"),

        ("displacement", "REAL"),

        ("dropoff", "REAL"),

        ("deadweight", "REAL"),

        ("net_impact", "REAL"),

        ("social_value", "REAL"),

        ("economic_value", "REAL"),

        ("government_saving", "REAL"),

        ("environmental_value", "REAL"),

        ("sroi_ratio", "REAL"),

        ("is_active", "INTEGER DEFAULT 1"),

        ("archive_reason", "TEXT"),

        ("archived_by", "TEXT"),

        ("archived_date", "TEXT"),

    ]

    for column_name, column_type in new_columns:

        try:

            cursor.execute(
                f"""
                ALTER TABLE projects
                ADD COLUMN {column_name} {column_type}
                """
            )

            conn.commit()

        except:
            pass


    logical_columns = [

        ("inputs", "TEXT"),

        ("short_term_change", "TEXT"),

        ("medium_term_change", "TEXT"),

        ("long_term_change", "TEXT"),

        ("impact", "TEXT")

    ]


    kpi_columns = [

        ("framework_level", "TEXT"),

        ("linked_element", "TEXT"),

        ("stakeholder_priority", "TEXT")

    ]

    for column_name, column_type in kpi_columns:

        try:

            cursor.execute(
                f"""
                ALTER TABLE kpis
                ADD COLUMN {column_name} {column_type}
                """
            )

            conn.commit()

        except:
            pass


    for column_name, column_type in logical_columns:

        try:

            cursor.execute(
                f"""
                ALTER TABLE logical_framework
                ADD COLUMN {column_name} {column_type}
                """
            )

            conn.commit()

        except:
            pass

    conn.close()


def delete_attachment(attachment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM attachments
        WHERE id = ?
        """,
        (attachment_id,)
    )

    conn.commit()
    conn.close()


def update_kpi(
    kpi_id,
    indicator_name,
    target_value,
    actual_value,
    unit,
    indicator_type,
    framework_level,
    linked_element,
    stakeholder_priority,
    deviation_reason
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE kpis
    SET

        indicator_name = ?,

        target_value = ?,

        actual_value = ?,

        unit = ?,

        indicator_type = ?,

        framework_level = ?,

        linked_element = ?,

        stakeholder_priority = ?,

        deviation_reason = ?

    WHERE id = ?
    """, (

        indicator_name,

        target_value,

        actual_value,

        unit,

        indicator_type,

        framework_level,

        linked_element,

        stakeholder_priority,

        deviation_reason,

        kpi_id

    ))

    conn.commit()
    conn.close()


def create_performance_tracking_table():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS performance_tracking(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        project_id INTEGER,

        indicator_name TEXT,

        target_value REAL,

        actual_value REAL,

        deviation_reason TEXT

    )
    """)

    conn.commit()
    conn.close()

def add_performance_record(
    project_id,
    indicator_name,
    target_value,
    actual_value,
    deviation_reason
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO performance_tracking(
        project_id,
        indicator_name,
        target_value,
        actual_value,
        deviation_reason
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        project_id,
        indicator_name,
        target_value,
        actual_value,
        deviation_reason
    ))

    conn.commit()
    conn.close()

def get_performance_records(
    project_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM performance_tracking
    WHERE project_id = ?
    """, (project_id,))

    data = cursor.fetchall()

    conn.close()

    return data