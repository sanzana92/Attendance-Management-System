
from database import connect_database


def attendance_report():
    conn = connect_database()
    if conn is None:
        return

    cursor = conn.cursor()

    query = """
    SELECT
        s.student_id,
        s.reg_no,
        s.name,
        COUNT(a.attendance_id) AS total_classes,
        SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END) AS present_days,
        ROUND(
            SUM(CASE WHEN a.status = 'Present' THEN 1 ELSE 0 END)
            * 100.0 / NULLIF(COUNT(a.attendance_id), 0), 2
        ) AS attendance_percentage
    FROM students s
    LEFT JOIN attendance a ON s.student_id = a.student_id
    GROUP BY s.student_id, s.reg_no, s.name
    ORDER BY s.student_id
    """

    cursor.execute(query)
    records = cursor.fetchall()

    print("\n===== ATTENDANCE REPORT =====")

    for record in records:
        print(
            "ID:", record[0],
            "| Register No:", record[1],
            "| Name:", record[2],
            "| Total Classes:", record[3],
            "| Present:", record[4],
            "| Attendance:", record[5], "%"
        )

    cursor.close()
    conn.close()
