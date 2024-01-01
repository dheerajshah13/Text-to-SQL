learn_questions = [
    {
        'Question': "Find the names and total revenue of the top 5 paying customers.",
        'SQLQuery': """
            SELECT
                customer_id,
                CONCAT(first_name, ' ', last_name) AS customer_name,
                SUM(amount) AS total_revenue
            FROM
                payment
                JOIN customer USING(customer_id)
            GROUP BY
                customer_id
            ORDER BY
                total_revenue DESC
            LIMIT 5;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Customer names and total revenue for the top 5 paying customers."
    },
    {
        'Question': "List the films that have been rented the most.",
        'SQLQuery': """
            SELECT
                film_id,
                title,
                COUNT(rental_id) AS rental_count
            FROM
                film
                JOIN inventory USING (film_id)
                JOIN rental USING (inventory_id)
            GROUP BY
                film_id
            ORDER BY
                rental_count DESC;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Film titles and rental counts for the most rented films."
    },
    {
        'Question': "Find the customers who have rented more than 50 films.",
        'SQLQuery': """
            SELECT
                customer_id,
                CONCAT(first_name, ' ', last_name) AS customer_name,
                COUNT(rental_id) AS rental_count
            FROM
                customer
                JOIN rental USING (customer_id)
            GROUP BY
                customer_id
            HAVING
                rental_count > 50;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Customer names and rental counts for customers who rented more than 50 films."
    },
    {
        'Question': "Retrieve the films that are in the 'Action' category and have not been rented.",
        'SQLQuery': """
            SELECT
                film_id,
                title
            FROM
                film
                JOIN film_category USING (film_id)
                LEFT JOIN rental USING (film_id)
            WHERE
                category_id = 1 AND rental_id IS NULL;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Film titles in the 'Action' category that have not been rented."
    },
    {
        'Question': "Find the staff members with the highest number of rentals.",
        'SQLQuery': """
            SELECT
                staff_id,
                CONCAT(first_name, ' ', last_name) AS staff_name,
                COUNT(rental_id) AS rental_count
            FROM
                staff
                LEFT JOIN rental USING (staff_id)
            GROUP BY
                staff_id
            ORDER BY
                rental_count DESC
            LIMIT 1;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Staff names and rental counts for the staff member with the highest number of rentals."
    },
    {
        'Question': "List the films that are available for rent at a specific store.",
        'SQLQuery': """
            SELECT
                film_id,
                title
            FROM
                film
                JOIN inventory USING (film_id)
            WHERE
                inventory.store_id = 1;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Film titles available for rent at a specific store."
    },
    {
        'Question': "Calculate the average rental duration for each film.",
        'SQLQuery': """
            SELECT
                film_id,
                title,
                AVG(return_date - rental_date) AS avg_rental_duration
            FROM
                film
                JOIN rental USING (film_id)
            GROUP BY
                film_id
            ORDER BY
                avg_rental_duration DESC;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Film titles and their average rental duration."
    },
    {
        'Question': "Find the customers who have rented all the films in a specific category.",
        'SQLQuery': """
            SELECT
                customer_id,
                CONCAT(first_name, ' ', last_name) AS customer_name
            FROM
                customer
                CROSS JOIN category
                LEFT JOIN (
                    SELECT
                        customer_id,
                        film_id
                    FROM
                        rental
                        JOIN inventory USING (inventory_id)
                        JOIN film_category USING (film_id)
                    WHERE
                        category_id = 1
                ) AS rented_films USING (customer_id, film_id)
            GROUP BY
                customer_id
            HAVING
                COUNT(film_id) = COUNT(rented_films.film_id);
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Customer names who have rented all films in a specific category."
    },
    {
        'Question': "Retrieve the films that have not been rented in the last 30 days.",
        'SQLQuery': """
            SELECT
                film_id,
                title
            FROM
                film
                LEFT JOIN inventory USING (film_id)
                LEFT JOIN rental USING (inventory_id)
            WHERE
                rental_date IS NULL OR rental_date < (NOW() - INTERVAL 30 DAY);
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Film titles that have not been rented in the last 30 days."
    },
    {
        'Question': "Calculate the total revenue generated by each film category.",
        'SQLQuery': """
            SELECT
                category_id,
                name AS category_name,
                SUM(amount) AS total_revenue
            FROM
                category
                JOIN film_category USING (category_id)
                JOIN film USING (film_id)
                JOIN inventory USING (film_id)
                JOIN rental USING (inventory_id)
                JOIN payment USING (rental_id)
            GROUP BY
                category_id
            ORDER BY
                total_revenue DESC;
        """,
        'SQLResult': "Result of the SQL query",
        'Answer': "Total revenue for each film category."
    }
]
