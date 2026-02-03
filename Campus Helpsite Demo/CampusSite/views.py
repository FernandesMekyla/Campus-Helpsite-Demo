from os import error
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager,UserMixin, login_user, logout_user, login_required
from werkzeug.security import check_password_hash

from CampusSite.db import get_conn

app = Flask(

    __name__,
    template_folder='templates'

    )

app.secret_key = "change-me"

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")


def validate_fk(value):
    value = (value or "").strip()
    return int(value) if value.isdigit() else None


@app.route("/times")
def times():
    return render_template("times.html")

@app.route("/thanks", methods =["POST"])
def thanks():
    name = request.form.get("name", "").strip()
    issue_type = request.form.get("issue_type", "").strip()
    return render_template("thanks.html", name=name, issue_type=issue_type)

@app.route("/tickets")
def tickets():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
        SELECT
            t.TicketId,
            t.Title,
            t.Status,
            t.CreatedAt,
            c.Name AS CategoryName,
            s.FullName AS AssignedTo
        FROM Tickets t 
        LEFT JOIN Categories c ON t.CategoryID = c.CategoryID
        LEFT JOIN Staff s ON t.StaffID = s.StaffID
        ORDER BY t.CreatedAt DESC;
        """)
        tickets = cur.fetchall()

    return render_template("tickets.html", tickets=tickets)

@app.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():
    error = None
    title = ""
    desc = ""
    category_raw = ""
    assigned_raw = ""
    
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        desc = request.form.get("description", "").strip()
        category_raw = request.form.get("category_id", "").strip()
        assigned_raw = request.form.get("assigned_to", "").strip()

        if not title or not desc:
            return render_template("new.html", error="Title and Description are required.")

        else:

            category_id = validate_fk(category_raw)
            assigned_to = validate_fk(assigned_raw)

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO dbo.tickets (Title, Description)
                VALUES (?, ?);
                """, (title, desc, category_id, staff_id))
            conn.commit()
        return redirect(url_for("tickets"))
        
    with get_conn() as conn:
                cur = conn.cursor()
                categories = cur.execute("""
                SELECT CategoryID, Name
                FROM dbo.Categories;
                ORDER BY Name;
                """).fetchall()

                staff = cur.execute("""
                SELECT StaffID, FullName
                FROM dbo.staff
                ORDER BY FullName;)
                """).fetchall()

    return render_template(
        "new.html", 
        error=error,
        categories=categories,
        staff=staff,
        title=title,
        description=desc,
    ) 

@app.route("/tickets/edit/<int:ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    with get_conn() as conn:
        cur = conn.cursor()

        if request.method == "POST":
            title = request.form.get("title", "").strip()
            desc = request.form.get("description", "").strip()
            status = request.form.get("status", "open").strip().lower()

            if not title or not desc or status not in ("open", "closed"):
                # Reload existing ticket for the form
                cur.execute("""
                    SELECT TicketId, Title, Description, Status
                    FROM dbo.Tickets
                    WHERE TicketId = ?;
                """, (ticket_id,))
                ticket = cur.fetchone()
                return render_template("edit.html", ticket=ticket, error="Please check your inputs.")

            cur.execute("""
                UPDATE dbo.Tickets
                SET Title = ?, Description = ?, Status = ?
                WHERE TicketId = ?;
            """, (title, desc, status, ticket_id))
            conn.commit()
            return redirect(url_for("tickets"))

        # GET: load existing ticket
        cur.execute("""
            SELECT TicketId, Title, Description, Status
            FROM dbo.Tickets
            WHERE TicketId = ?;
        """, (ticket_id,))
        ticket = cur.fetchone()

    if ticket is None:
        return "Ticket not found", 404

    return render_template("edit.html", ticket=ticket, error=None)

@app.route("/tickets/delete/<int:ticket_id>", methods=["POST"])
def delete_ticket(ticket_id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM dbo.Tickets WHERE TicketId = ?;", (ticket_id,))
        conn.commit()

    return redirect(url_for("tickets"))


