GO
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