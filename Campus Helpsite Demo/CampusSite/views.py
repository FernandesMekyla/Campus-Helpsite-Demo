from flask import Flask, render_template, request, redirect, url_for
from CampusSite.db import get_conn

app = Flask(

    __name__,
    template_folder='templates'

    )

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/services")
def services():
    return render_template("services.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

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
            SELECT TicketId, Title, Description, Status, CreatedAt
            FROM dbo.Tickets
            ORDER BY TicketId DESC;
        """)
        tickets = cur.fetchall()

    return render_template("tickets.html", tickets=tickets)

@app.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        desc = request.form.get("description", "").strip()

        if not title or not desc:
            return render_template("new.html", error="Title and Description are required.")

        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                """INSERT INTO dbo.tickets (Title, Description)
                VALUES (?, ?);
                """, (title, desc)
            )
            conn.commit()

        return redirect(url_for("tickets"))
        
    return render_template("new.html", error=None)

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
